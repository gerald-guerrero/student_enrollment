# Generated by Django 5.1.5 on 2025-02-13 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_student_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SectionEnrollment',
        ),
        migrations.RemoveField(
            model_name='section',
            name='students',
        ),
    ]
