"""
URL configuration for MeterReadingLookup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from lookup import views

urlpatterns = [
    path('', views.index, name='main.html'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('flowfile_list/', views.flowfile_list, name='flowfile_list'),
    path('detail/<str:file_name>', views.flowfile_detail, name='flowfile_detail'),
    path('admin/', admin.site.urls),
]
