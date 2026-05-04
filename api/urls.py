from django.urls import path
from .views import register, login, login_page, dashboard_page
from .views import *

urlpatterns = [
    # API
    path('register/', register),
    path('login/', login),

    # HTML Pages
    path('', login_page, name='login_page'),
    path('dashboard/', dashboard_page, name='dashboard'),
    
]
from .views import create_project_page, create_task_page

urlpatterns += [
    path('create-project/', create_project_page, name='create_project'),
    path('create-task/', create_task_page, name='create_task'),
    path('update-task/<int:id>/', update_task_status, name='update_task'),
    
]