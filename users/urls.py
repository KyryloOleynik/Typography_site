from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordChangeForm

app_name = 'user'

urlpatterns = [
    path('my-orders/', views.my_orders_view, name='my_orders'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('messages/', views.view_messages, name="messages"),
    path('favorites/', views.favorites, name="favorites"),
    path('favorites/remove-selected-favorites/', views.remove_selected_favorites, name="remove_selected_favorites"),
    path('remove-from-favorites/<slug:slug>/', views.remove_from_favorites, name="remove_from_favorites"),
    path('add-to-favorites/<slug:slug>/', views.add_to_favorites, name="add_to_favorites"),
    path('', views.dashboard , name="dashboard"),
    path('logout/', views.CustomLogout.as_view(), name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.registration, name='registration'),
    path('password-change/', views.CustomPasswordChangeView.as_view(template_name='users/password_change.html', success_url='/account/', form_class=CustomPasswordChangeForm), name='password_change'),
    path('update-profile-info/', views.update_profile, name="update_profile"),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('email-change/', views.email_change, name='email_change'),
    path('tickets/', views.my_tickets, name='tickets'),
    path('update-recipient/', views.update_recipient, name="update_recipient"),
    path('add-recipient/', views.add_recipient, name="add_recipient"),
    path('delete-recipient/', views.delete_recipient, name='delete_recipient'),
]