# Generated by Django 2.1.7 on 2019-03-27 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20190327_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='prescription_status',
            field=models.CharField(blank=True, choices=[('Rx', 'Rx'), ('OTC', 'OTC')], max_length=3, null=True),
        ),
    ]
