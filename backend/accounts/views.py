from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model  # Get custom User model
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer, ProfileImageSerializer
from rest_framework.views import APIView


User = get_user_model()  # Current configured user model


class LoginView(APIView):
    """
    User Login API (Token authentication only)
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Create or get token
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response({
                "message": "Login successful", 
                "user": serializer.data,
                "token": token.key
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    Logout API (Token authentication only)
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Delete user token
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


class SignupAPIView(APIView):
    """
    API based Signup view
    """
    def post(self, request):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        username = request.data.get("username")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        # Check required fields
        if not all([first_name, last_name, username, password, confirm_password]):
            return Response(
                {"detail": "All fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check username duplicate
        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Username is already taken."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check password match
        if password != confirm_password:
            return Response(
                {"detail": "Passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Password validation
        try:
            # Use Django's default password validation function
            validate_password(password)
        except ValidationError as e:
            # Print validation error messages (for debugging)
            print(f"Password validation error: {e.messages}")
            
            # Convert to REST Framework ValidationError
            # This allows DRF exception handling system to properly generate a response
            raise ValidationError(detail=e.messages)

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # Create token
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)

        return Response(
            {
                "detail": "Account created successfully!", 
                "user": serializer.data,
                "token": token.key
            },
            status=status.HTTP_201_CREATED
        )


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        # Retrieve user information
        user = get_object_or_404(User, id=id)
        
        # Serialization
        user_serializer = UserSerializer(user, context={'request': request})
        
        return Response({
            'user_profile': user_serializer.data
        })


class CurrentUserView(APIView):
    """
    API that returns current logged-in user information
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)


class ChangePasswordView(APIView):
    """
    Password Change API
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # Check required fields
        if not all([current_password, new_password, confirm_password]):
            return Response(
                {"detail": "All fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify current password
        user = request.user
        if not user.check_password(current_password):
            return Response(
                {"detail": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check new passwords match
        if new_password != confirm_password:
            return Response(
                {"detail": "New passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate new password
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response(
                {"detail": e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Change password
        user.set_password(new_password)
        user.save()

        # Reissue token (invalidate current token after password change)
        Token.objects.filter(user=user).delete()
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "detail": "Password changed successfully.",
                "token": token.key
            }, 
            status=status.HTTP_200_OK
        )


class ProfileImageUpdateView(APIView):
    """
    Profile Image Update API
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        serializer = ProfileImageSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Return updated user information
            user_serializer = UserSerializer(request.user, context={'request': request})
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)