# Generated by Django 5.0.2 on 2024-10-06 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_course_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.CharField(choices=[('Development', 'Development'), ('Business', 'Business'), ('Finance and Accounting ', 'Finance and Accounting '), ('IT & Software', 'IT & Software'), ('Marketing', 'Marketing'), ('Photography', 'Photography'), ('Health and Fitness', 'Helath and Fitness'), ('Music', 'Music')], default='Choose Your Category', max_length=200),
        ),
    ]
