from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLoginSerializer, UserRegistrationSerializer
from rest_framework import generics
from rest_framework import permissions, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

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


def home(request):
    return render(request, 'home/home.html')


@csrf_exempt
def about(request):
        data = json.loads(request.body)
        api_key = data.get('API_KEY', 'No API_KEY found')
        return JsonResponse({'api_key': api_key,'data':data})
