from typing import Any
from django import forms
from accounts.models import Faculty,Course,Video,CourseModule
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.hashers import make_password






class FacultyRegForm(UserCreationForm):
    class Meta:
        model = Faculty
        fields = ['username','name', 'emailid', 'address', 'qualification', 'subject', 'password1', 'password2']
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'emailid': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email id'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'qualification': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Qualification'}),
            'subject': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
    def __init__(self, *args, **kwargs):
        super(FacultyRegForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['placeholder'] = 'confirm password'



class FacultyLoginForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control',
                                                                            'placeholder':'username'}))
    
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                                 'placeholder':'password'}))



class CourseForm1(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control', 
                                                  'placeholder': '   e.g .Learn From scratch '})
        }

class CourseForm2(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'})
        }
        
class CourseForm3(forms.ModelForm):
    class Meta:
        model = Course
        fields = [ 'course_desc', 'syllabus','course_duration','course_fee','course_image']
        widgets = {

            'course_desc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe Your Courese'}),
            'syllabus': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Syllabus'}),
            'course_duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Duration'}),
            'course_fee': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Fee'}),
            'course_image': forms.FileInput(attrs={'class': 'form-control-file border'})
        }

class CourseDescrptionEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_desc']
        widgets = {
            'course_desc': forms.Textarea(attrs={'class': 'form-control'})
        }

class CourseSyllabusEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['syllabus']
        widgets = {
            'syllabus': forms.Textarea(attrs={'class': 'form-control'})
        }


class CourseModuleForm(forms.ModelForm):
    class Meta:
        model = CourseModule
        fields = ['module_name']
        widgets = {
            'module_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'e.g. Introduction'})
        }


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title','video']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'video': forms.FileInput(attrs={'class': 'form-control-file border'})
        }
