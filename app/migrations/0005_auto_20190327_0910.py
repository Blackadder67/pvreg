# Generated by Django 2.1.7 on 2019-03-27 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20190326_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='fname_rus',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='lname_rus',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
