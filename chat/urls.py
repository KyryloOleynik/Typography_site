from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('send-message/', views.send_message, name="send_message"),
    path('upload-chat/', views.upload_chat, name="upload_chat"),
]