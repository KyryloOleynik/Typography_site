# Generated by Django 5.2.4 on 2025-07-25 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0007_alter_banner_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Створено'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(upload_to='banners/', verbose_name='Баннер'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='link',
            field=models.CharField(blank=True, verbose_name='Посилання на банері'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='text',
            field=models.TextField(blank=True, verbose_name='Текст банеру'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='title',
            field=models.CharField(blank=True, max_length=255, verbose_name='Заголовок'),
        ),
    ]
