# Generated by Django 2.1.2 on 2019-03-04 13:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tickets', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('when', models.DateTimeField()),
                ('ticket', models.ForeignKey(on_delete='CASCADE', related_name='ticket', to='tickets.Ticket', verbose_name='карточка')),
                ('user', models.ForeignKey(on_delete='CASCADE', related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
        ),
    ]