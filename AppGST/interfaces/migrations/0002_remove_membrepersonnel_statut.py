# Generated by Django 4.2.11 on 2024-03-30 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interfaces', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membrepersonnel',
            name='statut',
        ),
    ]
