# Generated by Django 3.2.10 on 2023-11-20 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EarnMoneyYoutubeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_of_job', models.FloatField(default=0)),
                ('number_job', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home_app.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='EarnMoneyWeb1sModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_of_job', models.FloatField(default=0)),
                ('number_job', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home_app.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='EarnMoneyTiktokModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_of_job', models.FloatField(default=0)),
                ('number_job', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home_app.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='EarnMoneyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_in_day', models.FloatField(default=0)),
                ('money_in_month', models.FloatField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home_app.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='EarnMoneyFacebookModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_of_job', models.FloatField(default=0)),
                ('number_job', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home_app.usermodel')),
            ],
        ),
    ]
