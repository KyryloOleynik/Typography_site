from django.db import models
from decimal import Decimal
from users.models import CustomUser
from catalog.models import Service, ServiceOption
from catalog.quantity_choices import quantity_choices
from PFB_Typography.settings import AUTH_USER_MODEL

class Recipient(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipients')
    last_name = models.CharField("Прізвище", max_length=100)
    first_name = models.CharField("Ім'я", max_length=100)
    middle_name = models.CharField("По батькові", max_length=100, blank=True)
    phone = models.CharField("Телефон", max_length=20)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.phone})"
    
    class Meta:
        verbose_name = 'Отримувач'
        verbose_name_plural = 'Отримувачі'

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новий'),
        ('processing', 'В обробці'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', verbose_name="Користувач")
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    updated_at = models.DateTimeField("Дата оновлення", auto_now=True)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='new')
    address = models.CharField("Адреса доставки", max_length=255, null=True, blank=True)
    delivery_method = models.CharField("Метод доставки", max_length=100, null=True, blank=True)
    payment_method = models.CharField("Метод оплати", max_length=100, null=True, blank=True)
    recipient = models.ForeignKey(Recipient, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Отримувач")

    def __str__(self):
        return f"Замовлення #{self.pk} від {self.user.email}"

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Замовлення")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Послуга")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Тираж")
    options = models.ManyToManyField(ServiceOption, blank=True, verbose_name="Обрані опції")

    @property
    def base_price(self):
        return self.service.price_from or Decimal('0.00')

    def get_options_price(self):
        return sum((opt.price or Decimal('0.00')) for opt in self.options.all())

    @property
    def unit_price(self):
        return self.base_price + self.get_options_price()

    @property
    def total_price(self):
        return self.unit_price * (Decimal(self.quantity) / Decimal(quantity_choices[0]))

    def __str__(self):
        return f"{self.service.title} × {self.quantity}"

    class Meta:
        verbose_name = 'Позиція замовлення'
        verbose_name_plural = 'Позиції замовлення'