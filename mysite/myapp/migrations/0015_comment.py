# Generated by Django 5.0.4 on 2024-06-16 09:11

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_alter_user_userlogin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentID', models.AutoField(primary_key=True, serialize=False)),
                ('commentCreationDate', models.DateField(default=datetime.datetime.now)),
                ('commentDescription', models.TextField()),
                ('commentCreator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_comment', to='myapp.user')),
                ('commentTicket', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assigned_ticket', to='myapp.ticket')),
            ],
        ),
    ]
