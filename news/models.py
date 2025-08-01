from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class News(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    content = CKEditor5Field("Контент", config_name='extends')
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    related_to_store = models.BooleanField(default=False, verbose_name="Пов'язано з магазином", help_text="Позначте, якщо новина стосується товарів або подій магазину.")
    image = models.ImageField("Зображення", upload_to='news/')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Новина"
        verbose_name_plural = "Новини"

    def __str__(self):
        return self.title
