# Generated by Django 5.1.6 on 2025-03-19 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='photo',
            field=models.ImageField(blank=True, default='photos/wedding inv debo code QR 004 1.jpg', null=True, upload_to='photos_invites/'),
        ),
    ]
