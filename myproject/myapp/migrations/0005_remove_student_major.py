# Generated by Django 5.1.5 on 2025-01-27 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_major'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='major',
        ),
    ]