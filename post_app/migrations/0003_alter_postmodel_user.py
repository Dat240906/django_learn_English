# Generated by Django 3.2.10 on 2023-11-20 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0007_auto_20231120_1120'),
        ('post_app', '0002_rename_user_comment_commentmodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home_app.usermodel'),
        ),
    ]
