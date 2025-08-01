from django.contrib import admin
from .models import Ticket, TicketMessage

# Register your models here.
class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 1
    autocomplete_fields = ['ticket']
    readonly_fields = ['created_at']
    ordering = ['created_at']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs['initial'] = request.user
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class IsWaitingAnswer(admin.SimpleListFilter):
    title = 'Чекає на відповідь'
    parameter_name = 'is_waiting_answer'

    def lookups(self, request, model_admin):
        return [('yes', 'Так')]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            ticket_ids = [
                ticket.id for ticket in queryset
                if ticket.status == 'new' and (
                    (ticket.user and ticket.last_message and not ticket.last_message.user.is_superuser and not ticket.last_message.user.is_staff)
                    or
                    (not ticket.user and ticket.last_message and ticket.last_message.user is None and ticket.session_key)
                )
            ]
            
            return queryset.filter(id__in=ticket_ids)
        return queryset
    
class SessionKeyExistsFilter(admin.SimpleListFilter):
    title = 'Session Key існує'
    parameter_name = 'session_key_exists'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Є'),
            ('no', 'Немає'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(session_key__isnull=False).exclude(session_key='')
        if self.value() == 'no':
            return queryset.filter(session_key__isnull=True) | queryset.filter(session_key='')
        return queryset

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'last_message_text')
    list_filter = ('status', 'created_at', IsWaitingAnswer, SessionKeyExistsFilter)
    search_fields = ('user__phone', 'user__email')
    inlines = [TicketMessageInline]
    autocomplete_fields = ['user']
    readonly_fields = ['created_at']

    def last_message_text(self, obj):
        last = obj.messages.order_by('-created_at').first()
        return last.message if last else None
    last_message_text.short_description = "Останнє повідомлення"

@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'user', 'created_at', 'short_message')
    list_filter = ('created_at', 'user')
    search_fields = ('message', 'user__username', 'user__email')
    readonly_fields = ('created_at',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs['initial'] = request.user
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def short_message(self, obj):
        return obj.message[:50] + ('...' if len(obj.message) > 50 else '')
    short_message.short_description = 'Повідомлення'