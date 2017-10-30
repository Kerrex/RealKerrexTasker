import json
from collections import OrderedDict

from django.contrib.auth.models import User
from django.db.models import F, Max, Q
import datetime
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseForbidden
from django.utils import timezone

# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from pywebpush import webpush, WebPushException
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from kerrex_tasker.filters import UserCardNotificationFilter, UserFilter, CategoryFilter, CardFilter
from kerrex_tasker.forms import RegistrationForm
from kerrex_tasker.models import Project, Permission, Category, Card, UserProjectPermission, Priority, UserNotification, \
    UserCardNotification
from kerrex_tasker.permissions import has_permissions, is_user_blocked, allowed_by_default_permission, \
    get_filter_params_for_available_project_query, has_permission_to_edit
from kerrex_tasker.serializers import ProjectSerializer, PermissionSerializer, UserSerializer, CategorySerializer, \
    CardSerializer, UserProjectPermissionSerializer, PrioritySerializer, UserCardNotificationSerializer
from kerrex_tasker.services.web_push_service import WebPushService


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


@require_http_methods(["POST"])
@csrf_exempt
def has_permission(request):
    project_id = request.body
    token = request.META['HTTP_AUTHORIZATION'].replace('Token ', '')
    user = Token.objects.filter(key=token).first().user
    project = Project.objects.get(pk=project_id)
    if has_permission_to_edit(project, user):
        return HttpResponse('True')
    else:
        return HttpResponseForbidden('False')


@require_http_methods(["POST"])
@csrf_exempt
def register_service_worker(request):
    json_body = json.loads(request.body)
    if 'token' not in json_body or 'subscription_id' not in json_body:
        return JsonResponse({"error": "Unable to parse request body"}, status=400)

    user = Token.objects.filter(key=json_body['token']).first().user

    existing_subscription = UserNotification.objects.filter(user=user,
                                                            subscription_id=json_body['subscription_id']).first()
    if existing_subscription is not None:
        existing_subscription.subscription_id = json_body['subscription_id']
    else:
        existing_subscription = UserNotification()
        existing_subscription.user = user
        existing_subscription.subscription_id = json_body['subscription_id']

    existing_subscription.save()

    return HttpResponse('OK')


class NotifyView(View):
    push_service = WebPushService()

    @csrf_exempt
    def post(self, request):
        for card_notification in UserCardNotification.objects.all():
            user = card_notification.user
            if self.push_service.is_eliglble_for_push(card_notification):
                user_notification_devices = UserNotification.objects.filter(user=user)

                for device in user_notification_devices:
                    result = self.push_service.send_push(device.subscription_id, card_notification)
                    if not result:
                        device.delete()
                card_notification.delete()

        return HttpResponse("OK")


