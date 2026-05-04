from django.urls import path
from .views import (
    register,
    login_api,
    login_page,
    dashboard_page,
    create_project_page,
    create_task_page,
    update_task_status
)

urlpatterns = [
    # API
    path('register/', register),
    path('login/', login_api),

    # HTML Pages
    path('', login_page, name='login_page'),
    path('dashboard/', dashboard_page, name='dashboard'),

    path('create-project/', create_project_page, name='create_project'),
    path('create-task/', create_task_page, name='create_task'),
    path('update-task/<int:id>/', update_task_status, name='update_task'),
]