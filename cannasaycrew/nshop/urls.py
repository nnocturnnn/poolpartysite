from django.urls import path
from .views import VerificationView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('add', views.add_item, name='add'),
    path("logout",views.logout,name="logout"),
    path('activate/<uidb64>/<token>',VerificationView.as_view(), name="activate"),
    path('error_asses',views.error_asses,name="error_asses"),
    path('fine_asses',views.fine_asses,name="fine_asses"),
]