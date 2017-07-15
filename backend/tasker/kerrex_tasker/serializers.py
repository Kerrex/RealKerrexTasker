from django.contrib.auth.models import User
from rest_framework import serializers, viewsets

from kerrex_tasker.models import Project, Category, Card, CardComment, Permission
from rest_framework_json_api.relations import ResourceRelatedField


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'description', 'date_created', 'last_modified', 'owner', 'default_permission')

    owner = ResourceRelatedField(
        queryset=User.objects
    )
    default_permission = ResourceRelatedField(
        queryset=Permission.objects
    )


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'description')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        many = True
        model = Category
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        many = True
        model = Card
        fields = '__all__'


class CardCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardComment
        fields = ('content', 'date_created', 'last_modified', 'created_by', 'card')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)



