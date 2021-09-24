from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template import loader
from django.http import HttpResponse
from django.views import View
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text

from .models import Product
from .utils import send_auth_mail, token_generator

def index(request):
    product_list = Product.objects.all()
    template = loader.get_template('nshop/index.html')
    context = {'auction_list' : product_list}
    return HttpResponse(template.render(context, request))

def login(request):
    if request.method == 'POST':
        user=request.POST['user']
        passw=request.POST['pass']
        user=auth.authenticate(username=user,password=passw)
        if user is not None:
            if user.is_active:
                auth.login(request,user)
                return redirect('/nakaz/')
            else:
                messages.error(request,'Please activate acc')
                return redirect("login")
        else:
            messages.error(request,'invalid credentials!')
            return redirect("login")
    else:
        return render(request, "nshop/login.html")

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
            # elif User.objects.filter(email=email).exists():
            #     messages.info(request,'Email already exists!')
            #     return redirect('register')
            else:
                user = User.objects.create_user(username=name,password=pass1,email=email,first_name=name)
                user.is_active = False
                user.save()
                send_auth_mail(user, name, pass1, email, request)
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
    return redirect("/nakaz")


def media(request):
    return render(request, "nshop/media.html")

def error_asses(request):
    return render(request, "nshop/null.html", {'title': 'Error','color' : 'red'})

def fine_asses(request):
    return render(request, "nshop/null.html", {'title': 'Yep','color' : 'green'})

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not token_generator.check_token(user, token):
                return redirect('error_asses')
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request,"GJ")
            return redirect('fine_asses')
    
        except Exception as ex:
            print(ex)
        return redirect('login')
      