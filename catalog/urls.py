from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('<slug:slug>/', views.category_detail, name='category_detail'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
    path('service/<slug:slug>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('service/<slug:slug>/remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
]