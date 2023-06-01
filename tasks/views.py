from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

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

def tasks (request):
    return render (request, "tasks.html")

def sign_out (request):
    logout (request)
    return redirect ("home")

def sign_user(request):
    if request.method == "GET":
        return render (request, "signin.html", {
            "form": AuthenticationForm
        })
    else:
        user = authenticate (request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render (request, "signin.html", {
            "form": AuthenticationForm,
            "error": "Username or password is incorrect"
            })