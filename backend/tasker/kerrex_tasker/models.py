from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# Dict tables
class Permission(models.Model):
    name = models.CharField(max_length=25, null=False)
    description = models.CharField(max_length=255, null=False)


class Priority(models.Model):
    name = models.CharField(max_length=25, null=False)


# Non-dict tables
class Project(models.Model):
    name = models.CharField(max_length=24, null=False)
    description = models.CharField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    last_modified = models.DateTimeField(auto_now=True, null=False)
    default_permission = models.ForeignKey(Permission, on_delete=models.CASCADE, null=False)
    owner = models.ForeignKey(User, null=False)

    def __str__(self):
        return '{0} - {1}'.format(self.name, self.owner.username)

    class JSONAPIMeta:
        resource_name = 'project'


class UserProjectPermission(models.Model):
    given_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='given_by')
    permission = models.ForeignKey(Permission, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        unique_together = ('project', 'user')

    class JSONAPIMeta:
        resource_name = 'user_project_permission'


class Category(models.Model):
    name = models.CharField(max_length=24, null=False)
    order_in_project = models.IntegerField(null=False)
    project = models.ForeignKey(Project, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}, no. {1}'.format(self.name, self.order_in_project)

    class JSONAPIMeta:
        resource_name = 'category'

    class Meta:
        unique_together = ('project', 'order_in_project')


class Card(models.Model):
    name = models.CharField(max_length=24)
    description = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, models.SET_NULL, null=True, related_name='created_by')
    modified_by = models.ForeignKey(User, models.SET_NULL, null=True, related_name='modified_by')
    priority = models.ForeignKey(Priority, null=True)
    category = models.ForeignKey(Category, null=False)
    order_in_category = models.IntegerField(null=False)
    calendar_date_start = models.DateTimeField(null=True, blank=True, auto_now=False)
    calendar_date_end = models.DateTimeField(null=True, blank=True, auto_now=False)
    show_on_calendar = models.BooleanField(default=False)

    class JSONAPIMeta:
        resource_name = 'card'

    class Meta:
        unique_together = ('order_in_category', 'category')


class CardComment(models.Model):
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    class JSONAPIMeta:
        resource_name = 'card_comment'
