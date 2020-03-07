# Generated by Django 3.0.3 on 2020-03-07 13:17

import app.order.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(blank=True, choices=[(0, 'New'), (1, 'Confirm'), (2, 'Complete'), (3, 'Pending'), (4, 'Cancel'), (5, 'Delete')], default=0, null=True)),
                ('service', models.IntegerField(blank=True, choices=[(0, 'Ac'), (1, 'Electrical'), (2, 'Plumbing'), (3, 'Cleaning')], default=0, null=True)),
                ('main_info', models.IntegerField(blank=True, default=0, null=True)),
                ('sub_info', models.IntegerField(blank=True, default=0, null=True)),
                ('other_info', models.CharField(blank=True, max_length=256, null=True)),
                ('from_date', models.DateTimeField(blank=True, null=True)),
                ('to_date', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(blank=True, default=app.order.models.random_string, max_length=4, null=True)),
                ('address', models.CharField(blank=True, max_length=128, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lng', models.FloatField(blank=True, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('change_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'order',
            },
        ),
    ]
