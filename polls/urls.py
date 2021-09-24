from django.urls import path
from .views import VerificationView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.login, name='signin'),
    path('signup', views.register, name="register"),
    path('media', views.media, name="media"),
    path('buy', views.sell, name="sell"),
    path('detail1', views.detail, name="detail"),
    path('detail2', views.detail, name="detail"),
    path("logout",views.logout,name="logout"),
    path('activate/<uidb64>/<token>',VerificationView.as_view(), name="activate"),
    path('buy/<uidb64>/<token>',VerificationView.as_view(), name="buy"),
    path("get_url",views.get_url,name="get_url"),
]