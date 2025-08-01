from django.contrib import admin
from .models import CustomUser, Messages
from orders.models import Recipient

class RecipientInline(admin.TabularInline):
    model = Recipient
    extra = 0
    fields = ('last_name', 'first_name', 'middle_name', 'phone')
    readonly_fields = ()
    show_change_link = True

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'phone')
    ordering = ('id',)
    inlines = [RecipientInline]

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    search_fields = ('text', )
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = "created_at"

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['user'] = CustomUser.objects.all()
        return initial