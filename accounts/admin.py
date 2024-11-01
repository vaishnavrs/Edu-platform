from django.contrib import admin
from accounts.models import Faculty,Course,CourseModule,Video,Student,Cart
# Register your models here.
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(CourseModule)
admin.site.register(Video)
admin.site.register(Student)
admin.site.register(Cart)