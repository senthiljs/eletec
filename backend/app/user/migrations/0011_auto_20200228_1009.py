# Generated by Django 3.0 on 2020-02-28 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20200228_0025'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='skill',
            unique_together={('skill', 'user')},
        ),
    ]