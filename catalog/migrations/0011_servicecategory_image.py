# Generated by Django 5.2.4 on 2025-07-21 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_remove_servicecategory_parents_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicecategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='categories/'),
        ),
    ]
