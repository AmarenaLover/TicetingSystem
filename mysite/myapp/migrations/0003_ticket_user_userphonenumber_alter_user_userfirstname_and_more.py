# Generated by Django 5.0.4 on 2024-05-25 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_rename_firstname_user_userfirstname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticketID', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('ticketCreator', models.IntegerField()),
                ('ticketTitle', models.CharField(default='No data', max_length=255)),
                ('ticketDescription', models.CharField(default='No data', max_length=255)),
                ('ticketCreationDate', models.DateField()),
                ('ticketTechnician', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='userPhoneNumber',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='userFirstName',
            field=models.CharField(default='No data', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='userLastName',
            field=models.CharField(default='No data', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='userLogin',
            field=models.CharField(default='No data', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='userPassword',
            field=models.CharField(default='No data', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='userRole',
            field=models.IntegerField(default=0),
        ),
    ]
