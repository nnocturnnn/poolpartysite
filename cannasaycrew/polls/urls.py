from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.login, name='signin'),
    path('signup', views.register, name="register"),
    path('media', views.media, name="media"),
    path('buy', views.sell, name="sell"),
]