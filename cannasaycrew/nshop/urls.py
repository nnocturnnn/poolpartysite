from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('add', views.add_item, name='add'),
    path("logout",views.logout,name="logout"),
]