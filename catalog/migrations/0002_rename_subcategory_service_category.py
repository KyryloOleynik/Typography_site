# Generated by Django 5.2.4 on 2025-07-20 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='subcategory',
            new_name='category',
        ),
    ]
