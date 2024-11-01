from django.urls import path
from .views import *
urlpatterns = [
    path('facultyhome/', FacultyHomeView.as_view(), name='faculty_home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('login/',FacultyLoginView.as_view(),name='login'),
    path('addcourse/',AddCourseView1.as_view(),name='add_course'),
    path('addcourse1/',AddCourseView2.as_view(),name='add_course_2'),
    path('addcoursefinal/',AddCourseView3.as_view(),name='add_course_3'),
    path('detail/<int:id>/',DetailView.as_view(),name='detail'),
    path('update/<int:id>/',DescriptionUpdateView.as_view(),name='update_desc'),
    path('update/syllabus/<int:id>/',SyllabusEditView.as_view(),name='update_syllabus'),
    path('module/add/<int:id>/',ModuleCreationView.as_view(),name='create_form'),
    path('module/video/<int:id>/',VideoUploadingView.as_view(),name='video')


]