# Generated by Django 5.1.5 on 2025-01-28 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_student_enrollment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='department',
            field=models.CharField(choices=[('Business', 'Business'), ('Mathematics', 'Mathematics'), ('Engineering', 'Engineering')], max_length=50),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='class_day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')], max_length=10),
        ),
    ]