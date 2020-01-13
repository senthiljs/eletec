# Generated by Django 3.0 on 2020-01-12 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20191116_1201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='officeNo',
            new_name='office_no',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='villaNo',
            new_name='villa_no',
        ),
        migrations.AlterField(
            model_name='address',
            name='model',
            field=models.IntegerField(blank=True, choices=[(1, 'Personal'), (2, 'Company')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='style',
            field=models.IntegerField(blank=True, choices=[(1, 'Apartment'), (2, 'Villa')], default=1, null=True),
        ),
    ]