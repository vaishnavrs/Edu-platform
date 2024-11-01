from django.shortcuts import render,redirect
from .forms import SubscriberRegForm,SubscriberLoginForm
from django.views.generic import View,FormView
from django.contrib.auth import authenticate,login,logout
from accounts.models import Course,CourseModule,Video,Student,Cart
from django.contrib import messages
from django.db.models import Sum
# Create your views here.



class SubsciberRegView(View):
    def get(self, request):
        form = SubscriberRegForm()
        return render(request, 'subscriber_reg.html', {'reg_form': form})
    
    def post(self,request):
        form_data = SubscriberRegForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('index')
        return render(request,'subscriber_reg.html',{'reg_form':form_data})
    
class SubscriberLoginView(View):
    def get(self, request):
        form = SubscriberLoginForm()
        return render(request, 'subscriber_login.html', {'form': form})
    
    def post(self, request):
        form_data = SubscriberLoginForm(request.POST)
        if form_data.is_valid():
            uname = form_data.cleaned_data.get('username')
            pwd = form_data.cleaned_data.get('password')
            user = authenticate(request, username=uname, password=pwd, backend='accounts.StudentBackend')
            if user is not None:
                if user.user_type == 'Student':
                    login(request, user)
                    return redirect('index')
                else:
                    messages.info(request, 'Not allowed to login as a student')
                    return redirect('sub_login')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('sub_login')
        return render(request, 'subscriber_login.html', {'form': form_data})


class CourseDetailView(View):
    def get(self, request, **kwargs):
        course_id = kwargs.get('id')
        if course_id:
            course = Course.objects.get(id=course_id)
            module = CourseModule.objects.filter(course = course)
            video  = Video.objects.filter(course_module__in=module)
            des = {}
            desc_text = course.course_desc
            chunk_size = 100 
            for idx in range(0, len(desc_text), chunk_size):
                if len(des) < 10:
                    des[f'line{idx//chunk_size + 1}'] = desc_text[idx:idx + chunk_size].strip()
            return render(request,'course_detail.html',{'course':course,'description':des,'module':module,'video':video})
        return render(request,'index.html')
    


class AddToCartView(View):

    def post(self, request, **kwargs):
        course_id = kwargs.get('id')
        course = Course.objects.get(id=course_id)
        if request.user.is_authenticated:
            if request.user.user_type == 'Student':
                student = Student.objects.get(id=request.user.id) 
                if not Cart.objects.filter(student=student, course=course).exists():
                    Cart.objects.create(student=student, course=course)
                    return redirect('course_detail', id=course_id)
                else:
                    messages.info(request, 'Course is already in the cart.')
                    return redirect('course_detail', id=course_id)
            else:
                messages.error(request, 'Only students can add courses to the cart.')
                print('only students can add to cart',request.user.name)
                return redirect('course_detail', id=course_id)
        print('not authenticated')
        return redirect('sub_login')
    



class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            student = Student.objects.get(id=request.user.id)
            cart = Cart.objects.filter(student=student)
            total = cart.aggregate(total_price=Sum('course__course_fee'))['total_price'] or 0
            return render(request, 'cart.html',{'cart':cart,'total':total})
        return redirect('sub_login')

