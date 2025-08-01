from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_main, name="main_news"),
    path('<slug:slug>/', views.view_news, name='view_news'),
]