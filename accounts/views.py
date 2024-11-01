from django.shortcuts import render
from django.views.generic import View
from .models import Course





class HomeView(View):
    
    def get(self, request):
         category = request.GET.get('category', 'Development')
         courses = Course.objects.filter(category=category).order_by('category')
         grouped_courses = {category: list(courses)}
         return render(request, 'index.html', {'courses': grouped_courses, 'selected_category': category})



