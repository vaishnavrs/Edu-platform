from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views.generic import View
from .forms import FacultyRegForm,FacultyLoginForm,CourseForm1,CourseForm3,CourseForm2,CourseDescrptionEditForm,CourseSyllabusEditForm,CourseModuleForm,VideoForm
from accounts.models import Faculty,Course,CourseModule,Video
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

class FacultyHomeView(View):
    def get(self,request): 
        form = FacultyRegForm()
        log_form = FacultyLoginForm()
        return render(request,'facultyhome.html',{'form':form,'log_form':log_form})
        
     
    def post(self, request):
        form = FacultyRegForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'facultyhome.html', {'form': form})


class FacultyLoginView(View):

    def post(self, request):
        form = FacultyLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password,backends ='accounts.FacultyBackend')
            if user is not None:
                if user.user_type == 'teacher':
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return render(request, 'facultyhome.html', {'log_form': form})
            else:
                form.add_error(None, 'Invalid username or password')
                return render(request, 'facultyhome.html', {'log_form': form})
        else:
            return render(request, 'facultyhome.html', {'log_form': form})

        

class DashboardView(View):
    def get(self,request):
        if request.user.is_authenticated:
            courses = Course.objects.filter(faculty = self.request.user)
            name =request.user.name
            name = name[0:2]
            context = {
                'name': name,
                'courses': courses
            }
        return render(request,'dashboard.html',context)
    

class AddCourseView1(View):

    def get(self, request):
        if request.user:
            form = CourseForm1()
            return render(request,'add_course.html',{ 'form' : form })
        return redirect('facultyhome')
    
    def post(self,request):

        form_data = CourseForm1(data=request.POST)
        if form_data.is_valid():
            request.session['course_name'] = form_data.cleaned_data.get('course_name')
            return redirect('add_course_2')
        return redirect('facultyhome')

class AddCourseView2(View):

    def get(self, request):
        if request.user:
            form = CourseForm2()
            return render(request,'add_course_step2.html',{'form':form})
        return redirect('facultyhome')
    
    def post(self,request):
        form_data = CourseForm2(data=request.POST)
        if form_data.is_valid():
            request.session['category'] = form_data.cleaned_data.get('category')
            return redirect('add_course_3')
        return redirect('facultyhome')
        
class AddCourseView3(View):
    def get(self, request):
        if request.user:
            form = CourseForm3()
            return render(request,'add_course_step3.html',{'form':form})
        
    def post(self,request):
        form = CourseForm3(data=request.POST,files=request.FILES)
        if form.is_valid():
            Course.objects.create(
                faculty = request.user,
                course_name = request.session['course_name'],
                category = request.session['category'],
                course_image = form.cleaned_data.get('course_image'),
                syllabus = form.cleaned_data.get('syllabus'),
                course_desc = form.cleaned_data.get('course_desc'),
                course_fee = form.cleaned_data.get('course_fee'),
                course_duration = form.cleaned_data.get('course_duration'),
            )
            request.session.pop('course_name', None)
            request.session.pop('category', None)
            return redirect('dashboard')
        for field, errors in form.errors.items():
                for error in errors:
                   print( messages.error(request, f"{field}: {error}"))
        return render(request,'add_course_step3.html',{'form':form})
    

class DetailView(View):

    def get(self, request,**kwargs):
        c_id = kwargs.get('id')
        name = request.user.name
        name = name[0:2]
        course = Course.objects.get(id=c_id)
        c_module = CourseModule.objects.filter(course = c_id)
        module_form = CourseModuleForm()
        form = CourseDescrptionEditForm(instance=course)
        syllabus = CourseSyllabusEditForm(instance=course)
        video_data = Video.objects.filter(course_module__in = c_module)
        video_form = VideoForm()
        return render(request,'detail_view.html',{'course':course,'name':name,'form':form,'syllabus':syllabus,
                                    'module_form':module_form,'c_module':c_module,'video_data': video_data,
                                    'video_form': video_form, })
    


