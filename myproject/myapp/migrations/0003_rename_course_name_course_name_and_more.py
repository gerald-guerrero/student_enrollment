# Generated by Django 5.1.5 on 2025-01-27 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_schedule_class_day'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='course_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='semester_enrolled',
            new_name='semester',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='year_enrolled',
            new_name='year',
        ),
    ]
