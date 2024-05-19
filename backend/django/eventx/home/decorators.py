from rest_framework.response import Response
from rest_framework import status
from .utils import validate_api_key

def api_key_required(func):
    def wrapper(request, *args, **kwargs):
        api_key = request.headers.get('API-KEY')
        if not api_key or not validate_api_key(api_key):
            return Response({'detail': 'Invalid API key.'}, status=status.HTTP_403_FORBIDDEN)
        return func(request, *args, **kwargs)
    return wrapper