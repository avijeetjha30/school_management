from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.db.models import F
from django.db import transaction
# -----------------------------------------------------------------------
from helper.generate_token import GenerateToken, redis_client
from helper.utility import api_response
from student.models import Student
from student.api.serializers import *


# Class Create
class ClassAV(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClassSerializer

    def get(self, request, uid=None):
        if uid:
            c_data = Class.objects.filter(id=uid)
        else:
            c_data = Class.objects.all()
        serialized_data = self.serializer_class(c_data, many=True)
        api_response_data = {'data': serialized_data.data, 'message': 'Class Created.', 'status_code': status.HTTP_200_OK, 'success': True}
        return Response(api_response(**api_response_data), status=api_response_data.get('status_code'))

    def post(self, request):
        try:
            token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
            token = AccessToken(token)
            if token.payload['email'] == 'admin@smanagement.com':
                if Class.objects.filter(name=request.data['name']).exists():
                    api_response_data = {'data': None, 'message': 'Class already created.', 'status_code': status.HTTP_200_OK, 'success': True}
                else:
                    Class.objects.create(name=request.data['name'])
                    api_response_data = {'data': None, 'message': 'Class Created.', 'status_code': status.HTTP_200_OK, 'success': True}
            else:
                api_response_data = {'data': None, 'message': "Only admin can create class.", 'status_code': status.HTTP_400_BAD_REQUEST, 'success': False} # noqa
        except Exception as e:
            api_response_data = {'data': None, 'message': str(e), 'status_code': status.HTTP_400_BAD_REQUEST, 'success': False}
        return Response(api_response(**api_response_data), status=api_response_data.get('status_code'))


# Student registration
class RegistrationAV(GenericAPIView):
    serializer_class = RegistrationSerializers

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            serialized_data.save()
            api_response_data = {'data': None, 'message': 'Your Registration is successfull', 'status_code': status.HTTP_200_OK, 'success': True} # noqa
        else:
            api_response_data = {'data': None, 'message': serialized_data.errors, 'status_code': status.HTTP_400_BAD_REQUEST, 'success': False}

        return Response(api_response(**api_response_data), status=api_response_data.get('status_code'))


# Activate account by admin
class ActivateStudentAV(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, uid):
        try:
            Student.objects.filter(id=uid).update(is_active=True)
            api_response_data = {'data': None, 'message': 'Student is activated now', 'status_code': status.HTTP_200_OK, 'success': True} # noqa
        except Exception as e:
            api_response_data = {'data': None, 'message': str(e), 'status_code': status.HTTP_400_BAD_REQUEST, 'success': False}

        return Response(api_response(**api_response_data), status=api_response_data.get('status_code'))


# Login student
class LoginAV(GenericAPIView):
    serializer_class = LoginSerializers

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            user = Student.objects.get(phone_number=serialized_data.data.get('phone_number'))
            token = GenerateToken()
            api_response_data = {'data': token.get_token(user), 'message': 'You are are logged in...!', 'status_code': status.HTTP_200_OK, 'success': True} # noqa
        else:
            api_response_data = {'data': None, 'message': serialized_data.errors, 'status_code': status.HTTP_400_BAD_REQUEST, 'success': False}
        return Response(api_response(**api_response_data), status=api_response_data.get('status_code'))


# Logout user with blacklist refresh and access token
class LogoutAV(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            token = AccessToken(token)
            jti = token.payload['jti']
            redis_client.srem(f"user_{token.payload['email']}", jti)
            token = RefreshToken(request.META.get('HTTP_REFRESH_TOKEN'))
            token.blacklist()
            api_response_data = {'data': None, 'message': 'you are logged out...!', 'status_code': status.HTTP_200_OK, 'success': True}
        except Exception as e:
            api_response_data = {'data': None, 'message': str(e), 'status_code': status.HTTP_404_NOT_FOUND, 'success': False}
        response_data = api_response(**api_response_data)
        return Response(response_data, status=api_response_data['status_code'])


# student listing
class StudentsAV(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentSerializer

    def get(self, request, uid=None):
        token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        token = AccessToken(token)
        if token.payload['email'] == 'admin@smanagement.com':
            if uid:
                s_data = StudentProfile.objects.filter(student_id=uid).select_related(
                    'student_id',
                ).values(
                    'id', 'profile_picture', 'address', 'country', 'state', 'city', 'zipcode', 'created_at', 'updated_at'
                ).annotate(
                    first_name=F('student_id__first_name'), last_name=F('student_id__last_name'), username=F('student_id__username'), email=F('student_id__email'), phone_number=F('student_id__phone_number'), class_id=F('student_id__class_id'), is_active=F('student_id__is_active') # noqa
                )
                serialized_data = StudentDetailSerializer(s_data, many=True)
            else:
                s_data = Student.objects.all()
                serialized_data = self.serializer_class(s_data, many=True)
        else:
            s_data = StudentProfile.objects.filter(student_id__id=token.payload['id']).select_related(
                'student_id',
            ).values(
                'id', 'profile_picture', 'address', 'country', 'state', 'city', 'zipcode', 'created_at', 'updated_at'
            ).annotate(
                first_name=F('student_id__first_name'), last_name=F('student_id__last_name'), username=F('student_id__username'), email=F('student_id__email'), phone_number=F('student_id__phone_number'), class_id=F('student_id__class_id'), is_active=F('student_id__is_active') # noqa
            )
            serialized_data = StudentDetailSerializer(s_data, many=True)

        api_response_data = {'data': serialized_data.data, 'message': 'Data fetched.', 'status_code': status.HTTP_200_OK, 'success': True}

        return Response(api_response(**api_response_data), status=api_response_data.get('status_code'))


# deactivate student listing
class DeactivateStudentsAV(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentSerializer

    def get(self, request, uid=None):
        token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        token = AccessToken(token)
        if token.payload['email'] == 'admin@smanagement.com':
            s_data = Student.objects.filter(is_active=False)
            serialized_data = self.serializer_class(s_data, many=True)
            api_response_data = {'data': serialized_data.data, 'message': 'Data fetched.', 'status_code': status.HTTP_200_OK, 'success': True}
        else:
            api_response_data = {'data': None, 'message': "Only admin fetch data.", 'status_code': status.HTTP_400_BAD_REQUEST, 'success': False} # noqa
        return Response(api_response(**api_response_data), status=api_response_data.get('status_code'))


# update profile
class UpdateProfileAV(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, uid=None):
        token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        token = AccessToken(token)
        if token.payload.get('email') != 'admin@smanagement.com':
            uid = token.payload.get('id')
        data = request.data
        if data:
            with transaction.atomic():
                try:
                    serialized_data = UpdateStudentSerializer(data=request.data)
                    if serialized_data.is_valid(raise_exception=True):
                        Student.objects.filter(id=uid).update(**serialized_data.data)
                    serialized_data = UpdateStudentProfileSerializer(data=request.data)
                    if serialized_data.is_valid(raise_exception=True):
                        data = serialized_data.data
                        data['profile_picture'] = request.FILES.get('profile_picture')
                        StudentProfile.objects.filter(student_id=uid).update(**data)
                    api_response_data = {'data': None, 'message': "Student profile updated", 'status_code': status.HTTP_200_OK, 'success': True}
                except Exception as e:
                    print("************", str(e))
                    transaction.set_rollback(True)
                    api_response_data = {'data': None, 'message': serialized_data.errors, 'status_code': status.HTTP_400_BAD_REQUEST, 'success': False} # noqa
        return Response(api_response(**api_response_data), status=api_response_data.get('status_code'))
