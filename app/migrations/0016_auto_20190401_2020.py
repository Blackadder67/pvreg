# Generated by Django 2.1.7 on 2019-04-01 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_question_question_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.CharField(max_length=300),
        ),
    ]