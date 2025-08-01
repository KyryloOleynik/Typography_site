from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from core.utils import get_base_info, send_activation_email, send_confirm_email
from .forms import RegistrationForm, ChangeUserDataForm, CustomPasswordResetForm, CustomSetPasswordForm, RecipientForm
from catalog.models import Service
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import views as auth_views
from .models import CustomUser
from orders.models import Order
from django.http import JsonResponse
from django.urls import reverse_lazy
from orders.utils import Cart
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from orders.models import Order, OrderItem, Recipient
from urllib.parse import urlparse
from django.urls import reverse

# Create your views here.
def registration(request):
    main_data = get_base_info(request)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_activation_email(request, user)
            messages.success(
                request,
                "Ви успішно зареєстровані! "
                "Будь ласка, перевірте свою електронну пошту — ми надіслали лист із посиланням для активації акаунта. "
                "Якщо листа немає у входящих, перевірте, будь ласка, папку 'Спам'."
            )
            return redirect('main')
    else:
        form = RegistrationForm()
    return render(request, 'users/registration.html', {'form': form, **main_data })

class CustomLogout(auth_views.LogoutView):
    next_page = 'main'

    def dispatch(self, request, *args, **kwargs):
        session_cart = Cart(request)
        session_cart.clear()
        
        order = None
        if request.user.is_authenticated:
            try:
                order = Order.objects.prefetch_related('items__options').get(user=request.user, status='new')
            except Order.DoesNotExist:
                pass
        
        logout(request)

        session_cart = Cart(request)

        response = HttpResponseRedirect(self.get_success_url())
        if order:
            for item in order.items.all():
                service = item.service
                quantity = item.quantity
                options = list(item.options.values_list('id', flat=True))

                if not session_cart.contains_similar_item({'service': service, 'quantity': quantity, 'options': list(item.options.all()),}):
                    session_cart.add(service, quantity, options)

        return response
    
@require_POST
def login_view(request):

    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, email=email, password=password)

    if user is not None:
        session_cart = Cart(request)
        auth_login(request, user)

        order, _ = Order.objects.get_or_create(user=user, status='new')

        for item in session_cart.get_items():
            exists = False
            for existing_item in order.items.all():
                if (
                    existing_item.service_id == item['service'].id and
                    existing_item.quantity == item['quantity'] and
                    set(existing_item.options.values_list('id', flat=True)) ==
                    set(opt.id for opt in item['options'])
                ):
                    exists = True
                    break

            if not exists:
                order_item = OrderItem.objects.create(
                    order=order,
                    service=item['service'],
                    quantity=item['quantity']
                )
                order_item.options.set(item['options'])

        session_cart.clear()
        messages.success(request, 'Ви увійшли в систему.')
        return redirect('main')

    messages.error(request, 'Невірний email або пароль.')
    return redirect('main')

@login_required
def dashboard(request):
    main_data = get_base_info(request)
    form = ChangeUserDataForm(instance=request.user)
    recipient_form = RecipientForm()
    recipient_form_edit = RecipientForm()
    return render(request, 'users/dashboard.html', {'form': form, 'recipient_form': recipient_form, 'recipient_form_edit': recipient_form_edit, **main_data })

@require_POST
def add_to_favorites(request, slug):
    if request.user.is_authenticated:
        try:
            target_service = Service.objects.get(slug=slug)
            request.user.favorites.add(target_service)
            messages.success(request, 'Товар додано до обраного.')
        except Service.DoesNotExist:
            messages.error(request, 'Ця послуга наразі недоступна.')
    else:
        messages.error(request, 'Для додавання товару до обраного необхідно увійти до акаунту.')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@require_POST
def remove_from_favorites(request, slug):
    if request.user.is_authenticated:
        try:
            target_service = Service.objects.get(slug=slug)
            if target_service in request.user.favorites.all():
                request.user.favorites.remove(target_service)
            else:
                messages.error(request, 'Цієї послуги немає у списку обраного.')
            messages.success(request, 'Товар видалено з обраного.')
        except Service.DoesNotExist:
            messages.error(request, 'Ця послуга наразі недоступна.')
    else:
        messages.error(request, 'Для редагування обраного потрібно увійти до акаунту.')

    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def favorites(request):
    main_data = get_base_info(request)
    return render(request, 'users/favorites.html', {**main_data, })

@require_POST
def remove_selected_favorites(request):
    slugs = request.POST.getlist('services')
    selected_favorites = Service.objects.filter(slug__in=slugs)
    for favorite in selected_favorites:
        if favorite in request.user.favorites.all():
            request.user.favorites.remove(favorite)
        else:
            messages.error(request, 'Цієї послуги немає у списку обраного.')

    return redirect(request.META.get('HTTP_REFERER', 'user:favorites'))

class CustomPasswordChangeView(auth_views.PasswordChangeView):

    def form_valid(self, form):
        messages.success(self.request, "Пароль успішно змінено")
        return super().form_valid(form)
    
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("main")

    email_template_name = 'users/password_reset_email.html'

    def form_valid(self, form):
        messages.success(self.request, "Посилання для скидання пароля надіслано на вашу пошту. Перевірте, будь ласка, також папку 'Спам'.")
        return super().form_valid(form)
    
