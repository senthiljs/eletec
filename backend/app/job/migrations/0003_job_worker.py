# Generated by Django 3.0 on 2020-01-16 07:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job', '0002_job_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job', to=settings.AUTH_USER_MODEL),
        ),
    ]
