from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Review
from .serializers import ReviewSerializer
from games.models import Game
import math

# 사용자 권한 클래스
class IsOwnerOrReadOnly:
    """
    객체의 소유자만 수정/삭제할 수 있도록 하는 권한
    """
    def has_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 허용
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # 쓰기 권한은 리뷰 작성자에게만 허용
        return obj.user == request.user

class ReviewListView(APIView):
    """
    리뷰 목록 조회 및 새 리뷰 생성 API
    """
    
    def get(self, request):
        """리뷰 목록을 조회합니다."""
        # 쿼리 파라미터로 필터링
        game_id = request.query_params.get('game_id')
        user_id = request.query_params.get('user_id')
        
        # 페이지네이션 파라미터
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 5))
        ordering = request.query_params.get('ordering', '-created_at')
        
        # 기본 쿼리셋
        reviews = Review.objects.all()
        
        # 필터링 적용
        if game_id:
            reviews = reviews.filter(game_id=game_id)
        if user_id:
            reviews = reviews.filter(user_id=user_id)
            
        # 정렬 적용
        reviews = reviews.order_by(ordering)
        
        # 전체 리뷰 수와 페이지 수 계산
        total_reviews = reviews.count()
        total_pages = math.ceil(total_reviews / page_size)
        
        # 페이지네이션 적용
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_reviews = reviews[start_index:end_index]
        
        # 평균 평점 계산 (필터링된 리뷰 기준)
        avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        
        # 직렬화
        serializer = ReviewSerializer(paginated_reviews, many=True)
        
        # 응답 데이터 구성
        response_data = {
            'reviews': serializer.data,
            'pagination': {
                'total_reviews': total_reviews,
                'total_pages': total_pages,
                'current_page': page,
                'page_size': page_size,
            },
            'average_rating': avg_rating,
        }
        
        return Response(response_data)
    
    def post(self, request):
        """새 리뷰를 생성합니다."""
        # 인증 확인
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # 게임 ID 확인
        game_id = request.data.get('game_id')
        if not game_id:
            return Response(
                {"error": "Game ID is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 게임 존재 여부 확인
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response(
                {"error": "Game not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 이미 리뷰가 존재하는지 확인
        existing_review = Review.objects.filter(
            user=request.user,
            game_id=game_id
        ).first()
        
        if existing_review:
            return Response(
                {"error": "You have already reviewed this game"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 데이터 유효성 검사
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # 게임과 사용자 정보 설정
            serializer.save(user=request.user, game=game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(APIView):
    """
    특정 리뷰 조회, 수정, 삭제 API
    """
    
    def get(self, request, review_id):
        """특정 리뷰를 조회합니다."""
        try:
            review = Review.objects.get(id=review_id)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist:
            return Response(
                {"error": "Review not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request, review_id):
        """특정 리뷰를 수정합니다."""
        # 인증 확인
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            review = Review.objects.get(id=review_id)
            
            # 권한 확인
            if review.user != request.user:
                return Response(
                    {"error": "You do not have permission to edit this review"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # 데이터 유효성 검사
            serializer = ReviewSerializer(review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Review.DoesNotExist:
            return Response(
                {"error": "Review not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request, review_id):
        """특정 리뷰를 삭제합니다."""
        # 인증 확인
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            review = Review.objects.get(id=review_id)
            
            # 권한 확인
            if review.user != request.user:
                return Response(
                    {"error": "You do not have permission to delete this review"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # 리뷰 삭제
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Review.DoesNotExist:
            return Response(
                {"error": "Review not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class GameReviewsView(APIView):
    """
    특정 게임의 리뷰 목록 조회 API
    """
    
    def get(self, request, game_id):
        """특정 게임의 리뷰 목록을 조회합니다."""
        # 게임 존재 여부 확인
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response(
                {"error": "Game not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 페이지네이션 파라미터
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 5))
        ordering = request.query_params.get('ordering', '-created_at')
        
        # 해당 게임의 리뷰 쿼리셋
        reviews = Review.objects.filter(game_id=game_id).order_by(ordering)
        
        # 전체 리뷰 수와 페이지 수 계산
        total_reviews = reviews.count()
        total_pages = math.ceil(total_reviews / page_size) if total_reviews > 0 else 1
        
        # 페이지네이션 적용
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_reviews = reviews[start_index:end_index]
        
        # 평균 평점 계산
        avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        
        # 직렬화
        serializer = ReviewSerializer(paginated_reviews, many=True)
        
        # 응답 데이터 구성
        response_data = {
            'reviews': serializer.data,
            'pagination': {
                'total_reviews': total_reviews,
                'total_pages': total_pages,
                'current_page': page,
                'page_size': page_size,
            },
            'average_rating': avg_rating,
        }
        
        return Response(response_data)

class UserGameReviewView(APIView):
    """
    현재 로그인한 사용자의 특정 게임 리뷰 조회 API
    """
    
    def get(self, request, game_id):
        """현재 사용자의 특정 게임에 대한 리뷰를 조회합니다."""
        # 인증 확인
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # 게임 존재 여부 확인
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response(
                {"error": "Game not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 사용자의 리뷰 조회
        try:
            review = Review.objects.get(user=request.user, game_id=game_id)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist:
            # 리뷰가 없는 경우 404 대신 200 응답으로 리뷰가 없다는 정보 반환
            return Response(
                {
                    "has_review": False,
                    "message": "You have not reviewed this game yet"
                }, 
                status=status.HTTP_200_OK
            )
