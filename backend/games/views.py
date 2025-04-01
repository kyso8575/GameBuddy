from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Game
from .serializers import GameSerializer
import math
import requests
import os
from django.conf import settings

class GameListView(APIView):    
    # 필터링 및 페이지네이션 적용
    def post(self, request):
        # 필터 파라미터 가져오기
        genre_filter = request.data.get('genres', None)
        platform_filter = request.data.get('platforms', None)
        search_query = request.data.get('search', '')
        
        # 페이지네이션 파라미터 가져오기
        page = int(request.data.get('page', 1))
        items_per_page = int(request.data.get('items_per_page', 50))
        
        # 기본 쿼리셋
        games = Game.objects.all().order_by('-metacritic_score')

        # 검색어 필터링 (제목에 검색어가 포함된 게임만 필터링)
        if search_query:
            games = [game for game in games if search_query.lower() in game.name.lower()]

        # 장르 필터링 (SQLite에서 __contains는 지원되지 않으므로 Python에서 처리)
        if genre_filter and genre_filter != "All Genres":
            games = [game for game in games if genre_filter in game.genres]


        # 플랫폼 필터링
        if platform_filter and platform_filter != "All Platforms":
            games = [game for game in games if platform_filter in game.platforms]

        # 전체 게임 수와 페이지 수 계산
        total_items = len(games)
        total_pages = math.ceil(total_items / items_per_page)
        
        # 페이지네이션 적용
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        paginated_games = games[start_index:end_index]
        
        # 필터링된 결과 직렬화
        serializer = GameSerializer(paginated_games, many=True)
        
        # 응답 데이터 구성 (게임 목록 + 페이지네이션 정보)
        response_data = {
            'games': serializer.data,
            'total_items': total_items,
            'total_pages': total_pages,
            'current_page': page
        }
        
        return Response(response_data)

class GameDetailView(APIView):
    def get(self, request, game_id):
        try:
            # 특정 ID를 가진 게임 찾기
            game = Game.objects.get(id=game_id)
            
            # description이 없는 경우 RAWG API에서 가져오기
            if not game.description:
                # RAWG API 키 가져오기
                api_key = os.environ.get('RAWG_API_KEY', '')
                
                if api_key:
                    # RAWG API 요청
                    api_url = f"https://api.rawg.io/api/games/{game_id}?key={api_key}"
                    response = requests.get(api_url)
                    
                    # 요청이 성공적이고 응답에 description이 있으면 저장
                    if response.status_code == 200:
                        data = response.json()
                        if 'description' in data:
                            game.description = data['description']
                            game.save()
            
            # 게임 데이터 직렬화
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist:
            return Response(
                {"error": "Game not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
