# Generated by Django 3.2.10 on 2023-09-11 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0007_auto_20230911_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawmoneymodel',
            name='money',
            field=models.CharField(default=0, max_length=30),
        ),
        migrations.AlterField(
            model_name='withdrawmoneymodel',
            name='stk',
            field=models.CharField(max_length=20),
        ),
    ]
