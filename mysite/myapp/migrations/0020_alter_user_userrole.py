# Generated by Django 5.0.4 on 2024-06-16 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_alter_user_userrole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userRole',
            field=models.IntegerField(default=0),
        ),
    ]