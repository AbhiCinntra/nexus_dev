# Generated by Django 4.0.3 on 2024-02-01 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cards', '0003_cards_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cards',
            name='Default',
            field=models.IntegerField(default=0),
        ),
    ]
