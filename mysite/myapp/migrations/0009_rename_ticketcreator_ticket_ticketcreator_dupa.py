# Generated by Django 5.0.4 on 2024-06-15 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_ticket_ticketdescription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='ticketCreator',
            new_name='ticketCreator_dupa',
        ),
    ]