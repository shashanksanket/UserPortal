from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    path('list',views.list,name='list'),
    path('download_file/<int:pk>',views.download,name='download_file'),
    
    # path('index',views.index,name='index'),
    
]
