from django.core.management.base import BaseCommand
import requests
from games.models import Game
import os
from dotenv import load_dotenv
import concurrent.futures
import json
from django.db import transaction
import time
import datetime
import threading
import sys
from queue import Queue
import random

load_dotenv()

class Command(BaseCommand):
    help = 'Fetch and save game data from API using threads for faster processing'

    def add_arguments(self, parser):
        parser.add_argument('--max-pages', type=int, default=1000,
                           help='Maximum number of pages to fetch (default: 1000)')
        parser.add_argument('--workers', type=int, default=10,
                           help='Number of worker threads to use (default: 10)')
        parser.add_argument('--batch-size', type=int, default=100,
                           help='Batch size for saving games (default: 100)')
        parser.add_argument('--start-page', type=int, default=1,
                           help='Start page number (default: 1)')

    def log_info(self, message):
        """로그 메시지 출력 (시간 포함)"""
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        thread_id = threading.current_thread().name
        self.stdout.write(self.style.SUCCESS(f"[{current_time}][{thread_id}] {message}"))

    def log_warning(self, message):
        """경고 로그 메시지 출력"""
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        thread_id = threading.current_thread().name
        self.stdout.write(self.style.WARNING(f"[{current_time}][{thread_id}] {message}"))

    def log_error(self, message):
        """에러 로그 메시지 출력"""
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        thread_id = threading.current_thread().name
        self.stdout.write(self.style.ERROR(f"[{current_time}][{thread_id}] {message}"))

    def fetch_page(self, url, page_index=None):
        """Fetch a single page of game data"""
        try:
            thread_name = threading.current_thread().name
            self.log_info(f"쓰레드 {thread_name}가 페이지 {page_index if page_index is not None else '?'} 요청 중: {url}")
            
            # 쓰레드별 요청 간 약간의 무작위 지연을 추가하여 API 서버 부하 분산
            time.sleep(random.uniform(0.1, 0.5))
            
            start_time = time.time()
            response = requests.get(url)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                result_count = len(data['results'])
                self.log_info(f"페이지 {page_index if page_index is not None else '?'} 데이터 {result_count}개 수신 완료 ({elapsed:.2f}초)")
                return {
                    'results': data['results'],
                    'next': data.get('next'),
                    'page_index': page_index
                }
            else:
                self.log_error(f"API 요청 실패: {response.status_code} for URL: {url}")
                return None
        except Exception as e:
            self.log_error(f"Error fetching page {url}: {str(e)}")
            return None

    def process_game(self, game_data):
        """Process a single game data and return a Game model instance"""
        try:
            # 게임 ID 가져오기
            game_id = game_data.get('id')
            if not game_id:
                self.log_warning(f"Game without ID: {game_data.get('name', 'unknown')}")
                return None

            # genres에서 name만 추출, 기본값은 빈 문자열
            genres = [genre.get('name', '') for genre in game_data.get('genres', [])]

            # platforms에서 name만 추출, 기본값은 빈 문자열
            platforms = [platform.get('platform', {}).get('name', '') for platform in game_data.get('platforms', [])]

            # stores에서 name만 추출, 기본값은 빈 문자열
            store_names = [store_data.get('store', {}).get('name', '') for store_data in game_data.get('stores', [])]

            # short_screenshots에서 image만 추출, 기본값은 빈 문자열
            screenshots = [screenshot.get('image', '') for screenshot in game_data.get('short_screenshots', [])]
            
            # esrb_rating 처리: 없으면 빈 문자열로 설정
            esrb_rating = game_data.get('esrb_rating')
            esrb_rating = esrb_rating.get('name', '') if esrb_rating else ''

            # Game 데이터 생성 (아직 저장하지 않음)
            return {
                'id': game_id,  # API에서 제공하는 ID 사용
                'name': game_data.get('name', ''),
                'released': game_data.get('released', ''),
                'background_image': game_data.get('background_image', ''),
                'rating': game_data.get('rating', 0),
                'metacritic_score': game_data.get('metacritic', 0),
                'playtime': game_data.get('playtime', 0),
                'platforms': json.dumps(platforms),  # JSON 문자열로 저장
                'genres': json.dumps(genres),        # JSON 문자열로 저장
                'stores': ','.join(store_names),     # 쉼표로 구분된 문자열로 저장
                'esrb_rating': esrb_rating,
                'screenshots': json.dumps(screenshots)  # JSON 문자열로 저장
            }
        except Exception as e:
            self.log_error(f"Error processing game {game_data.get('name', 'unknown')}: {str(e)}")
            return None

    def save_games_batch(self, games_data, batch_index=None):
        """Save a batch of games to the database with transaction"""
        saved_count = 0
        start_time = time.time()
        try:
            new_games = 0
            existing_games = 0
            with transaction.atomic():
                for game_data in games_data:
                    if game_data:
                        game_id = game_data['id']
                        if not Game.objects.filter(id=game_id).exists():
                            game = Game(**game_data)
                            game.save()
                            saved_count += 1
                            new_games += 1
                        else:
                            existing_games += 1
            
            elapsed = time.time() - start_time
            self.log_info(f"배치 {batch_index if batch_index is not None else '?'} 저장 완료: "
                         f"새 게임 {new_games}개, 이미 존재하는 게임 {existing_games}개 ({elapsed:.2f}초)")
            return saved_count
        except Exception as e:
            self.log_error(f"Error saving batch: {str(e)}")
            return 0
    
    def fetch_and_process_page(self, page_info):
        """페이지를 가져와서 처리하는 통합 함수 (쓰레드에서 실행)"""
        url = page_info['url']
        page_index = page_info['page_index']
        
        page_data = self.fetch_page(url, page_index)
        if not page_data:
            return None
            
        result = {'page_index': page_index, 'processed_games': []}
        
        # 게임 데이터 처리
        for game_data in page_data['results']:
            processed_game = self.process_game(game_data)
            if processed_game:
                result['processed_games'].append(processed_game)
                
        return result

    def handle(self, *args, **kwargs):
        start_time = time.time()
        total_start_time = datetime.datetime.now()
        
        max_pages = kwargs['max_pages']
        workers = kwargs['workers']
        batch_size = kwargs['batch_size']
        start_page = kwargs['start_page']
        
        self.log_info(f"==== 데이터 수집 시작 ====")
        self.log_info(f"최대 페이지 수: {max_pages}, 작업자 수: {workers}, 배치 크기: {batch_size}, 시작 페이지: {start_page}")
        self.log_info(f"시작 시간: {total_start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # 공유 데이터 구조
        result_queue = Queue()  # 처리된 게임 데이터를 저장할 큐
        api_key = os.getenv('RAWG_API_KEY')
        
        # API 요청 URL 템플릿
        base_url = f"https://api.rawg.io/api/games?key={api_key}"
        
        # 간단히 처리: 페이지 번호만 바꿔서 URL 생성
        urls_to_fetch = []
        end_page = start_page + max_pages - 1
        
        for page_index in range(start_page, end_page + 1):
            page_url = f"{base_url}&page={page_index}" if page_index > 1 else base_url
            urls_to_fetch.append({
                'url': page_url,
                'page_index': page_index
            })
        
        total_pages = len(urls_to_fetch)
        self.log_info(f"총 {total_pages}개 페이지 URL 준비 완료")
        self.log_info(f"병렬 데이터 수집 시작...")

        saved_count = 0
        games_to_save = []
        batch_count = 0
        completed_count = 0

        # 병렬 처리 시작
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            # 작업 제출 (임의의 순서로 섞어서 처리)
            page_infos = list(urls_to_fetch)  # 복사본 생성
            random.shuffle(page_infos)  # 페이지 순서 무작위화 (API 서버 부하 분산)
            
            self.log_info(f"총 {len(page_infos)}개 페이지 작업을 {workers}개 쓰레드에 할당")
            
            # 실제 쓰레드 풀에 작업 제출
            future_to_page = {
                executor.submit(self.fetch_and_process_page, page_info): page_info 
                for page_info in page_infos
            }
            
            # 작업 완료 상태 확인 로그
            self.log_info(f"총 {len(future_to_page)}개 작업 제출 완료, 결과 수집 시작")
            
            # 완료된 작업 결과 수집
            for future in concurrent.futures.as_completed(future_to_page):
                page_info = future_to_page[future]
                completed_count += 1
                
                # 진행 상황 표시
                progress_percentage = (completed_count / total_pages) * 100
                self.log_info(f"페이지 처리 진행 상황: {completed_count}/{total_pages} ({progress_percentage:.1f}%)")
                
                try:
                    result = future.result()
                    if result:
                        processed_games = result['processed_games']
                        page_idx = result['page_index']
                        
                        self.log_info(f"페이지 {page_idx}에서 {len(processed_games)}개 게임 처리 완료")
                        
                        # 처리된 게임 데이터 저장 목록에 추가
                        games_to_save.extend(processed_games)
                        
                        # 배치 크기에 도달하면 저장
                        while len(games_to_save) >= batch_size:
                            batch_count += 1
                            batch_to_save = games_to_save[:batch_size]
                            games_to_save = games_to_save[batch_size:]
                            
                            batch_saved = self.save_games_batch(batch_to_save, batch_count)
                            saved_count += batch_saved
                            
                            # 현재까지의 통계 출력
                            elapsed_time = time.time() - start_time
                            games_per_second = saved_count / elapsed_time if elapsed_time > 0 else 0
                            self.log_info(f"현재까지 {saved_count}개 게임 저장 완료 (평균 속도: {games_per_second:.1f} 게임/초)")
                except Exception as e:
                    self.log_error(f"페이지 {page_info['page_index']} 처리 중 오류 발생: {str(e)}")

        # 남은 게임 데이터 저장
        if games_to_save:
            batch_count += 1
            batch_saved = self.save_games_batch(games_to_save, batch_count)
            saved_count += batch_saved

        # 최종 결과 출력
        total_end_time = datetime.datetime.now()
        total_elapsed = total_end_time - total_start_time
        total_elapsed_seconds = total_elapsed.total_seconds()
        
        self.log_info(f"==== 데이터 수집 완료 ====")
        self.log_info(f"총 {saved_count}개 게임 데이터 저장 (총 {total_pages}개 페이지에서)")
        self.log_info(f"시작 시간: {total_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log_info(f"종료 시간: {total_end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log_info(f"총 소요 시간: {total_elapsed}")
        
        if total_elapsed_seconds > 0:
            games_per_second = saved_count / total_elapsed_seconds
            self.log_info(f"처리 속도: {games_per_second:.2f} 게임/초")
        
        # DB 상태 요약
        total_games = Game.objects.count()
        self.log_info(f"데이터베이스 내 총 게임 수: {total_games}개")