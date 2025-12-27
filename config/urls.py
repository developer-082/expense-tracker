"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from main.views import statistics, expense_delete, expense_create, expense_update, category_create, category_delete, category_update, home, categories

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', statistics, name='dashboard'),

    path('home/', home, name='home'),
    path('expense/create/', expense_create, name='expense_create'),
    path('expense/delete/<int:pk>/', expense_delete, name='expense_delete'),
    path('expense/update/<int:pk>/', expense_update, name='expense_update'),

    path('categories/', categories, name='categories'),
    path('categories/create/', category_create, name='category_creat'),
    path('categories/delete/<int:pk>/', category_delete, name='category_delete'),
    path('categories/update/<int:pk>/', category_update, name='category_update')
]
