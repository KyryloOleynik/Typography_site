from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from users.models import CustomUser
from django.contrib import messages
from django.shortcuts import redirect, render
from .utils import get_base_info

# Create your views here.
def activate_account(request, uidb64, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=user_id)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Акаунт успішно активовано! Можете увійти.')
        return redirect('main')
    else:
        messages.error(request, 'Посилання недійсне або протерміноване.')
        return redirect('main')

def change_email_confirm(request, uidb64, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=user_id)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    new_email = (request.GET.get('new_email') or '').strip()

    if user is not None and default_token_generator.check_token(user, token) and new_email:
        if CustomUser.objects.filter(email=new_email).exclude(id=user.id).exists():
            messages.error(request, 'Ця електронна адреса вже використовується іншим користувачем.')
            return redirect('main')
        user.email = new_email
        user.save()
        messages.success(request, 'Електронну адресу успішно змінено!')
        return redirect('main')
    else:
        messages.error(request, 'Посилання недійсне або застаріле, або не вказано нову електронну адресу.')
        return redirect('main')
    

def custom_404(request, exception):
    main_data = get_base_info(request)
    return render(request, '404.html', context=main_data, status=404)

def custom_500(request):
    main_data = get_base_info(request)
    return render(request, '500.html', context=main_data, status=500)

def custom_400(request, exception):
    main_data = get_base_info(request)
    return render(request, '400.html', context=main_data, status=400)

def custom_403(request, exception):
    main_data = get_base_info(request)
    return render(request, '403.html', context=main_data, status=403)