# Generated by Django 3.1.4 on 2021-01-05 18:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_borrow_return_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrow',
            name='return_date',
        ),
        migrations.AddField(
            model_name='borrow',
            name='date_return',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
