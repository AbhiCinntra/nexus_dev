# Generated by Django 4.0.3 on 2024-01-25 06:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Contacts', '0002_contacts_country_code_alter_contacts_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='Unique_Id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
