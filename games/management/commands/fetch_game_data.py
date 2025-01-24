from django.core.management.base import BaseCommand
import requests
from games.models import Game
import os
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = 'Fetch and save game data from API'

    def handle(self, *args, **kwargs):
        # API 요청 URL
        api_url = f"https://api.rawg.io/api/games?key={os.getenv('RAWG_API_KEY')}"
        page_count = 0  # 페이지 요청 횟수 카운트
        saved_count = 0  # 저장된 게임의 수 카운트

        while api_url and page_count < 10000:  # `next`가 없거나 페이지 수가 10000을 넘지 않도록 제한
            # API 요청
            response = requests.get(api_url)

            if response.status_code == 200:
                games_data = response.json()['results']  # API에서 결과를 가져옵니다.

                for game_data in games_data:
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

                    # 이미 데이터가 있는지 확인
                    if not Game.objects.filter(name=game_data.get('name', '')).exists():
                        # Game 모델에 데이터 저장
                        game = Game(
                            name=game_data.get('name', ''),  # 기본값 빈 문자열
                            released=game_data.get('released', ''),  # 기본값 빈 문자열
                            background_image=game_data.get('background_image', ''),  # 기본값 빈 문자열
                            rating=game_data.get('rating', 0),  # 기본값 0
                            metacritic_score=game_data.get('metacritic', 0),
                            playtime=game_data.get('playtime', 0),  # 기본값 0
                            platforms=platforms,  # name만 추출한 리스트
                            genres=genres,        # name만 추출한 리스트
                            stores=store_names,  # 이름만 추출한 리스트
                            esrb_rating=esrb_rating,  # esrb_rating이 없으면 빈 문자열
                            screenshots=screenshots  # 이미지가 없으면 빈 리스트
                        )
                        game.save()
                        saved_count += 1

                # 10페이지마다 저장된 게임 수 로그 출력
                if (page_count + 1) % 10 == 0:
                    self.stdout.write(self.style.SUCCESS(f"Saved {saved_count} games after {page_count + 1} pages"))

                # next 페이지가 있는지 확인하여, 있으면 그 URL을 api_url로 설정
                api_url = response.json().get('next')

                if api_url:
                    page_count += 1  # 페이지 요청 횟수 증가
                else:
                    self.stdout.write(self.style.SUCCESS('No more pages.'))
            else:
                self.stdout.write(self.style.ERROR(f"API 요청 실패: {response.status_code}"))
                break  # 실패한 경우 루프 종료

        # 페이지가 10,000번을 넘으면 종료
        if page_count >= 10000:
            self.stdout.write(self.style.WARNING('Reached the maximum number of pages (10,000).'))