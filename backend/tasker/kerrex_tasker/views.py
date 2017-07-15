import json
from collections import OrderedDict

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from kerrex_tasker.forms import RegistrationForm
from kerrex_tasker.models import Project, Permission, Category, Card
from kerrex_tasker.serializers import ProjectSerializer, PermissionSerializer, UserSerializer, CategorySerializer, \
    CardSerializer


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


class ProjectViewSet(viewsets.ModelViewSet):
    resource_name = 'projects'
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(owner=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        new_data = request.data
        owner_dict = OrderedDict()
        owner_dict['type'] = 'Users'
        owner_dict['id'] = user.id
        new_data['owner'] = owner_dict

        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        query = self.queryset
        if 'filter[project_id]' in self.request.query_params:
            project_id = self.request.query_params['filter[project_id]']
            query.filter(project=project_id)

        #TODO dopisać resztę filtrowania
        return query


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
