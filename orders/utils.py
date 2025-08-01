from decimal import Decimal
from django.conf import settings
from catalog.models import Service, ServiceOption
import copy
from catalog.quantity_choices import quantity_choices 
from datetime import datetime

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

        if 'cart_created_at' not in self.session:
            self.session['cart_created_at'] = datetime.now().isoformat()

    def get_created_date(self):
        created_iso = self.session.get('cart_created_at')
        if created_iso:
            return datetime.fromisoformat(created_iso)
        return None

    def save(self):
        self.session.modified = True

    def add(self, service, quantity=1, options=None, resetQuantity=False):
        if options is None:
            options = []

        service_id = str(service.id)
        option_ids = sorted(map(str, options))
        option_key = '-'.join(option_ids)
        cart_key = f"{service_id}:{option_key}" if option_ids else service_id

        base_price = service.price_from or Decimal('0.00')
        options_price = sum((option.price or Decimal('0.00')) for option in ServiceOption.objects.filter(id__in=options))
        total_unit_price = base_price + options_price

        if cart_key not in self.cart:
            self.cart[cart_key] = {
                'service_id': service_id,
                'quantity': 0,
                'price_per_item': str(total_unit_price),
                'options': option_ids
            }

        if resetQuantity:
            self.cart[cart_key]['quantity'] = quantity
        else:
            self.cart[cart_key]['quantity'] += quantity

        self.save()

    def remove(self, service_id_with_options):
        if service_id_with_options in self.cart:
            del self.cart[service_id_with_options]
            self.save()

    def clear(self):
        self.session.pop(settings.CART_SESSION_ID, None)
        self.session.pop('cart_created_at', None)
        self.save()

    def __iter__(self):
        cart = copy.deepcopy(self.cart)
        service_ids = [v['service_id'] for v in cart.values()]
        services = Service.objects.filter(id__in=service_ids)
        service_map = {str(service.id): service for service in services}

        for key, item in cart.items():
            service = service_map.get(item['service_id'])
            if not service:
                continue

            item['service'] = service
            item['price_per_item'] = Decimal(item['price_per_item'])
            item['unit_price'] = item['price_per_item']
            item['total_price'] = item['unit_price'] * (Decimal(item['quantity']) / Decimal(quantity_choices[0]))
            item['options'] = ServiceOption.objects.filter(id__in=item.get('options', []))
            yield item

    def count(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total = Decimal('0.00')
        for item in self.cart.values():
            price_per_item = Decimal(item['price_per_item'])
            quantity = Decimal(item['quantity'])
            total += price_per_item * (quantity / Decimal(quantity_choices[0]))
        return total
    
    def get_items(self):
        """Вернуть все позиции корзины как словари"""
        for item in self:
            yield item

    def contains_similar_item(self, other_item):
        """Проверяет, есть ли в корзине item с таким же service, quantity и options"""
        for item in self:
            if (
                item['service'].id == other_item['service'].id and
                item['quantity'] == other_item['quantity'] and
                set(opt.id for opt in item['options']) == set(opt.id for opt in other_item['options'])
            ):
                return True
        return False