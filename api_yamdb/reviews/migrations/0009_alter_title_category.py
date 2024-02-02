# Generated by Django 3.2 on 2024-01-31 18:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_auto_20240131_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(default='Категория не указана.', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='titles', to='reviews.category', verbose_name='Категория'),
        ),
    ]
