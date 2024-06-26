# Generated by Django 5.0.4 on 2024-05-25 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='firstname',
            new_name='userFirstName',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='lastname',
            new_name='userLastName',
        ),
        migrations.RemoveField(
            model_name='user',
            name='age',
        ),
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AddField(
            model_name='user',
            name='userID',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='user',
            name='userLogin',
            field=models.CharField(default='d', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='userPassword',
            field=models.CharField(default='d', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='userRole',
            field=models.IntegerField(default=1),
        ),
    ]
