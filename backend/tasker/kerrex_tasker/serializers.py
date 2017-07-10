from django.contrib.auth.models import User
from rest_framework import serializers, viewsets

from kerrex_tasker.models import Project, Category, Card, CardComment, Permission


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'description', 'date_created', 'last_modified', 'owner', 'default_permission')


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'description')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'order_in_project', 'project')


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('name', 'description', 'date_created', 'last_modified',
                  'created_by', 'modified_by', 'priority', 'category')


class CardCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardComment
        fields = ('content', 'date_created', 'last_modified', 'created_by', 'card')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)



