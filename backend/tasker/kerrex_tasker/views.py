import json
from collections import OrderedDict

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import F, Max
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
    resource_name = 'permissions'
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class UserViewSet(viewsets.ModelViewSet):
    resource_name = 'users'
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    resource_name = 'categories'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        query = self.queryset
        if 'filter[project_id]' in self.request.query_params:
            project_id = self.request.query_params['filter[project_id]']
            query = query.filter(project=project_id)

        # TODO dopisać resztę filtrowania
        return query.order_by('order_in_project')

    def create(self, request, *args, **kwargs):
        new_data = request.data
        new_data['project'] = new_data['project']['id']
        new_order_in_project_dict = Category.objects.filter(project_id=new_data['project']) \
            .aggregate(Max('order_in_project'))
        new_order_in_project = new_order_in_project_dict['order_in_project__max'] + 1 \
            if new_order_in_project_dict['order_in_project__max'] is not None \
            else 0

        new_data['order_in_project'] = new_order_in_project
        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CardViewSet(viewsets.ModelViewSet):
    resource_name = 'cards'
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self):
        query = self.queryset
        for key in self.request.query_params.keys():
            print(key)
        if 'filter[category_id]' in self.request.query_params:
            category_id = self.request.query_params['filter[category_id]']
            query = query.filter(category_id=category_id)

        if 'filter[category_id][]' in self.request.query_params:
            category_ids = self.request.GET.getlist('filter[category_id][]')
            query = query.filter(category_id__in=category_ids)

        if 'filter[showOnCalendar]' in self.request.query_params:
            show_on_calendar = self.request.query_params['filter[showOnCalendar]'] == 'true'
            query = query.filter(show_on_calendar=show_on_calendar)

        if 'filter[calendarDateStart]' in self.request.query_params:
            calendar_date_start = self.request.query_params['filter[calendarDateStart]']
            if calendar_date_start == '':
                calendar_date_start = None
            query = query.filter(calendar_date_start=calendar_date_start)

        return query.order_by('order_in_category')

    def update(self, request, *args, **kwargs):
        user = request.user
        new_data = request.data

        # fix 'got OrderedDict instead of pk error'
        new_data['created_by'] = new_data['created_by']['id']
        new_data['modified_by'] = user.id
        new_data['category'] = new_data['category']['id']

        order_in_category = new_data['order_in_category']
        category = new_data['category']

        card_to_update = Card.objects.get(pk=new_data['id'])
        old_category = card_to_update.category_id
        old_order_in_category = card_to_update.order_in_category
        print(int(category) != int(old_category))
        changing_category = int(category) != int(old_category)
        if changing_category:
            # increment order for cards in new category
            Card.objects.filter(category_id=category, order_in_category__gte=order_in_category) \
                .update(order_in_category=F('order_in_category') + 1)
        else:
            card_to_update.order_in_category = -1
            card_to_update.save()
            Card.objects.filter(category_id=category, order_in_category__gt=old_order_in_category,
                                order_in_category__lte=order_in_category) \
                        .update(order_in_category=F('order_in_category') - 1)

        # perform actual update of card
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=new_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # decrement order for cards in old category
        if changing_category:
            Card.objects.filter(category_id=old_category, order_in_category__gt=old_order_in_category) \
                .update(order_in_category=F('order_in_category') - 1)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        new_data = request.data
        new_data['category'] = new_data['category']['id']
        category = new_data['category']
        order_in_category = new_data['order_in_category']
        new_data['created_by'] = request.user.id
        new_data['modified_by'] = request.user.id

        # increment order for cards in new category
        Card.objects.filter(category_id=category, order_in_category__gte=order_in_category) \
            .update(order_in_category=F('order_in_category') + 1)

        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
