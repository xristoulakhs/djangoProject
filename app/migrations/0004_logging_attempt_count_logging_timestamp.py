# Generated by Django 4.1.5 on 2023-01-17 16:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_logging'),
    ]

    operations = [
        migrations.AddField(
            model_name='logging',
            name='attempt_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='logging',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]