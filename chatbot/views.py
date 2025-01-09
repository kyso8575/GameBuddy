from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatSession
from .serializers import ChatSessionSerializer
from .chatbot import generate_answer
from django.contrib.auth.models import User




# 공통 사용자 확인 함수
def get_user_from_request(request):
    user_id = request.data.get('user_id') or request.query_params.get('user_id')
    if not user_id:
        return None, {"error": "user_id is required"}, status.HTTP_400_BAD_REQUEST

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None, {"error": "User not found"}, status.HTTP_404_NOT_FOUND

    return user, None, None


# 세션 처리 함수
def handle_chat_session(user, message, session_id=None):
    bot_response = generate_answer(message)
    session_message = {
        "user_message": message,
        "bot_response": bot_response,
    }

    # session_id가 있으면 해당 세션을 업데이트, 없으면 새로운 세션 생성
    if session_id:
        try:
            # 기존 세션을 가져옴
            chat_session = ChatSession.objects.get(id=session_id, user=user)

            # 기존 메시지가 리스트 형식으로 저장되어 있지 않으면, 리스트로 변환
            existing_messages = chat_session.message if isinstance(chat_session.message, list) else [chat_session.message]

            # 새 메시지를 기존 메시지 목록에 추가
            existing_messages.append(session_message)

            # 업데이트된 메시지 목록을 저장
            chat_session.message = existing_messages
            chat_session.save()
        except ChatSession.DoesNotExist:
            return None, {"error": "Session not found or user mismatch"}
    else:
        # 새로운 세션 생성 (message를 리스트로 저장)
        chat_session = ChatSession.objects.create(user=user, message=[session_message])

    return chat_session, None


class LoadSessionView(APIView):
    def get(self, request):
        # user 정보와 에러 처리
        user, error, status_code = get_user_from_request(request)
        if error:
            return Response(error, status=status_code)

        # 요청에서 session_id를 받음
        session_id = request.query_params.get('session_id')

        if not session_id:
            return Response({"error": "session_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 해당 session_id에 맞는 세션을 가져오기
        try:
            chat_session = ChatSession.objects.get(id=session_id, user=user)
        except ChatSession.DoesNotExist:
            return Response({"error": "Session not found or user mismatch"}, status=status.HTTP_404_NOT_FOUND)

        # 직렬화하여 반환
        serializer = ChatSessionSerializer(chat_session)
        return Response(serializer.data)


class ProcessSessionView(APIView):
    def post(self, request):
        user, error, status_code = get_user_from_request(request)
        if error:
            return Response(error, status=status_code)

        message = request.data.get('message')
        session_id = request.data.get('session_id')

        if not message:
            return Response({"error": "message is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 세션 처리
        chat_session, error = handle_chat_session(user, message, session_id)
        if error:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        # 직렬화하여 응답 반환
        serializer = ChatSessionSerializer(chat_session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StartSessionView(APIView):
    def post(self, request):
        user, error, status_code = get_user_from_request(request)
        if error:
            return Response(error, status=status_code)

        message = request.data.get('message')
        if not message:
            return Response({"error": "message is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 세션 처리
        chat_session, error = handle_chat_session(user, message)
        if error:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        # 직렬화하여 응답 반환
        serializer = ChatSessionSerializer(chat_session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)