# Generated by Django 5.0.4 on 2024-06-30 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='verification',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='emailid',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='phone',
            field=models.IntegerField(unique=True),
        ),
    ]
