from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Review

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """리뷰 작성자 정보를 위한 시리얼라이저"""
    class Meta:
        model = User
        fields = ['id', 'username']

class ReviewSerializer(serializers.ModelSerializer):
    """리뷰 시리얼라이저"""
    user = UserSerializer(read_only=True)
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'username', 'game', 'rating', 'review', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_username(self, obj):
        """리뷰 작성자 이름을 반환 (호환성을 위해)"""
        return obj.user.username if obj.user else None
        
    def create(self, validated_data):
        """현재 로그인한 사용자를 리뷰 작성자로 설정"""
        request = self.context.get('request')
        
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
            
        return super().create(validated_data)
