# Generated by Django 5.0.2 on 2024-09-28 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_faculty_groups_alter_faculty_user_permissions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='type',
            field=models.CharField(default='Student', max_length=100),
        ),
    ]
