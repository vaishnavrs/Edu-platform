from django.contrib.auth.backends import ModelBackend,BaseBackend
from django.contrib.auth.models import User
from .models import Student,Faculty

        
class StudentBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f"Authenticating student with username: {username}")
        try:
            student = Student.objects.get(username=username)
            print(f"Student found: {student.name}")
            if student.check_password(password):
                print("Password is correct")
                return student
            else:
                print("Password is incorrect")
        except Student.DoesNotExist:
            print(f"No student found with username: {username}")
            return None

    def get_user(self, user_id):
        print(f"Getting student with ID: {user_id}")
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            print(f"No student found with ID: {user_id}")
            return None

        

class FacultyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            faculty = Faculty.objects.get(username=username)
            if faculty.check_password(password):
                return faculty
        except Faculty.DoesNotExist:
            return None