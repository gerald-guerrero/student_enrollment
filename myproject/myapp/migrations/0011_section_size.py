# Generated by Django 5.1.5 on 2025-01-30 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_alter_course_credits_alter_section_building_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='size',
            field=models.IntegerField(default=50, help_text='Provide the maximum amount of students that can register for this section'),
        ),
    ]