class DescriptionUpdateView(UpdateView):

    model = Course
    pk_url_kwarg = 'id'
    form_class = CourseDescrptionEditForm
    template_name = 'detail_view.html'

    def get_success_url(self) -> str:
        return reverse_lazy('detail',kwargs={'id':self.kwargs['id']})


class SyllabusEditView(UpdateView):
    model = Course
    pk_url_kwarg = 'id'
    form_class = CourseSyllabusEditForm
    template_name = 'detail_view.html'

    def get_success_url(self) -> str:
        return reverse_lazy('detail',kwargs = {'id':self.kwargs.get('id')})
    

class ModuleCreationView(View):
    
    def get(self, request, **kwargs):
        c_id = kwargs.get('id')
        course = Course.objects.get(id = c_id)
        module_form = CourseModuleForm()
        c_module = CourseModule.objects.filter(course = c_id)
        video_data = Video.objects.filter(course_module__in = c_module)
        form = CourseDescrptionEditForm(instance=course)
        syllabus = CourseSyllabusEditForm(instance=course)
        video_form = VideoForm()
        context = {
            'form': form,
            'syllabus': syllabus,
            'module_form': module_form,
            'course': course,
            'c_module': c_module,
            'video_data': video_data,
            'video_form': video_form,
        }
        return render(request,'detail_view.html',context)
    
    def post(self,request,**kwargs):
        c_id = kwargs.get('id')
        course = Course.objects.get(id = c_id)
        c_module = CourseModule.objects.filter(course = c_id)
        form_data = CourseModuleForm(request.POST)
        module_form = CourseModuleForm()
        video_data = Video.objects.filter(course_module__in = c_module)
        form = CourseDescrptionEditForm(instance=course)
        syllabus = CourseSyllabusEditForm(instance=course)
        video_form = VideoForm()
        context = {
            'form': form,
            'syllabus': syllabus,
            'module_form': module_form,
            'course': course,
            'c_module' : c_module,
            'video_data': video_data,
            'video_form': video_form,
            
        }
        if form_data.is_valid():
            module = form_data.save(commit=False)   
            module.course = course
            module.save()
            return redirect('video',id=c_id)
        
        return render(request,'detail_view.html',context)
    

class VideoUploadingView(View):

    def get(self, request, **kwargs):
        c_id = kwargs.get('id')
        course = Course.objects.get(id = c_id)
        video_form = VideoForm()
        c_module = CourseModule.objects.filter(course = c_id)
        video_data = Video.objects.filter(course_module__in = c_module)
        module_form = CourseModuleForm()
        form = CourseDescrptionEditForm(instance=course)
        syllabus = CourseSyllabusEditForm(instance=course)
        context = {

            'form': form,
            'syllabus': syllabus,
            'module_form': module_form,
            'course': course,
            'video_form': video_form,
            'video_data': video_data,
            'c_module': c_module,

        }
        return render(request,'detail_view.html',context)
    def post(self, request, **kwargs):

        c_id = kwargs.get('id')
        course = Course.objects.get(id = c_id)
        video_form = VideoForm()
        c_module = CourseModule.objects.filter(course = c_id)
        video_data = Video.objects.filter(course_module__in = c_module)
        module_form = CourseModuleForm()
        form = CourseDescrptionEditForm(instance=course)
        syllabus = CourseSyllabusEditForm(instance=course)
        context = {

            'form': form,
            'syllabus': syllabus,
            'module_form': module_form,
            'course': course,
            'video_form': video_form,
            'video_data': video_data,
            'c_module': c_module,

        }
        video_form_data = VideoForm(data=request.POST,files=request.FILES)
        if video_form_data.is_valid():
            course_module_id = request.POST.get('course_module')                        
            course_module = CourseModule.objects.get(id = course_module_id)
            if course_module:
                try:
                    video = video_form_data.save(commit=False)
                    video.course_module = course_module
                    video.save()
                    return redirect('detail',id=c_id)
                except CourseModule.DoesNotExist:
                    messages.error(request, 'Course Module does not exist')
        return render(request,'detail_view.html',context)


