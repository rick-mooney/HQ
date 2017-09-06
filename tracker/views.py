from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy

import csv
from datetime import datetime, timedelta, time

from tracker.models import Task, Project
from tracker.forms import (CreateTaskForm, CreateProjectForm)


class TaskView(TemplateView):
    template_name = 'task.html'

    def get(self, request):
        search_query = request.GET.get('search', None)
        user=request.user

        if search_query == 'Completed_tasks':
            query = Task.objects.all().filter(Status="CO", user=user).order_by('Goal_Date')
            args = {'query': query,'SearchWord':search_query}
            return render(request, self.template_name, args)

        elif search_query == 'Deleted_tasks':
            query = Task.objects.all().filter(isDeleted=True, user=user).order_by('Goal_Date')
            args = {'query': query,'SearchWord':search_query}
            return render(request, self.template_name, args)

        elif search_query == 'short_list_tasks':
            query = Task.objects.all().filter(Short_list=True, user=user).order_by('Goal_Date')
            args = {'query': query,'SearchWord':search_query}
            return render(request, self.template_name, args)

        elif search_query == 'Overdue_tasks':
            query = Task.objects.all().filter(Goal_Date__lt=datetime.now().date(), user=user).exclude(Status="CO").order_by('Project')
            args = {'query': query,'SearchWord':search_query}
            return render(request, self.template_name, args)

        elif search_query == 'Today_tasks':
            query = Task.objects.all().filter(Goal_Date=datetime.now().date(), user=user).exclude(Status="CO").order_by('Project')
            args = {'query': query,'SearchWord':search_query}
            return render(request, self.template_name, args)

        elif search_query == 'This_week':
            query = Task.objects.all().filter(Goal_Date__lte=datetime.now().date()+timedelta(7), Goal_Date__gte=datetime.now().date(), user=user).exclude(Status="CO").order_by('Goal_Date')
            args = {'query': query,'SearchWord':search_query}
            return render(request, self.template_name, args)

        elif search_query == 'This_month':
            query = Task.objects.all().filter(Goal_Date__lte=datetime.now().date()+timedelta(31), Goal_Date__gte=datetime.now().date(), user=user).exclude(Status="CO").order_by('Goal_Date')
            args = {'query': query,'SearchWord':search_query}
            return render(request, self.template_name, args)

        elif search_query != None:
            query = (Task.objects.all().filter(Task_Name__icontains=search_query, user=user).exclude(Status="CO").order_by('Goal_Date')) \
            | (Task.objects.all().filter(Notes__icontains=search_query, user=user).exclude(Status="CO").order_by('Goal_Date'))
            args = {'query': query,'SearchWord':search_query}
            return render(request, self.template_name, args)

        else:
            query = Task.objects.all().filter(user=user).exclude(Status="CO").order_by('Goal_Date')
            args = {'query': query}
            return render(request, self.template_name, args)

    def post(self, request):
        search_query = request.GET.get('search', None)
        query = Task.objects.all().filter(Task_Name__icontains=search_query).order_by('Goal_Date').exclude(Status="CO")
        args = {'query': query, 'SearchWord':search_query}
        return render(request, self.template_name, args)

class ProjectView(TemplateView):
    template_name = 'project.html'
    #user = TemplateView.request.user

    def get(self, request):
        user = request.user
        # search_query = request.GET.get('search', None)
        # if search_query != None:
        #     query = Project.objects.all().filter(Project_Name__icontains=search_query)
        #
        #     args = {'query': query,'SearchWord':search_query}
        #     return render(request, self.template_name, args)
        # else:
        query = Project.objects.all().filter(user=user)
        args = {'query': query}
        return render(request, self.template_name, args)


class CreateProject(TemplateView):
    template_name = 'create_project.html'

    def get(self, request):
        form = CreateProjectForm
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('tracker:project')

        args = {'form':form}
        return render(request, self.template_name, args)


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('tracker:project')


class ProjectEdit(UpdateView):
    model = Project
    fields = '__all__'
    success_url = reverse_lazy('tracker:project')


class ProjectListView(TemplateView):
    template_name = 'task.html'

    def get(self, request, **kwargs):
        user = request.user
        project = self.kwargs['pk']
        query = Task.objects.all().filter(Project=project, user=user).order_by('Goal_Date').exclude(Status="CO")
        args = {'query': query}
        return render(request, self.template_name, args)

    def post(self, request, **kwargs):
        user = request.user
        project = self.kwargs['pk']
        query = Task.objects.all().filter(Project=project, user=user).order_by('Goal_Date').exclude(Status="CO")
        args = {'query': query}
        return render(request, self.template_name, args)


class CreateTaskView(TemplateView):
    template_name = 'edit_task.html'

    def get(self, request):
        user = request.user
        form = CreateTaskForm(user=user)
        return render(request, self.template_name, {'form': form, 'from': request.GET.get('from',None)})

    def post(self, request):
        user=request.user
        form = CreateTaskForm(user, request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            next = request.GET.get('next', None)
            if next:
                return redirect(next)
            else:
                return redirect('tracker:task')

        args = {'form':form, 'from' : request.GET.get('from', None)}
        return render(request, self.template_name, args)


class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('tracker:project')

class TaskEdit(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tracker:project')

def export_tasks_csv(request):
    user = request.user
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(['Task_Name','Project','Category','Short_list','Status','Start_Date','Modified_Date','Goal_Date','Notes'])

    tasks = Task.objects.all().filter(user=user).values_list('Task_Name','Project','Category','Short_list','Status','Start_Date','Modified_Date','Goal_Date','Notes')
    for task in tasks:
        writer.writerow(task)

    return response

# class date_filters(request):
#     if today:
#         today = datetime.now().date()
# tomorrow = today + timedelta(7)
# today_start = datetime.combine(today, time())
# today_end = datetime.combine(tomorrow, time())
