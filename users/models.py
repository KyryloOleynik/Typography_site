from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from catalog.models import Service
from django.db.models import F

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError('Необхідно вказати емейл або телефон')
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email, phone=phone, password=password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email користувача", unique=True)
    phone = models.CharField("Телефон", max_length=20, unique=True, null=True, blank=True)
    is_active = models.BooleanField("Активний", default=False)
    is_staff = models.BooleanField("Права персоналу", default=False)
    favorites = models.ManyToManyField(Service, related_name="favorited_by", blank=True, verbose_name="Бажане користувача")
    first_name = models.CharField("Ім'я", max_length=150, blank=True, null=True)
    last_name = models.CharField("Прізвище", max_length=150, blank=True, null=True)
    middle_name = models.CharField("По батькові", max_length=150, blank=True, null=True)
    unread_messages = models.PositiveIntegerField("Непрочитаних повідомлень", default=0)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []

    @property
    def messages_sorted(self):
        return self.messages.order_by('-created_at')

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return self.email or self.phone or 'Користувач'
    
class Messages(models.Model):
    text = models.TextField("Текст повідомлення")
    user = models.ManyToManyField(CustomUser, related_name='messages', verbose_name="Отримувач")
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)

    class Meta:
        verbose_name = 'Повідомлення'
        verbose_name_plural = 'Повідомлення'

    def save(self, *args, **kwargs):
        if self._state.adding:
            CustomUser.objects.update(unread_messages=F('unread_messages') + 1)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Повідомлення {self.text[:30]}...."