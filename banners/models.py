from django.db import models

# Create your models here.
class Banner(models.Model):
    title = models.CharField("Заголовок", max_length=255, blank=True)
    text = models.TextField("Текст банеру", blank=True)
    image = models.ImageField("Баннер", upload_to='banners/')
    link = models.CharField("Посилання на банері", blank=True)
    created_at = models.DateTimeField("Створено", auto_now_add=True)
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Банер'
        verbose_name_plural = 'Банери'