# Generated by Django 4.2.5 on 2023-10-01 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_users_userfile_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='permissions',
            field=models.CharField(choices=[('Field Operator', 'Field Operator'), ('Base Operator', 'Base Operator'), ('Admin', 'Admin')], max_length=20),
        ),
    ]