from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Django ValidationError를 REST Framework API 응답으로 변환하는 커스텀 예외 핸들러
    """
    # 기본 DRF 예외 핸들러를 먼저 호출
    response = exception_handler(exc, context)
    
    # 기존 핸들러가 응답을 생성한 경우 그대로 반환
    if response is not None:
        return response
    
    # Django ValidationError 처리
    if isinstance(exc, DjangoValidationError):
        error_messages = exc.messages if hasattr(exc, 'messages') else [str(exc)]
        data = {'detail': error_messages}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    # 기타 예외의 경우 일반적인 500 에러 메시지 반환
    if isinstance(exc, Exception):
        data = {'detail': 'Internal server error'}
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # 처리되지 않은 예외는 None을 반환하여 Django의 기본 예외 처리로 위임
    return None 