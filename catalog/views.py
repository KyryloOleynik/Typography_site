from django.shortcuts import render, redirect
from core.utils import get_base_info
from .models import ServiceCategory, Service, ServiceOption
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from decimal import Decimal
from orders.utils import Cart
from .quantity_choices import quantity_choices
from django.http import JsonResponse

def get_all_subcats(target_category):
    subcategories = list(target_category.children.all())
    for subcategory in target_category.children.all():
        subcategories.extend(get_all_subcats(subcategory))
    return subcategories

def get_all_parent_categories(category):
    all_categories = [category]
    current = category.parent

    while current:
        all_categories.append(current)
        current = current.parent

    return list(reversed(all_categories))
    

# Create your views here.
def category_detail(request, slug):
    main_data = get_base_info(request)
    target_category = get_object_or_404(ServiceCategory, slug=slug)
    all_categories = get_all_subcats(target_category)
    all_categories.append(target_category)
    services = Service.objects.filter(category__in=all_categories)
    category_path = get_all_parent_categories(target_category)

    return render(request, 'catalog/category_detail.html', {'target_category': target_category, 'services': services, 'category_path': category_path, **main_data})

def service_detail(request, slug):
    main_data = get_base_info(request)
    target_service = Service.objects.get(slug=slug)
    category_path = get_all_parent_categories(target_service.category)

    return render(request, 'catalog/service_detail.html', {'target_service': target_service, 'category_path': category_path, 'quantity_choices': quantity_choices, **main_data})

@require_POST
def add_to_cart(request, slug):
    service = get_object_or_404(Service, slug=slug)
    quantity = request.POST.get("tirazh")

    try:
        quantity = int(quantity)
        if quantity <= 0 or quantity not in quantity_choices:
            raise ValueError
    except (TypeError, ValueError):
        messages.error(request, "Невірно вказано тираж.")
        return redirect('catalog:service_detail', slug=slug)

    option_ids = [
        int(value) for key, value in request.POST.items()
        if key.startswith("option_")
    ]

    cart = get_base_info(request).get('cart')

    if isinstance(cart, Cart):
        cart.add(service=service, quantity=quantity, options=option_ids)
        messages.success(request, f"Послугу «{service.title}» додано до кошика.")
    else:

        existing_item = None
        for item in cart.items.all():
            if item.service == service and item.options.count() == len(option_ids) and \
               set(item.options.values_list('id', flat=True)) == set(option_ids):
                existing_item = item
                break

        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            new_item = cart.items.create(service=service, quantity=quantity)
            new_item.options.set(option_ids)

        messages.success(request, f"Послугу «{service.title}» додано до вашого замовлення.")

    return redirect('catalog:service_detail', slug=slug)


@require_POST
def remove_from_cart(request, slug):
    service = get_object_or_404(Service, slug=slug)
    cart = get_base_info(request).get('cart')

    posted_option_ids = set(
        int(value) for key, value in request.POST.items() if key.startswith("option_")
    )

    try:
        quantity = int(request.POST.get("tirazh"))
    except (TypeError, ValueError):
        quantity = None

    if isinstance(cart, Cart):
        keys_to_remove = []

        for key, item in cart.cart.items():
            item_option_ids = set(map(int, item.get('options', [])))
            if (
                str(item.get('service_id')) == str(service.id)
                and set(item_option_ids) == posted_option_ids
                and (item.get('quantity') is None or item.get('quantity') == quantity)
            ):
                keys_to_remove.append(key)

        for key in keys_to_remove:
            cart.remove(key)

        if keys_to_remove:
            return JsonResponse({"message": f"Послугу «{service.title}» видалено з корзини.", "new_total_price": cart.get_total_price()})
        else:
            return JsonResponse({"error": "Вказана позиція не знайдена у корзині."}, status=404)

    else:
        items = cart.items.filter(service=service)
        found = False

        for item in items:
            item_option_ids = set(item.options.values_list('id', flat=True))
            if (
                item_option_ids == posted_option_ids
                and (item.quantity is None or item.quantity == quantity)
            ):
                item.delete()
                found = True

        if found:
            return JsonResponse({"message": f"Послугу «{service.title}» видалено з вашого замовлення.", "new_total_price": cart.total_price})
        else:
            return JsonResponse({"error": "Вказана позиція не знайдена у вашому замовленні."}, status=404)