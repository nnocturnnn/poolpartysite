from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.template import loader
from django.contrib.auth.models import User, auth
from django.views import View
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.core.mail import EmailMessage
from .utils import send_auth_mail, token_generator, url_generate, mono_check, create_phys_ticket
from .models import Urls
import os

def get_url(request):
    user = User.objects.get(id=1)
    links = url_generate(user,request,'buy')
    url = Urls(link=links,active=False)
    url.save()
    return HttpResponse(links)

def index(request):
    return render(request, "polls/index.html")


def login(request):
    if request.method == 'POST':
        user=request.POST['user']
        passw=request.POST['pass']
        user=auth.authenticate(username=user,password=passw)
        if user is not None:
            if user.is_active:
                auth.login(request,user)
                return redirect('/polls/')
            else:
                messages.error(request,'Please activate acc')
                return redirect("signin")
        else:
            messages.error(request,'invalid credentials!')
            return redirect("signin")
    else:
        return render(request, "polls/signin.html")


def register(request):
    if request.method == 'POST':
        try:
            name = request.POST['user']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            email = request.POST['email']
            if pass1 == pass2:
                if User.objects.filter(username=name).exists():
                    messages.info(request,'Username already exists!')
                    return redirect('/polls/signup')
                # elif User.objects.filter(email=email).exists():
                #     messages.info(request,'Email already exists!')
                #     return redirect('register')
                else:
                    user = User.objects.create_user(username=name,password=pass1,email=email,first_name=name)
                    user.is_active = False
                    user.save()
                    send_auth_mail(user, name, pass1, email, request, 'reg')
                    return redirect('signin')
            else:
                messages.info(request,'Password not matching!!')
                return redirect('/polls/signup')
        except Exception as e:
            print(e)
            return redirect('/polls/')
    else:
        return render(request, "polls/signup.html")


def logout(request):
    auth.logout(request)
    return redirect("/polls")


def media(request):
    return render(request, "polls/media.html")


def sell(request):
    return render(request, "polls/sell.html")


def detail(request):
    template = loader.get_template('polls/detail.html')
    usr = request.user
    if request.method == "POST":
        if mono_check(usr.username):
            link = url_generate(usr,request,'buy')
            url = Urls(link=link,active=False)
            url.save()
            if request.path[-1] == "2":
                create_phys_ticket(link,usr.email)
                context = {'price' : "350", 'backcolor' : 'green'}
                return HttpResponse(template.render(context, request))
            else:
                create_phys_ticket(link,usr.email)
                context = {'price' : "400", 'backcolor' : 'green'}
                return HttpResponse(template.render(context, request))
        else:
            if request.path[-1] == "2":
                context = {'price' : "350", 'backcolor' : 'red'}
                return HttpResponse(template.render(context, request))
            else:
                context = {'price' : "400", 'backcolor' : 'red'}
                return HttpResponse(template.render(context, request))
    else:
        if request.path[-1] == "2":
            context = {'price' : "350"}
            return HttpResponse(template.render(context, request))
        else:
            context = {'price' : "400"}
            return HttpResponse(template.render(context, request))


def error_asses(request):
    return render(request, "polls/null.html", {'title': 'Error','color' : 'red'})

def fine_asses(request):
    return render(request, "polls/null.html", {'title': 'Yep','color' : 'green'})

class VerificationView(View):
    def get(self, request, uidb64, token):
        if 'buy' not in request.build_absolute_uri():
            try:
                id = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=id)
                if not token_generator.check_token(user, token):
                    return redirect('polls/signup')
                if user.is_active:
                    return redirect('polls/login')
                user.is_active = True
                user.save()
                messages.success(request,"GJ")
                return redirect('polls/login')
        
            except Exception as ex:
                print(ex)
            return redirect('login')
        else:
            try:
                link = Urls.objects.get(link=request.build_absolute_uri())
                if link.active:
                    return redirect('error_asses')
                link.active = True
                link.save()
                return redirect('fine_asses')
            except Exception as ex:
                return redirect('error_asses')
