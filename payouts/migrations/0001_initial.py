# Generated by Django 3.1.3 on 2021-02-09 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_auto_20210201_0840'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawlSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paypal_id', models.CharField(max_length=512, verbose_name='paypal id')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.doctor')),
            ],
        ),
    ]
