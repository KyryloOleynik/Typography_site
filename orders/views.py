from django.shortcuts import render, redirect, get_object_or_404
from core.utils import get_base_info
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from users.forms import RecipientForm, ChangeUserDataForm
from orders.models import Recipient, Order
from django.contrib import messages

# Create your views here.
delivery_options = [
    {"label": "Самовивіз із магазину", "price": "0 ₴", "checked": True, "extra_html": ""},
    {"label": "Доставка Новою Поштою", "price": "за тарифами", "checked": False, "extra_html": "<small class='text-muted'>1-2 дні</small>"},
]
payment_options = [
    {"value": "cod", "title": "Оплата при отриманні", "checked": True, "description": "Оплачуєте після огляду товару"},
    {"value": "online", "title": "Оплата карткою онлайн", "checked": False, "description": "Visa/MasterCard/Google Pay"},
]

@login_required
def checkout(request):
    main_data = get_base_info(request)
    form_user = ChangeUserDataForm(instance=request.user)
    if not main_data.get('cart').items.exists():
        return redirect(request.META.get('HTTP_REFERER', 'main'))
    cart = main_data.get('cart')
    if cart.recipient:
        current_recipient = cart.recipient
    else:
        current_recipient = request.user.recipients.first()
        if current_recipient:
            cart.recipient = current_recipient
            cart.save()
    form = RecipientForm(instance=current_recipient)
    return render(request, 'orders/checkout.html', {**main_data, 'payment_options': payment_options, 'delivery_options': delivery_options, 'form': form, 'current_recipient': current_recipient, 'form_user': form_user })

@login_required
@require_POST
def update_order_recipient(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    form_user = ChangeUserDataForm(instance=request.user)

    recipient_id = request.POST.get('recipient_id')
    if recipient_id:
        recipient = get_object_or_404(Recipient, id=recipient_id, user=request.user)
        form = RecipientForm(request.POST, instance=recipient)
        if form.is_valid():
            form.save()
            order.recipient = recipient
            order.save()
            messages.success(request, "Отримувача успішно оновлено.")
            return redirect('checkout')
        else:
            for field, errors in form.errors.items():
                if field == '__all__':
                    for error in errors:
                        messages.error(request, error)
    else:
        messages.error(request, "Не вибрано отримувача для оновлення.")

    main_data = get_base_info(request)
    return render(request, 'orders/checkout.html', {**main_data, 'payment_options': payment_options, 'delivery_options': delivery_options, 'form': form, 'current_recipient': recipient, 'form_user': form_user })


@login_required
@require_POST
def add_order_recipient(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    form_user = ChangeUserDataForm(instance=request.user)

    form = RecipientForm(request.POST)
    if form.is_valid():
        recipient = form.save(commit=False)
        recipient.user = request.user
        recipient.save()

        order.recipient = recipient
        order.save()
        messages.success(request, "Отримувача успішно додано та прикріплено до замовлення.")
        return redirect('checkout')
    else:
        for field, errors in form.errors.items():
            if field == '__all__':
                for error in errors:
                    messages.error(request, error)

    main_data = get_base_info(request)
    return render(request, 'orders/checkout.html', {**main_data, 'payment_options': payment_options, 'delivery_options': delivery_options, 'form': form, 'current_recipient': None, 'form_user': form_user })