from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


# 🔹 User Profile Serializer (사용자 정보 + 상품 목록)
class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name',
            'profile_image',
        ]

    def get_profile_image(self, obj):
        return obj.profile_image.url if obj.profile_image else None
