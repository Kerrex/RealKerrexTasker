import json
from collections import OrderedDict

from django.contrib.auth.models import User
from django.db.models import F, Max, Q
import datetime
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseForbidden
from django.utils import timezone

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from pywebpush import webpush, WebPushException
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from kerrex_tasker.forms import RegistrationForm
from kerrex_tasker.models import Project, Permission, Category, Card, UserProjectPermission, Priority, UserNotification, \
    UserCardNotification
from kerrex_tasker.serializers import ProjectSerializer, PermissionSerializer, UserSerializer, CategorySerializer, \
    CardSerializer, UserProjectPermissionSerializer, PrioritySerializer, UserCardNotificationSerializer


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

    project = Project.objects.get(id=project_id)
    has_permissions = UserProjectPermission.objects.filter(
        Q(project_id=project_id) & Q(user_id=request.user.id) & (Q(permission_id=1) | Q(permission_id=3))).exists()

    is_user_blocked = UserProjectPermission.objects.filter(project_id=project_id, user_id=request.user.id,
                                                           permission_id=4)
    default_permission_allows = project.default_permission_id == 1 or project.default_permission_id == 3
    print(default_permission_allows)
    if project.owner.id == request.user.id or (
                default_permission_allows and not is_user_blocked) or has_permissions:
        print(True)
        return HttpResponse('True')
    else:
        return HttpResponseForbidden('False')


@require_http_methods(["POST"])
@csrf_exempt
def register_service_worker(request):
    json_body = json.loads(request.body)
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


@require_http_methods(["POST"])
@csrf_exempt
def notify(request):
    for card_notification in UserCardNotification.objects.all():
        now = timezone.now()
        card = card_notification.card
        user = card_notification.user
        minutes_before_start = datetime.timedelta(minutes=card_notification.minutes_before_start)
        date_start = card.calendar_date_start

        if date_start is None:
            continue

        if (now + minutes_before_start) > card.calendar_date_start or card.calendar_date_start < now:
            user_notification_devices = UserNotification.objects.filter(user=user)
            for device in user_notification_devices:
                subscription_info = json.loads(device.subscription_id)
                data = "{} starts in {} minutes!".format(card.name, card_notification.minutes_before_start)
                private_key = "nhUMvSrk-65JBY8ExLPvnGnLD_JrtWeSTxgdfJxsnd0"
                claims = {"sub": "mailto:romen3@gmail.com"}
                try:
                    webpush(subscription_info, data, vapid_private_key=private_key, vapid_claims=claims)
                except WebPushException:
                    print("Endpoint not registered! Removing")
                    device.delete()
            card_notification.delete()

    return HttpResponse("OK")


class UserCardNotificationViewSet(viewsets.ModelViewSet):
    resource_name = 'userCardNotifications'
    queryset = UserCardNotification.objects.all()
    serializer_class = UserCardNotificationSerializer
    pagination_class = None

    def get_queryset(self):
        query = self.queryset
        user = self.request.user
        if 'filter[card_id]' in self.request.query_params:
            card_id = self.request.query_params['filter[card_id]']
            query = query.filter(card_id=card_id, user=user)

        return query

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
        queryset = self.filter_queryset(self.get_queryset()).filter(Q(owner=user)
                                                                    | (Q(userprojectpermission__user=user)
                                                                       & Q(
            userprojectpermission__permission_id__in=[1, 3])))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        has_permissions = UserProjectPermission.objects.filter(
            Q(project=instance) & Q(user_id=request.user.id) & (Q(permission_id=1) | Q(permission_id=3))).exists()

        is_user_blocked = UserProjectPermission.objects.filter(project=instance, user_id=request.user.id,
                                                               permission_id=4)
        default_permission_allows = instance.default_permission_id == 1 or instance.default_permission_id == 3
        print(default_permission_allows)
        if instance.owner.id == request.user.id or (
                    default_permission_allows and not is_user_blocked) or has_permissions:
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
        default_edit_permission = instance.default_permission_id == 1
        is_blocked = UserProjectPermission.objects.filter(project=instance, user_id=request.user.id,
                                                          permission_id=4).exists()
        has_permission_to_edit = UserProjectPermission.objects.filter(project=instance, user_id=request.user.id,
                                                                      permission_id=1).exists()
        if (not default_edit_permission and not has_permission_to_edit) or (default_edit_permission and is_blocked):
            return HttpResponseForbidden("No permission to edit that project");

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
        query = self.queryset
        if 'filter[usernameOrEmail]' in self.request.query_params:
            username_or_email = self.request.query_params['filter[usernameOrEmail]']
            query = query.filter(Q(username=username_or_email) | Q(email=username_or_email))

        return query


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
        print(request.body)
        new_data = request.data

        # fix 'got OrderedDict instead of pk error'
        new_data['created_by'] = new_data['created_by']['id']
        new_data['modified_by'] = user.id
        new_data['category'] = new_data['category']['id']
        new_data['priority'] = new_data['priority']['id'] if new_data['priority'] is not None else None

        order_in_category = new_data['order_in_category']
        category = new_data['category']
        print(new_data)
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

        if new_data['calendar_date_start'] == 'Invalid date':
            new_data['calendar_date_start'] = None
        if new_data['calendar_date_end'] == 'Invalid date':
            new_data['calendar_date_end'] = None

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

    def decrement_order_for_old_category(self, old_category, old_order_in_category):
        cards = Card.objects.filter(category_id=old_category, order_in_category__gt=old_order_in_category) \
            .order_by('order_in_category')
        for card in cards:
            card.order_in_category = card.order_in_category - 1
            card.save()

    def increment_order_for_new_category(self, category, order_in_category):
        cards = Card.objects.filter(category_id=category, order_in_category__gte=order_in_category) \
            .order_by('-order_in_category')
        for card in cards:
            card.order_in_category = card.order_in_category + 1
            card.save()

    def move_in_same_category(self, card_to_update, category, old_order_in_category, order_in_category):
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
