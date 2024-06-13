from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('join_page', views.join_page, name='join_page'),
    path('login_chk', views.login_chk, name='login_chk'),
    path('join_chk', views.join_chk, name='join_chk'),
    path('logout', views.logout, name='logout'),
]
