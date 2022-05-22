from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('hello', views.hello, name='hello'),
    path('update', views.update, name='update'),
    path('home', views.home, name='home'),
    path('verify', views.verify, name='verify'),
    path('up', views.up, name='up'),
    path('upload', views.upload, name='upload'),
    path('add', views.add, name='add'),
    path('modify', views.modify, name='modify'),
    path('delete', views.delete, name='delete')
]