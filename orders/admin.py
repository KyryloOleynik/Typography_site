from django.contrib import admin
from .models import Order, OrderItem, Recipient

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)
    autocomplete_fields = ['service']
    show_change_link = False

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)
    autocomplete_fields = ['service']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipient_display', 'status', 'created_at', 'total_price_display')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'id', 'recipient__last_name')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at', 'total_price_display')
    ordering = ['-created_at']
    date_hierarchy = "created_at"
    autocomplete_fields = ['user', 'recipient']

    def total_price_display(self, obj):
        return f"{obj.total_price:.2f} грн"
    total_price_display.short_description = "Сума замовлення"

    def recipient_display(self, obj):
        if obj.recipient:
            return str(obj.recipient)
        return "-"
    recipient_display.short_description = "Отримувач"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'service', 'quantity', 'total_price_display')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'service__title')
    autocomplete_fields = ['order', 'service']

    def total_price_display(self, obj):
        return f"{obj.total_price:.2f} грн"
    total_price_display.short_description = "Сума"


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'last_name', 'first_name', 'phone')
    search_fields = ('last_name', 'first_name', 'phone', 'user__email')
    autocomplete_fields = ['user']
