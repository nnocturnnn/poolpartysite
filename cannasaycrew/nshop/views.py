from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages

def index(request):
    return render(request, "nshop/index.html")

def login(request):
    if User.is_authenticate() == False:
        if request.method == 'POST':
            user=request.POST['user']
            passw=request.POST['pass']
            user=auth.authenticate(username=user,password=passw)
            if user is not None:
                auth.login(request,user)
                return redirect('/nakaz/')
            else:
                messages.error(request,'invalid credentials!')
                return redirect("login")
        else:
            return render(request, "nshop/login.html")
    else:
        return render(request, "nshop/index.html")

def register(request):
    if request.method == 'POST':
        name = request.POST['user']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        email = request.POST['email']
        if pass1 == pass2:
            if User.objects.filter(username=name).exists():
                messages.info(request,'Username already exists!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already exists!')
                return redirect('register')
            else:
                user = User.objects.create_user(username=name,password=pass1,email=email,first_name=name)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'Password not matching!!')
            return redirect('register')
    else:
        return render(request, "nshop/register.html")

def add_item(request):
    return render(request, "nshop/add.html")



def logout(request):
    auth.logout(request)
    return redirect("/")