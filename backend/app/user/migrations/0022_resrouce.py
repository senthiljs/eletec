# Generated by Django 3.0.3 on 2020-03-02 18:37

import app.user.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_remove_address_officeno'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resrouce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(blank=True, default='unknow', max_length=64, null=True)),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=app.user.models.content_file_name)),
                ('image_ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resource', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'resource',
            },
        ),
    ]
