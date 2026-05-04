from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.utils.timezone import now

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Task, Project


# -------------------------
# 🌐 HOME PAGE
# -------------------------
def home(request):
    return render(request, 'home.html')


# -------------------------
# 🔐 API: REGISTER
# -------------------------
@api_view(['POST'])
def register(request):
    user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        role=request.data.get('role', 'member')
    )
    return Response({'message': 'User created'})


# -------------------------
# 🔐 API: LOGIN (FIXED NAME)
# -------------------------
@api_view(['POST'])
@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "username and password required"}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    })
# -------------------------
# 🌐 LOGIN PAGE (HTML)
# -------------------------
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


# -------------------------
# 🌐 DASHBOARD
# -------------------------
def dashboard_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')

    tasks = Task.objects.all()

    return render(request, 'dashboard.html', {
        "tasks": tasks,
        "total": tasks.count(),
        "completed": tasks.filter(status='completed').count(),
        "pending": tasks.filter(status='pending').count(),
        "overdue": tasks.filter(due_date__lt=now()).count()
    })


# -------------------------
# 🌐 CREATE PROJECT
# -------------------------
def create_project_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')

    if request.method == 'POST':
        Project.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            created_by=request.user
        )
        return redirect('dashboard')

    return render(request, 'create_project.html')


# -------------------------
# 🌐 CREATE TASK
# -------------------------
def create_task_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')

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


# -------------------------
# ✅ UPDATE TASK STATUS
# -------------------------
def update_task_status(request, id):
    if not request.user.is_authenticated:
        return redirect('login_page')

    task = Task.objects.get(id=id)
    task.status = 'completed'
    task.save()

    return redirect('dashboard')