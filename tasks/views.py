from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone

def home(request):
    return render(request, "home.html")

def sign_up(request):
    if request.method == "GET":
        return render(request, "signup.html", {
            "form": UserCreationForm
        })
    else:
        if request.POST["password1"] == request.POST["password2"]:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()
                #this fuction save the cookie with the new user in the browser 
                login (request, user)
                return redirect ("tasks" )
            except IntegrityError:
                return render(request, "signup.html", {
            "form": UserCreationForm,
            "error":"User already exists"
        })
        error ="passwords do not match"
        return render(request, "signup.html", {
            "form": UserCreationForm,
            "error":error
        })

@login_required ()
def tasks (request):
    tasks = Task.objects.filter (user=request.user, date_completed__isnull=True)
    return render (request, "tasks.html", {
        "tasks":tasks
    })
    #the first tasks in the context, is the var wich is going to be in the html

@login_required ()
def tasks_completed (request):
    tasks = Task.objects.filter (user=request.user, date_completed__isnull=False).order_by ("-date_completed")
    return render (request, "tasks.html", {
        "tasks":tasks
    })

@login_required ()
def task_detail (request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm (instance=task)
        return render (request, "task_detail.html", {
            "task":task, "form":form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm (request.POST, instance=task)
            form.save()
            return redirect ("tasks")
        except ValueError:
            return render (request, "task_detail.html", {
            "task":task, 
            "form":form,
            "error":"No ha sido posible actualizar la tarea"
        })

@login_required ()
def task_complete (request, task_id):
    task = get_object_or_404 (Task,pk=task_id, user=request.user)
    if request.method == "POST":
        task.date_completed = timezone.now()
        task.save()
        return redirect ("tasks")

@login_required ()
def task_list (request):
    task = get_object_or_404 (Task, user=request.user)
    return render (request, "task_completed.html", {"tasks":task})

@login_required ()
def task_delete (request, task_id):
    task = get_object_or_404 (Task,pk=task_id, user=request.user)
    if request.method == "POST":
        task.date_completed = timezone.now()
        task.delete()
        return redirect ("tasks")

@login_required ()
def create_tasks (request):
    if request.method == "GET":
        return render (request, "create_tasks.html", {
            "form": TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save (commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect ("tasks")
        except ValueError:
                return render (request, "create_tasks.html", {
            "form": TaskForm,
            "error":"Please provide a correct date"
        })

def sign_out (request):
    logout (request)
    return redirect ("home")

def sign_user(request):
    #only showing the form
    if request.method == "GET":
        return render (request, "signin.html", {
            "form": AuthenticationForm
        })
    else:
        #checks if the user exists
        user = authenticate (request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render (request, "signin.html", {
            "form": AuthenticationForm,
            "error": "Username or password is incorrect"
            })
        else:
            login (request, user)
            return redirect ("tasks")