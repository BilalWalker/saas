from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login

# Create your views here.
def login_view(request):
    username = 'cfe2'#request.POST["username"]
    password = 'bilalkhan123'#request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        print("login here!")
        return redirect("/")
    return render(request, "auth/login.html", {})

# def register_view(request):
#     return render(request, "auth/login.html", {})
