from django.db import models
from django.conf import settings

# Create your models here.
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новий'),
        ('closed', 'Закритий'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets',
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Тікет #{self.id} ({self.user.first_name})"
        return f"Тікет #{self.session_key} (Гість)"

    @property 
    def topic(self):
        return self.messages.order_by('created_at').first()

    @property
    def last_message(self):
        return self.messages.order_by('-created_at').first()

    class Meta:
        verbose_name = 'Тікет'
        verbose_name_plural = 'Тікети'
        ordering = ['-created_at']

class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(verbose_name="Повідомлення")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Повідомлення'
        verbose_name_plural = 'Повідомлення'
        ordering = ['created_at'] 

    def __str__(self):
        if self.user:
            return f"{self.user.first_name}: {self.message[:30]}..."
        return f"{self.ticket.session_key} (Гість): {self.message[:30]}..."
    
    @property
    def created_at_iso(self):
        return self.created_at.isoformat()
    
    @property
    def role(self):
        return 'support' if self.user and (self.user.is_staff or self.user.is_superuser) else 'user'