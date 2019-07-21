'''Определяет схемы URL пользователей'''

from django.conf.urls import url
from django.contrib.auth.views import LoginView

from . import views

urlpatterns =[
    # страница входа
    url(r'^login/$', LoginView.as_view(template_name='users/login.html'), name='login'),
    # страница выхода
    url(r'^logout/$', views.logout_view, name='logout'),
    # страница реистрации
    url(r'^register/$', views.register, name='register'),
]