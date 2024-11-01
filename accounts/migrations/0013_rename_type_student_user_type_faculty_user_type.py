# Generated by Django 5.0.2 on 2024-09-28 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_student_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='type',
            new_name='user_type',
        ),
        migrations.AddField(
            model_name='faculty',
            name='user_type',
            field=models.CharField(default='teacher', max_length=100),
        ),
    ]