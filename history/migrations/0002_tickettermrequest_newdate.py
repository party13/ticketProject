# Generated by Django 2.1.5 on 2019-03-10 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickettermrequest',
            name='newDate',
            field=models.DateField(default=None),
        ),
    ]