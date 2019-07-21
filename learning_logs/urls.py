'''Определяет схемы URL для learning_logs'''

from django.conf.urls import url
from . import views

urlpatterns = [
    # Домашняя страница
    url(r'^$', views.index, name='index'),
    # Вывод всех тем
    url(r'^topics/$', views.topics, name='topics'),
    # Страница с подробной информацией по отдельной теме
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    # Страница для добавления новой темы
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    # Страница для удаления темы
    url(r'^new_topic/(?P<topic_id>\d+)/$', views.del_topic, name='del_topic'),
    # Страница для добавления новой записи
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    # Страница для редактирования записи
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
    # Удаление записи
    url(r'^del_entry/(?P<entry_id>\d+)/$', views.del_entry, name='del_entry'),
]