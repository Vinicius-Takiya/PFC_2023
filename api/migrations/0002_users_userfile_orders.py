# Generated by Django 4.2.5 on 2023-10-01 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('militar_idt', models.CharField(max_length=30, unique=True)),
                ('permissions', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='user_files/')),
                ('description', models.TextField(blank=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.users')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_of_sending', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Aprovado', 'Aprovado'), ('Reprovado', 'Reprovado'), ('Aguardando Análise', 'Aguardando Análise')], max_length=20)),
                ('order_name', models.CharField(max_length=255)),
                ('field_comments', models.TextField(blank=True)),
                ('operator_comments', models.TextField(blank=True)),
                ('base_operator', models.ForeignKey(limit_choices_to={'permissions': 'Base Operator'}, on_delete=django.db.models.deletion.CASCADE, related_name='base_orders', to='api.users')),
                ('field_operator', models.ForeignKey(limit_choices_to={'permissions': 'Field Operator'}, on_delete=django.db.models.deletion.CASCADE, related_name='field_orders', to='api.users')),
                ('files', models.ManyToManyField(to='api.userfile')),
            ],
        ),
    ]
