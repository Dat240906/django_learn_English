# Generated by Django 3.2.10 on 2023-11-22 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0009_alter_usermodel_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='avatar',
            field=models.ImageField(default='base-user.png', upload_to=''),
        ),
    ]
