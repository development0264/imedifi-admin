# Generated by Django 3.1.3 on 2021-02-09 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210201_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='files',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.file'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='certificate',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.certificate'),
        ),
    ]
