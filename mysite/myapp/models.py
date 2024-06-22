from django.db import models
from datetime import datetime


class User(models.Model):
    userID = models.AutoField(primary_key=True)
    userLogin = models.CharField(max_length=255, unique=True)
    userPassword = models.CharField(max_length=255)
    userFirstName = models.CharField(max_length=255)
    userLastName = models.CharField(max_length=255)
    userRole = models.IntegerField(default=0)
    userPhoneNumber = models.CharField(max_length=20, blank=True)


class Ticket(models.Model):
    ticketID = models.AutoField(primary_key=True)
    ticketCreator = models.ForeignKey(User, related_name='created_tickets', on_delete=models.PROTECT)
    ticketTitle = models.CharField(max_length=255)
    ticketDescription = models.TextField(max_length=1024)
    ticketCreationDate = models.DateField(default=datetime.now)
    ticketStatus = models.IntegerField(default=0)
    ticketTechnician = models.ForeignKey(User, related_name='assigned_tickets', on_delete=models.PROTECT, null=True, blank=True)


class Comment(models.Model):
    commentID = models.AutoField(primary_key=True)
    commentTicket = models.ForeignKey(Ticket, related_name='assigned_ticket', on_delete=models.PROTECT)
    commentCreator = models.ForeignKey(User, related_name='created_comment', on_delete=models.PROTECT)
    commentCreationDate = models.DateField(default=datetime.now)
    commentDescription = models.TextField()

