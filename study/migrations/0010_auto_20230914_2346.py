# Generated by Django 3.2.10 on 2023-09-14 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0009_withdrawmoneymodel_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawmoneymodel',
            name='gmail',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='withdrawmoneymodel',
            name='ttk',
            field=models.CharField(max_length=50),
        ),
    ]