# TODO do przetestowania w następnej kolejności
class UserCardNotificationViewSet(viewsets.ModelViewSet):
    resource_name = 'userCardNotifications'
    queryset = UserCardNotification.objects.all()
    serializer_class = UserCardNotificationSerializer
    pagination_class = None

    def get_queryset(self):
        query_filter = UserCardNotificationFilter(self.queryset, self.request.user)
        return query_filter.filter(self.request.query_params)

    def create(self, request, *args, **kwargs):
        new_data = request.data

        new_data['user'] = request.user.id
        new_data['card'] = new_data['card']['id']

        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectViewSet(viewsets.ModelViewSet):
    resource_name = 'projects'
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.filter_queryset(self.get_queryset()).filter(get_filter_params_for_available_project_query(user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if has_permissions(instance.id, request.user):
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            raise Http404

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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if not has_permission_to_edit(instance, request.user):
            return HttpResponseForbidden("No permission to edit that project")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    resource_name = 'permissions'
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class UserViewSet(viewsets.ModelViewSet):
    resource_name = 'users'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user_filter = UserFilter(self.queryset)
        return user_filter.filter(self.request.query_params)


class CategoryViewSet(viewsets.ModelViewSet):
    resource_name = 'categories'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        query = self.queryset
        cat_filter = CategoryFilter(query)
        query = cat_filter.filter(self.request.query_params)

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

# TODO filtrowanka wydzielić do oddzielnej klasy z jakimiś stałymi, itd
class CardViewSet(viewsets.ModelViewSet):
    resource_name = 'cards'
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self):
        query = self.queryset
        card_filter = CardFilter(query)
        return card_filter.filter(query).order_by('order_in_category')

    # TODO Podzielić i to przetestować jakoś
    def update(self, request, *args, **kwargs):
        user = request.user
        print(request.body)
        new_data = request.data

        # fix 'got OrderedDict instead of pk error'
        self.fix_got_ordered_dict_instead_of_pk_error(new_data, user)

        order_in_category = new_data['order_in_category']
        category = new_data['category']

        # sprawdzanie czy order i kategoria się w ogole zmienily
        card_to_update = Card.objects.get(pk=new_data['id'])
        old_category = card_to_update.category_id
        old_order_in_category = card_to_update.order_in_category
        changing_category = int(category) != int(old_category)
        changing_order = int(order_in_category) != int(old_order_in_category)
        if changing_category:
            # increment order for cards in new category
            self.increment_order_for_new_category(category, order_in_category)
        elif not changing_category and changing_order:
            self.move_in_same_category(card_to_update, category, old_order_in_category, order_in_category)

        self.verify_and_correct_dates(new_data)

        # perform actual update of card
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=new_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # decrement order for cards in old category
        if changing_category:
            self.decrement_order_for_old_category(old_category, old_order_in_category)

        return Response(serializer.data)

    @staticmethod
    def verify_and_correct_dates(new_data):
        if new_data['calendar_date_start'] == 'Invalid date':
            new_data['calendar_date_start'] = None
        if new_data['calendar_date_end'] == 'Invalid date':
            new_data['calendar_date_end'] = None

    @staticmethod
    def fix_got_ordered_dict_instead_of_pk_error(new_data, user):
        new_data['created_by'] = new_data['created_by']['id']
        new_data['modified_by'] = user.id
        new_data['category'] = new_data['category']['id']
        new_data['priority'] = new_data['priority']['id'] if new_data['priority'] is not None else None

    @staticmethod
    def decrement_order_for_old_category(old_category, old_order_in_category):
        cards = Card.objects.filter(category_id=old_category, order_in_category__gt=old_order_in_category) \
            .order_by('order_in_category')
        for card in cards:
            card.order_in_category = card.order_in_category - 1
            card.save()

    @staticmethod
    def increment_order_for_new_category(category, order_in_category):
        cards = Card.objects.filter(category_id=category, order_in_category__gte=order_in_category) \
            .order_by('-order_in_category')
        for card in cards:
            card.order_in_category = card.order_in_category + 1
            card.save()

    @staticmethod
    def move_in_same_category(card_to_update, category, old_order_in_category, order_in_category):
        card_to_update.order_in_category = -1
        card_to_update.save()
        is_raising = order_in_category > old_order_in_category
        between_touple = ((old_order_in_category, order_in_category) if is_raising
                          else (order_in_category, old_order_in_category))
        order_by = 'order_in_category' if is_raising else '-order_in_category'
        cards_to_move = Card.objects.filter(category_id=category, order_in_category__range=between_touple) \
            .order_by(order_by)
        for card in cards_to_move:
            card.order_in_category = card.order_in_category + (1 if not is_raising else -1)
            card.save()
        card_to_update.order_in_category = order_in_category
        card_to_update.save()

    def create(self, request, *args, **kwargs):
        new_data = request.data
        new_data['category'] = new_data['category']['id']
        category = new_data['category']
        order_in_category = new_data['order_in_category']
        new_data['created_by'] = request.user.id
        new_data['modified_by'] = request.user.id
        new_data['calendar_date_start'] = None
        new_data['calendar_date_end'] = None

        if not Category.objects.filter(id=category).exists():
            return HttpResponseForbidden('You cant edit that project!!')

        project = Category.objects.get(pk=category).project
        if not has_permission_to_edit(project, request.user):
            return HttpResponseForbidden('You cant edit that project!!')

        self.increment_order_for_new_category(category, order_in_category)
        # increment order for cards in new category
        #Card.objects.filter(category_id=category, order_in_category__gte=order_in_category) \
        #    .update(order_in_category=F('order_in_category') + 1)

        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserProjectPermissionViewSet(viewsets.ModelViewSet):
    resource_name = 'userProjectPermissions'
    queryset = UserProjectPermission.objects.all()
    serializer_class = UserProjectPermissionSerializer
    pagination_class = None

    def get_queryset(self):
        query = self.queryset
        if 'filter[project_id]' in self.request.query_params:
            project_id = self.request.query_params['filter[project_id]']
            query = query.filter(project_id=project_id)

        return query

    def create(self, request, *args, **kwargs):
        new_data = request.data
        print(new_data['user'])
        new_data['user'] = new_data['user']['id']
        new_data['project'] = new_data['project']['id']
        new_data['permission'] = 1
        new_data['given_by'] = request.user.id

        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        new_data = request.data
        new_data['user'] = new_data['user']['id']
        new_data['project'] = new_data['project']['id']
        new_data['permission'] = new_data['permission']['id']
        new_data['given_by'] = request.user.id

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=new_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class PriorityViewSet(viewsets.ModelViewSet):
    resource_name = 'priorities'
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    pagination_class = None
