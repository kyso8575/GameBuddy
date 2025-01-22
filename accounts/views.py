from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model  # 커스텀 User 모델 가져오기
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.views import APIView


User = get_user_model()  # 현재 설정된 사용자 모델


class LoginView(APIView):
    """
    사용자 로그인 API
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            serializer = UserSerializer(user)
            return Response({"message": "로그인 성공", "user": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "유효하지 않은 사용자 이름 또는 비밀번호입니다."}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            auth_logout(request)
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        return Response({"detail": "User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)


class SignupAPIView(APIView):
    """
    API 기반 회원가입 뷰
    """
    def post(self, request):
        full_name = request.data.get("full_name")
        username = request.data.get("username")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        # 필수 필드 확인
        if not all([full_name, username, password, confirm_password]):
            return Response(
                {"detail": "All fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 사용자 이름 중복 확인
        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Username is already taken."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 비밀번호 일치 여부 확인
        if password != confirm_password:
            return Response(
                {"detail": "Passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 비밀번호 검증
        try:
            validate_password(password)
        except ValidationError as e:
            return Response(
                {"detail": e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 사용자 생성
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=full_name
        )
        user.save()

        return Response(
            {"detail": "Account created successfully!"},
            status=status.HTTP_201_CREATED
        )


class UserProfileAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, id):
        # 사용자 정보
        user = get_object_or_404(User, id=id)
        
        # 직렬화
        user_serializer = UserSerializer(user, context={'request': request})
        
        return Response({
            'user_profile': user_serializer.data
        })