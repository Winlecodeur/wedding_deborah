# Generated by Django 5.1.6 on 2025-03-20 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_invite_guest_count_table_capacite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='statut',
            field=models.CharField(choices=[('COUPLE', 'couple'), ('MR', 'mr'), ('MADAME', 'madame')], default='COUPLE', max_length=11),
        ),
    ]
