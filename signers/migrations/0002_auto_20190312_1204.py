# Generated by Django 2.1.2 on 2019-03-12 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signer',
            name='signDate',
            field=models.DateField(null=True),
        ),
    ]
