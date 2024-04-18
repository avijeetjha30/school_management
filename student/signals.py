from student.models import Student, StudentProfile
from django.db.models.signals import post_save


def on_create_student(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(student_id=instance)
        print("Student Profile is created")
    else:
        # if student is updated
        try:
            profile = StudentProfile.objects.get(student_id=instance)
            profile.save()
        except Exception as e:
            print(str(e))
            StudentProfile.objects.create(student_id=instance)
            print("User Profile is not exists but i created one")
        print("User profile updated")


post_save.connect(on_create_student, sender=Student)
