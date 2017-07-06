import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from kerrex_tasker.forms import RegistrationForm


@require_http_methods(["POST"])
@csrf_exempt
def register(request):
    """
    API endpoint to register a new user.
    """
    try:
        payload = json.loads(request.body)
    except ValueError:
        return JsonResponse({"error": "Unable to parse request body"}, status=400)

    form = RegistrationForm(payload)

    if form.is_valid():
        user = User.objects.create_user(form.cleaned_data["username"],
                                        form.cleaned_data["email"],
                                        form.cleaned_data["password"])
        user.save()

        return JsonResponse({"success": "User registered."}, status=201)

    return HttpResponse(form.errors.as_json(), status=400, content_type="application/json")