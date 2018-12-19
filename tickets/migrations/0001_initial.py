# Generated by Django 2.1.4 on 2018-12-17 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(db_index=True, unique=True)),
                ('theme', models.CharField(db_index=True, max_length=150)),
                ('job', models.TextField(db_index=True)),
                ('term', models.DateTimeField()),
                ('status', models.BooleanField()),
                ('osn', models.CharField(max_length=150)),
                ('zakaz', models.CharField(max_length=50)),
                ('reports', models.TextField(max_length=200)),
                ('controlGK', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.IntegerField(unique=True)),
                ('username', models.CharField(max_length=50)),
                ('secondname', models.CharField(db_index=True, max_length=50)),
                ('fathname', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='customer',
            field=models.ManyToManyField(related_name='customer', to='tickets.User'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='responsible',
            field=models.ManyToManyField(related_name='responsible', to='tickets.User'),
        ),
    ]