class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy("main")
    form_class = CustomSetPasswordForm

    def form_valid(self, form):
        messages.success(self.request, "Пароль успішно змінено. Тепер ви можете увійти.")
        return super().form_valid(form)
    
@require_POST
@login_required
def update_profile(request):
    form = ChangeUserDataForm(request.POST, instance=request.user)
    main_data = get_base_info(request)
    success_url = request.POST.get('success_url', '')

    if form.is_valid():
        form.save()
        messages.success(request, 'Дані успішно оновлено.')
        if success_url == "checkout":
            return redirect('checkout')
        return redirect('user:dashboard')
    else:
        messages.error(request, 'Будь ласка, перевірте введені дані.')
        return render(request, 'users/dashboard.html', {'form': form, **main_data })

@login_required
def view_messages(request):
    main_data = get_base_info(request)
    if request.method == "GET":
        CustomUser.objects.filter(pk=request.user.pk).update(unread_messages=0)
        request.user.unread_messages = 0
    return render(request, 'users/messages.html', {**main_data, })

@login_required
def my_orders_view(request):
    main_data = get_base_info(request)
    user_orders = request.user.orders.filter(items__isnull=False).distinct()
    return render(request, 'users/my_orders.html', {**main_data, 'user_orders': user_orders, })

@login_required
def order_detail(request, order_id):
    try:
        order = Order.objects.prefetch_related('items__options').get(id=order_id, user=request.user)

        data = {
            "id": order.id,
            "status": order.get_status_display(),
            "total_price": float(order.total_price),
            "items": [
                {
                    "name": item.service.title,
                    "quantity": item.quantity,
                    "service_slug": item.service.slug,
                    "price": float(item.service.price_from),
                    "total_price": float(item.total_price),
                    "options": [
                        {
                            "category": option.category.title,
                            "title": option.title,
                            "price": float(option.price) if option.price is not None else None
                        } for option in item.options.all()
                    ]
                }
                for item in order.items.all()
            ]
        }
        return JsonResponse(data)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Замовлення не знайдено"}, status=404)
    except Exception as e:
        return JsonResponse({"error": "Внутрішня помилка сервера"}, status=500)

@login_required
def email_change(request):
    main_data = get_base_info(request)

    if request.method == "POST":
        new_email = (request.POST.get('email') or '').strip()

        if not new_email:
            messages.error(request, "Будь ласка, введіть нову електронну пошту.")
        elif new_email == request.user.email:
            messages.warning(request, "Це вже ваша поточна електронна пошта.")
        elif CustomUser.objects.filter(email=new_email).exists():
            messages.error(request, "Користувач з такою електронною поштою вже існує.")
        else:
            send_confirm_email(request, request.user, new_email)
            messages.success(
                request,
                f"На адресу {new_email} надіслано лист для підтвердження. "
                f"Якщо ви не бачите листа, перевірте, будь ласка, папку 'Спам'."
            )
            return redirect("user:email_change")

    return render(request, "users/email_change.html", {**main_data})

@login_required
def my_tickets(request):
    main_data = get_base_info(request)
    return render(request, 'users/my_tickets.html', {**main_data, })

@require_POST
@login_required
def add_recipient(request):
    main_data = get_base_info(request)
    form_user = ChangeUserDataForm(instance=request.user)
    form = RecipientForm(request.POST)
    if form.is_valid():
        recipient = form.save(commit=False)
        recipient.user = request.user
        recipient.save()
        messages.success(request, "Отримувача успішно додано.")
        return redirect('user:dashboard')
    else:
        for field, errors in form.errors.items():
            if field == '__all__':
                for error in errors:
                    messages.error(request, error)
        messages.error(request, "Будь ласка, перевірте правильність введених даних у формі.")
        return render(request, 'users/dashboard.html', {'recipient_form': form, 'recipient_form_edit': RecipientForm(), 'user': request.user, 'form': form_user, **main_data})

@require_POST
@login_required
def update_recipient(request):
    main_data = get_base_info(request)
    form_user = ChangeUserDataForm(instance=request.user)
    recipient_id = request.POST.get('recipient_id')
    recipient = get_object_or_404(Recipient, id=recipient_id, user=request.user)
    form = RecipientForm(request.POST, instance=recipient)
    if form.is_valid():
        form.save()
        messages.success(request, "Отримувача успішно оновлено.")
        return redirect('user:dashboard')
    else:
        for field, errors in form.errors.items():
            if field == '__all__':
                for error in errors:
                    messages.error(request, error)
        messages.error(request, "Будь ласка, перевірте правильність введених даних у формі.")
        return render(request, 'users/dashboard.html', {'recipient_form': RecipientForm(), 'recipient_form_edit': form, 'recipient_id_to_open': recipient.id, 'user': request.user, 'form': form_user, **main_data})
    
@require_POST
@login_required
def delete_recipient(request):
    recipient_id = request.POST.get('recipient_id')
    try:
        recipient = Recipient.objects.get(id=recipient_id, user=request.user)
        recipient.delete()
        messages.success(request, "Отримувача успішно видалено.")
    except Recipient.DoesNotExist:
        messages.error(request, '')
    return redirect('user:dashboard')