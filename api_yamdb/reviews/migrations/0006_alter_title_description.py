# Generated by Django 3.2 on 2024-01-30 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_alter_title_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.CharField(blank=True, default=1, max_length=255, verbose_name='Описание'),
            preserve_default=False,
        ),
    ]
