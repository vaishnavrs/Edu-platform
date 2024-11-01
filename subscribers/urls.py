from django.urls import path
from .views import *

urlpatterns=[
    path('signup/',SubsciberRegView.as_view(),name='signup'),
    path('login/',SubscriberLoginView.as_view(),name='sub_login'),
    path('course/detail/<int:id>/',CourseDetailView.as_view(),name='course_detail'),
    path('course/cart/<int:id>/',AddToCartView.as_view(),name='add_to_cart'),
    path('cart/',CartView.as_view(),name='cart'),
]