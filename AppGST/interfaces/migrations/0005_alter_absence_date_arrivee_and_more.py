# Generated by Django 4.2.11 on 2024-04-01 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interfaces', '0004_alter_membrepersonnel_statut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absence',
            name='date_arrivee',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='absence',
            name='heure_arrivee',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='absence',
            name='personnel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interfaces.membrepersonnel'),
        ),
    ]
