from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse

def sample_get_api(request):
    if request.method == "GET":
        data = {
            "message": "Hello, this is a simple GET API!",
            "status": "success"
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)