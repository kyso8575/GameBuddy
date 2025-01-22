from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Game
from .serializers import GameSerializer

class GameListView(APIView):    
    # 필터링해서, metacrictic_score를 기반으로 상위 30개의 게임 추출
    def post(self, request):
        genre_filter = request.data.get('genres', None)
        playtime_filter = request.data.get('playtime', None)
        esrb_rating_filter = request.data.get('esrb_rating', None)
        platform_filter = request.data.get('platforms', None)
        
        games = Game.objects.all().order_by('-metacritic_score')

        # 장르 필터링 (SQLite에서 __contains는 지원되지 않으므로 Python에서 처리)
        if genre_filter and genre_filter != "전체":
            games = [game for game in games if genre_filter in game.genres]

        # 플레이 시간 필터링
        if playtime_filter and playtime_filter != "전체":
            games = [game for game in games if game.playtime == playtime_filter]

        # ESRB 등급 필터링
        if esrb_rating_filter and esrb_rating_filter != "전체":
            games = [game for game in games if game.esrb_rating == esrb_rating_filter]

        # 플랫폼 필터링
        if platform_filter and platform_filter != "전체":
            games = [game for game in games if platform_filter in game.platforms]

        games = games[:30]
        # 필터링된 결과 직렬화
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
