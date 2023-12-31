# Generated by Django 3.2.10 on 2023-12-23 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earn_money_app', '0002_giftcodemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteRewardTempModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint', models.CharField(max_length=50)),
                ('is_completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='giftcodemodel',
            name='code',
            field=models.CharField(default='', max_length=30, unique=True),
        ),
    ]
