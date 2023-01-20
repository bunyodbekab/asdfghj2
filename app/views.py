from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from app.bot import polToWebhook
@csrf_exempt
def webhook(request):
    polToWebhook(request)
    return JsonResponse({'message': 'OK'}, status=200)
