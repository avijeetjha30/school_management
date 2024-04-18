from django.core.management.base import BaseCommand
from student.models import Student, StudentProfile
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Seed the User table for creating a superuser'

    def handle(self, *args, **kwargs):
        student_data = {
            'password': make_password('qwerty@123'),
            'first_name': 'admin',
            'last_name': 'aklkl',
            'username': 'admin',
            'email': "admin@smanagement.com",
            'phone_number': '+911234567890',
            'is_active': True,
            'is_admin': True,
            'is_staff': True,
            'is_superadmin': True,
        }

        Student.objects.create(**student_data)

        student_profile_data = {
            'student_id': Student.objects.get(email=student_data['email']),
            'address': 'Noida',
            'city': 'Noida',
            'state': 'Utter Pradesh',
            'country': 'India',
            'zipcode': '2030306',
        }

        StudentProfile.objects.create(**student_profile_data)
        print(f"Super User '{student_data['first_name']} {student_data['last_name']} ({student_data['email']})' created.")
