from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login as auth_login
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import User, Task

def home(request):
    return render(request, 'home.html')
# 🔐 API: Register
@api_view(['POST'])
def register(request):
    user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        role=request.data['role']
    )
    return Response({'message': 'User created'})


# 🔐 API: Login
@api_view(['POST'])
def login(request):
    user = authenticate(
        username=request.data['username'],
        password=request.data['password']
    )
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)})
    return Response({'error': 'Invalid credentials'})


# 🌐 HTML Login Page
def login_page(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            auth_login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')


# 🌐 Dashboard Page
from django.utils.timezone import now

def dashboard_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')

    tasks = Task.objects.all()

    context = {
        "tasks": tasks,
        "total": tasks.count(),
        "completed": tasks.filter(status='completed').count(),
        "pending": tasks.filter(status='pending').count(),
        "overdue": tasks.filter(due_date__lt=now()).count()
    }

    return render(request, 'dashboard.html', context)
from .models import Project


# 🌐 Create Project Page
def create_project_page(request):
    if request.method == 'POST':
        Project.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            created_by=request.user
        )
        return redirect('dashboard')

    return render(request, 'create_project.html')


# 🌐 Create Task Page
def create_task_page(request):
    if request.method == 'POST':
        Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            due_date=request.POST['due_date'],
            project_id=request.POST['project_id'],
            assigned_to_id=request.POST['user_id']
        )
        return redirect('dashboard')

    return render(request, 'create_task.html')
def update_task_status(request, id):
    task = Task.objects.get(id=id)
    task.status = 'completed'
    task.save()
    return redirect('dashboard')