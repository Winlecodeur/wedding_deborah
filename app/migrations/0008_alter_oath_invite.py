# Generated by Django 5.1.6 on 2025-03-20 17:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_oath_invite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oath',
            name='invite',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='oaths', to='app.invite'),
        ),
    ]
