from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    TimetableEntry,
    AcademicCalendar,
    Holiday,
    AttendanceRule
)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Django's built-in User model.
    Includes a create method to handle password hashing
    if you want to allow user registration via API.
    """
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }

    def create(self, validated_data):
        # Use Django's create_user to handle password hashing
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class TimetableEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetableEntry
        fields = '__all__'
        read_only_fields = ['user']


class AcademicCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicCalendar
        fields = '__all__'
        read_only_fields = ['user']


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'
        read_only_fields = ['user']


class AttendanceRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRule
        fields = '__all__'
        read_only_fields = ['user']
