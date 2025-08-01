"""
URL configuration for PFB_Typography project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import pages.views, catalog.views, core.views, orders.views, reviews.views, users.views
from django.conf.urls import handler404, handler500

handler400 = 'core.views.custom_400'
handler403 = 'core.views.custom_403'
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'

urlpatterns = [
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
    path('', pages.views.main ,name='main'),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('about_us/', pages.views.about_us ,name="about_us"),
    path('pay-delivery/', pages.views.pay_delivery ,name="pay_delivery"),
    path('question–answer/', pages.views.question_answer ,name="question_answer"),
    path('account/', include('users.urls', namespace='user')),
    path('news/', include('news.urls', namespace='news')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('nested_admin/', include('nested_admin.urls')),
    path('activate/<uidb64>/<token>/', core.views.activate_account, name="activate_account"),
    path('email-change/<uidb64>/<token>/', core.views.change_email_confirm, name='change_email_confirm'),
    path("portfolio/", pages.views.portfolio_view, name="portfolio"),
    path("return-policy/", pages.views.return_policy_view, name="return_policy"),
    path("terms-of-use/", pages.views.terms_of_use_view, name="terms_of_use"),
    path("privacy-policy/", pages.views.privacy_policy_view, name="privacy_policy"),
    path('checkout/', orders.views.checkout, name='checkout'),
    path('add-order-recipient/<int:order_id>/', orders.views.add_order_recipient, name='add_order_recipient'),
    path('update-order-recipient/<int:order_id>/', orders.views.update_order_recipient, name='update_order_recipient'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)