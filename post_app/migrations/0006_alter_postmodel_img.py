# Generated by Django 3.2.10 on 2023-11-21 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0005_alter_postmodel_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='img',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
