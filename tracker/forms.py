from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User

from tracker.models import Task, Project

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = [
        'Project_name',
        'Description'
        ]

class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
        'Project',
        'Category',
        'Task_Name',
        'Goal_Date',
        'Status',
        'Notes',
        'Short_list',
        ]
        widgets = {
            'Goal_Date':DateInput(),
        }
    def __init__(self, user, *args, **kwargs):
       super(CreateTaskForm, self).__init__(*args, **kwargs)
       self.fields['Project'] = forms.ModelChoiceField(
       queryset=Project.objects.filter(user = user))

class EditTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = [
        'isDeleted',
        'user','Complete_Date'
        ]
        widgets = {
            'Goal_Date':DateInput(),
        }
    def __init__(self, user, *args, **kwargs):
       super(EditTaskForm, self).__init__(*args, **kwargs)
       self.fields['Project'] = forms.ModelChoiceField(
       queryset=Project.objects.filter(user = user))
