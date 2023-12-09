# Generated by Django 3.2.10 on 2023-11-20 07:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home_app', '0007_auto_20231120_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.CharField(max_length=500)),
                ('img', models.ImageField(upload_to='')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('num_like', models.IntegerField(default=0)),
                ('num_comment', models.IntegerField(default=0)),
                ('num_share', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home_app.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_comment', models.CharField(max_length=200)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post_app.postmodel')),
                ('user_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home_app.usermodel')),
            ],
        ),
    ]