# Generated by Django 3.1.3 on 2021-02-10 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210209_1640'),
        ('payouts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawlsetting',
            name='doctor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.doctor'),
        ),
    ]
