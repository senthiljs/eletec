# Generated by Django 3.0 on 2020-01-13 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20200113_1247'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VerifyCode',
        ),
    ]