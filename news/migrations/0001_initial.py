# Generated by Django 5.2.4 on 2025-07-25 22:18

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Контент')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('related_to_store', models.BooleanField(default=False, help_text='Позначте, якщо новина стосується товарів або подій магазину.', verbose_name="Пов'язано з магазином")),
                ('image', models.ImageField(upload_to='news/', verbose_name='Зображення')),
            ],
            options={
                'verbose_name': 'Новина',
                'verbose_name_plural': 'Новини',
            },
        ),
    ]
