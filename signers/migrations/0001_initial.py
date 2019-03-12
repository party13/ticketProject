# Generated by Django 2.1.2 on 2019-03-12 09:56

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
            name='Signer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isSigned', models.BooleanField(default=False)),
                ('signDate', models.DateField()),
                ('ticket', models.ForeignKey(on_delete='CASCADE', related_name='ticket_to_sign', to='tickets.Ticket', verbose_name='карточка')),
                ('user', models.ForeignKey(on_delete='CASCADE', related_name='signing_user', to=settings.AUTH_USER_MODEL, verbose_name='визирующий')),
            ],
        ),
    ]
