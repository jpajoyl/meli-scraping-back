# Generated by Django 5.1.3 on 2024-11-26 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.BooleanField(default=True),
        ),
    ]
