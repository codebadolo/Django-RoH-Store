from django.urls import path
from mysite import settings
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('colors/', views.colors, name='colors'),
]
