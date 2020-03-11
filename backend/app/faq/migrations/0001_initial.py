# Generated by Django 3.0.3 on 2020-03-11 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, choices=[('en', 'En'), ('ar', 'Ar')], default='en', max_length=4, null=True)),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('content', models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
    ]
