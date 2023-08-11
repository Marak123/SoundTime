from django.contrib.auth.models import Permission
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404

from .models import User, Group

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'created', 'updated']
        read_only_field = ['is_active', 'created', 'updated']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializerField(serializers.CharField):
    def to_representation(self, value):
        # For GET requests, return the object representation of the field
        return UserSerializer(value).data

    def to_internal_value(self, data):
        # For POST requests, return the string value of the field
        return data

class GroupSerializer(serializers.ModelSerializer):
    is_admin = UserSerializerField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions', 'is_admin']
        depth = 1

    def create(self, validated_data):
        validated_data['is_admin'] = User.objects.get(pk=validated_data['is_admin'])
        group = Group.objects.create(**validated_data)
        group.save()

        return group