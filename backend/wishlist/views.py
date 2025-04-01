from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Wishlist
from .serializers import WishlistSerializer
from games.models import Game

# Create your views here.

class WishlistListView(APIView):
    """사용자의 위시리스트 조회 및 게임 추가"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """사용자의 위시리스트 아이템 목록 조회"""
        wishlist_items = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist_items, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """게임을 위시리스트에 추가"""
        game_id = request.data.get('game_id')
        
        if not game_id:
            return Response(
                {"error": "게임 ID가 필요합니다."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 게임 존재 여부 확인
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response(
                {"error": "해당 게임을 찾을 수 없습니다."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 이미 위시리스트에 있는지 확인
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            game=game
        )
        
        if not created:
            return Response(
                {"message": "이미 위시리스트에 추가된 게임입니다."}, 
                status=status.HTTP_200_OK
            )
        
        serializer = WishlistSerializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class WishlistDetailView(APIView):
    """특정 위시리스트 아이템 조회 및 삭제"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, game_id):
        """특정 게임이 위시리스트에 있는지 확인"""
        wishlist_item = get_object_or_404(
            Wishlist, 
            user=request.user,
            game_id=game_id
        )
        serializer = WishlistSerializer(wishlist_item)
        return Response(serializer.data)
    
    def delete(self, request, game_id):
        """위시리스트에서 게임 제거"""
        try:
            wishlist_item = Wishlist.objects.get(
                user=request.user,
                game_id=game_id
            )
            wishlist_item.delete()
            return Response(
                {"message": "위시리스트에서 게임이 삭제되었습니다."},
                status=status.HTTP_200_OK
            )
        except Wishlist.DoesNotExist:
            return Response(
                {"error": "위시리스트에 해당 게임이 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

class WishlistStatusView(APIView):
    """게임이 위시리스트에 있는지 확인하는 API"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, game_id):
        """게임이 위시리스트에 있는지 확인"""
        is_in_wishlist = Wishlist.objects.filter(
            user=request.user, 
            game_id=game_id
        ).exists()
        
        return Response({
            'is_in_wishlist': is_in_wishlist
        })
