from django.shortcuts import render
from django.shortcuts import redirect, render

def index(request):
    return render(request, "polls/index.html")


def login(request):
    return render(request, "polls/signin.html")


def register(request):
    return render(request, "polls/signup.html")


def media(request):
    return render(request, "polls/media.html")


def sell(request):
    return render(request, "polls/sell.html")