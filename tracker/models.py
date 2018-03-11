
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django import forms

class Project(models.Model):
    Project_name = models.CharField(max_length=255)
    Description = models.CharField(max_length=255,blank=True)
    CreateDate = models.DateField(auto_now_add=True)
    count_tasks = models.PositiveIntegerField(null=True, default=0)
    count_complete = models.PositiveIntegerField(null=True, default=0)
    percent_overdue = models.PositiveIntegerField(null=True, default=0)
    percent_complete = models.PositiveIntegerField(null=True, default=0)
    user = models.ForeignKey(User)
    def __str__(self):
        return self.Project_name

class ProjectMember(models.Model):
    ProjectId = models.ForeignKey(Project)
    Owner = models.ForeignKey(User, related_name='own')
    Member = models.ForeignKey(User, related_name='mem', null=True)

class Task(models.Model):
    status_choices = (
        ('NS','Not Started'),
        ('IP','In Progress'),
        ('OH','On Hold'),
        ('CO','Complete'),
    )
    Task_Name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    Project = models.ForeignKey(Project, related_name="tasks")
    Category = models.CharField(max_length=255, blank=True )
    Short_list = models.BooleanField(default=False, blank=True)
    Status = models.CharField(max_length=2, choices = status_choices)
    Start_Date = models.DateField(auto_now_add=True)
    Modified_Date = models.DateField(auto_now=True)
    Goal_Date = models.DateField(blank=True, null=True)
    Notes = models.TextField(blank=True)
    isDeleted = models.BooleanField(default=False, blank=True)
    Complete_Date = models.DateField(blank=True, null=True)
