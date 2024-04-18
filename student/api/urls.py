from django.urls import path
from student.api.views import *


urlpatterns = [
    path('student', StudentsAV.as_view(), name='students'),
    path('student/<str:uid>', StudentsAV.as_view(), name='student_view'),
    path('deactivate-student', DeactivateStudentsAV.as_view(), name='students'),
    path('profile-update/<str:uid>', UpdateProfileAV.as_view(), name='update_student_profile'),
    path('class', ClassAV.as_view(), name='class'),
    path('class/<str:uid>', ClassAV.as_view(), name='class_view'),
    path('login', LoginAV.as_view(), name='login'),
    path('logout', LogoutAV.as_view(), name='logout'),
    path('registration', RegistrationAV.as_view(), name='student_registration'),
    path('activate/<str:uid>', ActivateStudentAV.as_view(), name='activate_student'),
]
