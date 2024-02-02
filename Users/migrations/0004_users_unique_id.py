# Generated by Django 4.0.3 on 2024-01-25 06:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_users_country_code_alter_users_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='Unique_Id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]