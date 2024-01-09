# Generated by Django 3.2.10 on 2023-12-21 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earn_money_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftCodeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=20, unique=True)),
                ('value', models.FloatField(default=0.0)),
            ],
        ),
    ]