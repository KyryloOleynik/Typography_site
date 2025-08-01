from django.db import models
from django.core.exceptions import ValidationError

class ServiceCategory(models.Model):
    image = models.ImageField("", upload_to='categories/', blank=True, null=True)
    title = models.CharField("", max_length=255)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE, verbose_name="")


    @property
    def is_main(self):
        return self.parent is None
    
    def clean(self):
        if self.parent == self and self.parent:
            raise ValidationError("Категорія не може бути дочірньою самою до себе!")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Service(models.Model):
    title = models.CharField("Назва", max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField("Опис", blank=True)
    price_from = models.DecimalField("Ціна починаючи з", max_digits=10, decimal_places=2, help_text="Мінімальна ціна від")
    image = models.ImageField("Забраження 1", upload_to='services/', blank=True, null=True)
    image2 = models.ImageField("Забраження 2", upload_to='services/', blank=True, null=True)
    image3 = models.ImageField("Забраження 3", upload_to='services/', blank=True, null=True)
    image4 = models.ImageField("Забраження 4", upload_to='services/', blank=True, null=True)
    image5 = models.ImageField("Забраження 5", upload_to='services/', blank=True, null=True)
    image6 = models.ImageField("Забраження 6", upload_to='services/', blank=True, null=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services', null=True, blank=True, verbose_name="Категорія")
    is_active = models.BooleanField("Активний", default=True)

    @property
    def images(self):
        return [self.image, self.image2, self.image3, self.image4, self.image5, self.image6]

    class Meta:
        verbose_name = "Послуга"
        verbose_name_plural = "Послуги"

    def __str__(self):
        return self.title

class ServiceOptionCategory(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='option_categories', verbose_name="Послуга")
    title = models.CharField("Тип опції", max_length=255, help_text="Тип опції, наприклад: Покриття, Формат, Кількість")

    def __str__(self):
        return f"{self.service.title} — {self.title}"

    class Meta:
        verbose_name = "Категорія опцій"
        verbose_name_plural = "Категорії опцій"

class ServiceOption(models.Model):
    category = models.ForeignKey(ServiceOptionCategory, on_delete=models.CASCADE, related_name='options', verbose_name="Категорія опції")
    title = models.CharField("Назва опції", max_length=255, help_text="Наприклад: глянцеве, A4, 100 шт.")
    price = models.DecimalField("ціна", max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.category.title}: {self.title} — {self.price} грн"

    class Meta:
        verbose_name = "Опція послуги"
        verbose_name_plural = "Опції послуг"
        ordering = ['category', 'title']