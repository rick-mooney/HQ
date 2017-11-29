from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django import forms

class Company(models.Model):
    name = models.CharField(max_length=200)
    size = models.IntegerField(blank=True)
    location = models.CharField(max_length=100,blank=True)
    ceo = models.CharField(max_length=50,blank=True)
    industry = models.CharField(max_length=50,blank=True)
    incorporated = models.CharField(max_length=4,blank=True)
    other_notes = models.TextField(blank=True)
    isDeleted = models.BooleanField(default=False, blank=True)
    user = models.ForeignKey(User)
    def __str__(self):
        return self.name

class Application(models.Model):
    status_choices = (
        ('NS','Not Started'),
        ('IP','In Progress'),
        ('OH','On Hold'),
        ('CO','Complete'),
    )
    app_status = models.CharField(max_length=2,choices=status_choices)
    position = models.CharField(max_length=255)
    company = models.ForeignKey(Company)
    applied_date = models.DateField(null=True)
    isDeleted = models.BooleanField(default=False, blank=True)
    user = models.ForeignKey(User)
    def __str__(self):
        return self.position

class Contact(models.Model):
    name = models.CharField(max_length=255,blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=25,blank=True)
    App = models.ForeignKey(Application)
    isDeleted = models.BooleanField(default=False, blank=True)

class Questions(models.Model):
    question = models.CharField(max_length=255)
    category = models.CharField(max_length=25)
    user = models.ForeignKey(User)
    isDeleted = models.BooleanField(default=False, blank=True)
    def __str__(self):
        return self.question

class Ask(models.Model): #joining table
    question = models.ForeignKey(Questions)
    app = models.ForeignKey(Application)
    answer = models.TextField(blank=True)
    isDeleted = models.BooleanField(default=False, blank=True)

class Notes(models.Model):
    note = models.TextField(blank=True)
    note_date = models.DateField(auto_now=True)
    App = models.ForeignKey(Application,null=True)
    isDeleted = models.BooleanField(default=False, blank=True)

class Resources(models.Model):
    type_choices = (
        ('LI','Linkedin'),
        ('WS','Website'),
        ('GD','Glassdoor'),
        ('OT','Other'),
    )
    resource_type = models.CharField(max_length=2,choices=type_choices)
    resource = models.URLField(max_length=200)
    App = models.ForeignKey(Application,null=True)
    isDeleted = models.BooleanField(default=False, blank=True)
