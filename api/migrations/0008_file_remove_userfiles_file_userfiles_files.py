# Generated by Django 4.2.5 on 2023-10-09 02:14

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_customuser_alter_orders_base_operator_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=api.models.user_file_upload_path)),
            ],
        ),
        migrations.RemoveField(
            model_name='userfiles',
            name='file',
        ),
        migrations.AddField(
            model_name='userfiles',
            name='files',
            field=models.ManyToManyField(to='api.file'),
        ),
    ]
