# Generated by Django 3.2.10 on 2023-11-20 01:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayByPaypalModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_account', models.EmailField(default='', max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home_app.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='PayByMoMoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_account', models.CharField(default='', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home_app.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='PayByBankModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_bank', models.CharField(default='', max_length=20)),
                ('number_account', models.CharField(default='', max_length=20)),
                ('name_account', models.CharField(default='', max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home_app.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='LoginLogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=20)),
                ('browser', models.CharField(max_length=200)),
                ('login_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home_app.usermodel')),
            ],
        ),
    ]