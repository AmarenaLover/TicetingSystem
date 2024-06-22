# Generated by Django 5.0.4 on 2024-06-15 12:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_ticket_ticketcreator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticketTechnician',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assigned_tickets', to='myapp.user'),
        ),
    ]