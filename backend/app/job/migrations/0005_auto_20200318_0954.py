# Generated by Django 3.0.3 on 2020-03-18 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_auto_20200317_0036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='worker',
            new_name='staff',
        ),
    ]
