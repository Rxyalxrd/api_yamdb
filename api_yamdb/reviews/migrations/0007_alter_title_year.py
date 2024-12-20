# Generated by Django 3.2 on 2024-01-30 18:13

import reviews.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_alter_title_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(default=1, help_text='Год создания', validators=[reviews.validators.validate_year], verbose_name='Год создания'),
            preserve_default=False,
        ),
    ]
