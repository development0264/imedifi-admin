# Generated by Django 3.1.3 on 2021-02-10 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.FloatField(),
        ),
    ]
