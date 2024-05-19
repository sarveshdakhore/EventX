from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLoginSerializer, UserRegistrationSerializer, APIKeySerializer
from rest_framework import generics
from rest_framework import permissions, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import APIKey
from .decorators import api_key_required
from rest_framework.decorators import api_view
import time
import hashlib
import base64

# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        print(serializer.is_valid())
        
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            print(username, password)
            
            user = authenticate(request, username=username, password=password, user_type='club')
            print(user)
            
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIKeyGenerationView(APIView):
    # This class expects from frontend request, "Authorization": Token <token>
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = APIKeySerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            event_name = serializer.validated_data['event_name']

            # Check if an API key already exists for the given user, event_name, and non-null event_id
            existing_api_key = APIKey.objects.filter(user=user, event_name=event_name, event_id__isnull=False).first()

            if existing_api_key:
                return Response({'detail': 'API key already exists for this user and event.'}, status=status.HTTP_400_BAD_REQUEST)

            api_key_obj = APIKey(user=user, event_name=event_name)
            
            timestamp = int(time.time())
            unique_identifier = f"{user.username}-{api_key_obj.event_id}-{event_name}-{timestamp}"
            hashed_value = hashlib.sha256(unique_identifier.encode()).digest()
            api_key = base64.b64encode(hashed_value).decode()

            api_key_obj.api_key = api_key
            api_key_obj.save()

            return Response({'api_key': api_key, 'event_id': api_key_obj.event_id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_key_required
@api_view(['GET'])
def check_api_key(request):
    return JsonResponse({ "message": "Valid"})


def home(request):
    return render(request, 'home/home.html')


@csrf_exempt
def about(request):
        data = json.loads(request.body)
        api_key = data.get('API_KEY', 'No API_KEY found')
        return JsonResponse({'api_key': api_key,'data':data})
