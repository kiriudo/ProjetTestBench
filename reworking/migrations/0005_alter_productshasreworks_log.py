# Generated by Django 4.1.1 on 2022-10-12 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reworking', '0004_alter_productshasreworks_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productshasreworks',
            name='log',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='reworking.logs'),
        ),
    ]
