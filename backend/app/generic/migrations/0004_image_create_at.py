# Generated by Django 3.0.3 on 2020-03-12 09:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('generic', '0003_auto_20200309_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
