from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hello', views.hello, name='hello'),
    path('update', views.update, name='update'), #Esto es lo que agregamos
    path('upload', views.upload, name='upload'),
    path('up', views.up, name='up') #Esto es lo que agregamos
]