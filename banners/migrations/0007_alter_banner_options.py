# Generated by Django 5.2.4 on 2025-07-21 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0006_banner_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'verbose_name': 'Банер', 'verbose_name_plural': 'Банери'},
        ),
    ]
