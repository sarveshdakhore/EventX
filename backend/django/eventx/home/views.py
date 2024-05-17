from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def home(request):
    return render(request, 'home/home.html')


@csrf_exempt
def about(request):
        data = json.loads(request.body)
        api_key = data.get('API_KEY', 'No API_KEY found')
        return JsonResponse({'api_key': api_key,'data':data})
