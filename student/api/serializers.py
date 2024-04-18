from rest_framework import serializers
from django.contrib.auth.hashers import check_password, make_password
from student.models import *
from helper.utility import validate_name, validate_number


# class list
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


# register student
class RegistrationSerializers(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, validators=validate_name())
    last_name = serializers.CharField(required=True, validators=validate_name())
    phone_number = serializers.CharField(required=True, validators=validate_number())
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'class_id', 'password', 'confirm_password')

    def validate(self, validated_data):
        data = super().validate(validated_data)
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password doesn't match...!")
        data['password'] = make_password(data['password'])
        data.pop('confirm_password')
        return data


# login
class LoginSerializers(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, validated_data):
        data = super().validate(validated_data)
        user = Student.objects.filter(phone_number=data['phone_number']).first()
        if not user:
            raise serializers.ValidationError('Invalid credential...!')
        if not user.is_active:
            raise serializers.ValidationError('You have to activate your account first check your phone number...!')
        if not check_password(data['password'], user.password):
            raise serializers.ValidationError('You enter wrong password...!')
        return data


# student list
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


# update student
class UpdateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('email', 'phone_number', 'updated_at')


# update profile
class UpdateStudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('profile_picture', 'address', 'country', 'state', 'city', 'zipcode', 'updated_at')


# Student detail list
class StudentDetailSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    class_id = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    zipcode = serializers.CharField(required=False)
    profile_picture = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    created_at = serializers.CharField(required=False)
    updated_at = serializers.CharField(required=False)
