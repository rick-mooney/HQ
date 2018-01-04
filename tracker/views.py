from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy

import csv
from datetime import datetime, timedelta, time

from tracker.models import Task, Project, ProjectMember
from tracker.forms import (CreateTaskForm, CreateProjectForm, EditTaskForm)

class canvas(TemplateView):
    template_name = 'canvas.html'
    def get(self, request):
        return render(request, self.template_name)

class TaskView(TemplateView):
    template_name = 'task.html'

    def get(self, request):
        user=request.user
        search_query = request.GET.get('search', None)

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
            query = Task.objects.all().filter(Goal_Date__lt=datetime.now().date(), user=user).exclude(Status="CO").order_by('Goal_Date')
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
            | (Task.objects.all().filter(Notes__icontains=search_query, user=user).exclude(Status="CO").order_by('Goal_Date')) \
            | (Task.objects.all().filter(Category__icontains=search_query, user=user).exclude(Status="CO").order_by('Goal_Date'))
            args = {'query': query,'SearchWord':search_query}
            return render(request, self.template_name, args)

        else:
            query = Task.objects.all().filter(user=user).exclude(Status="CO").order_by('Goal_Date')
            args = {'query': query}
            return render(request, self.template_name, args)

    def post(self, request):
        user=request.user
        search_query = request.GET.get('search', None)
        massUpdateList = request.POST.getlist('selectedTask')
        if massUpdateList != None:
            cat = request.POST.get('category')
            stat = request.POST.get('status')
            goalDate = request.POST.get('goalDate')
            shortList = request.POST.get('shortList')
            for task in massUpdateList:
                update = Task.objects.get(pk=int(task))
                if cat != '':
                    update.Category = cat
                if stat != '':
                    update.Status = stat
                if goalDate != '':
                    update.Goal_Date = goalDate
                if shortList:
                    update.Short_list = True
                update.save()
        if search_query != None:
            query = (Task.objects.all().filter(Task_Name__icontains=search_query, user=user).exclude(Status="CO").order_by('Goal_Date')) \
            | (Task.objects.all().filter(Notes__icontains=search_query, user=user).exclude(Status="CO").order_by('Goal_Date'))\
            | (Task.objects.all().filter(Category__icontains=search_query, user=user).exclude(Status="CO").order_by('Goal_Date'))
        else:
            query = Task.objects.all().filter(user=user).exclude(Status="CO").order_by('Goal_Date')
            search_query = ''
        args = {'query': query,'SearchWord':search_query}
        return render(request, self.template_name, args)

class ProjectView(TemplateView):
    template_name = 'project.html'

    def get(self, request):
        user = request.user
        query = Project.objects.all().filter(user=user)
        shared_projects = ProjectMember.objects.all().filter(Member=user)
        args = {'query': query, 'shared_projects':shared_projects}
        return render(request, self.template_name, args)

    def post(self, request):
        user = request.user
        new_project = request.POST.get('project_name')
        if new_project:
            Project.objects.create(Project_name=new_project, user=user)
        query = Project.objects.all().filter(user=user)
        shared_projects = ProjectMember.objects.all().filter(Member=user)
        args = {'query': query, 'shared_projects':shared_projects}
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
    fields = ['Project_name','Description']
    success_url = reverse_lazy('tracker:project')


class ProjectListView(TemplateView):
    template_name = 'task.html'

    def get(self, request, **kwargs):
        user = request.user
        project_id = self.kwargs['pk']
        project = Project.objects.all().filter(id=project_id)
        team_members = ProjectMember.objects.all().filter(ProjectId=project).values('Member')
        project_owners = ProjectMember.objects.all().filter(ProjectId=project).values('Owner')
        owner_id = []
        member_id = []
        project_creator = project.values_list('user')[0][0]
        if team_members != None:
            for name in team_members:
                name_id = name.get('Member')
                member_id.append(name_id)
        if project_owners != None:
            for name in project_owners:
                name_id = name.get('Owner')
                owner_id.append(name_id)
        if (user.id in owner_id) | (user.id in member_id) | (user.id == project_creator):
            query = Task.objects.all().filter(Project=project, user=user).order_by('Goal_Date').exclude(Status="CO")
            if (user.id in member_id) | (user.id in owner_id):
                query = Task.objects.all().filter(Project=project).order_by('Goal_Date').exclude(Status="CO")
            all_users = User.objects.all()
            team = ProjectMember.objects.all().filter(ProjectId=project)
            args = {'query': query, 'project':project, 'users':all_users, 'team':team}
            return render(request, self.template_name, args)
        else:
            return redirect('tracker:project')

    def post(self, request, **kwargs):
        user = request.user
        project_id = self.kwargs['pk']
        project_inst = Project.objects.get(pk=project_id)
        project = Project.objects.all().filter(id=project_id)
        new_task = request.POST.get('task_name')
        member_name = request.POST.get('member_name')
        project_creator = project.values_list('user')[0][0]
        owner_id = []
        member_id = []
        team_members = ProjectMember.objects.all().filter(ProjectId=project).values('Member')
        project_owners = ProjectMember.objects.all().filter(ProjectId=project).values('Owner')
        if new_task != None:
            post = Task()
            post.user=user
            post.Project=project_inst
            post.Task_Name = new_task
            post.Goal_Date = datetime.now().date()
            post.Status='NS'
            post.Category='Quick Task'
            post.save()
        if member_name != None:
            new_member = User.objects.get(username=member_name)
            create_member = ProjectMember()
            create_member.ProjectId = project_inst
            create_member.Owner = user
            create_member.Member = new_member
            create_member.save()
        if team_members != None:
            for name in team_members:
                name_id = name.get('Member')
                member_id.append(name_id)
        if project_owners != None:
            for name in project_owners:
                name_id = name.get('Owner')
                owner_id.append(name_id)
        if (user.id in owner_id) | (user.id in member_id) | (user.id == project_creator):
            query = Task.objects.all().filter(Project=project, user=user).order_by('Goal_Date').exclude(Status="CO")
            if (user.id in member_id) | (user.id in owner_id):
                query = Task.objects.all().filter(Project=project).order_by('Goal_Date').exclude(Status="CO")
            all_users = User.objects.all()
            team = ProjectMember.objects.all().filter(ProjectId=project)
            args = {'query': query, 'project':project, 'users':all_users, 'team':team}
            return render(request, self.template_name, args)
        else:
            return redirect('tracker:project')

class DeleteProjectMember(DeleteView):
    model = ProjectMember
    success_url = reverse_lazy('tracker:task')

class CreateTaskView(TemplateView):
    template_name = 'create_task.html'

    def get(self, request):
        user = request.user
        form = CreateTaskForm(user=user)
        return render(request, self.template_name, {'form': form, 'from': request.GET.get('from',None)})

    def post(self, request):
        user = request.user
        form = CreateTaskForm(user, request.POST)
        form.user = user.id
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            next = request.POST.get('next','/')
            if next:
                return redirect(next)
            else:
                return redirect('tracker:task')
        else:
            args = {'form':form, 'from' : request.GET.get('from', None)}
            return render(request, self.template_name, args)


class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('tracker:task')

class TaskEdit(TemplateView):
    template_name = 'edit_task.html'

    def get(self, request, **kwargs):
        user = request.user
        task_id = self.kwargs['pk']
        task_data = Task.objects.all().filter(id=task_id)
        project_id = task_data.values_list('Project')[0][0]
        task_owner = task_data.values_list('user')[0][0]
        team_members = ProjectMember.objects.all().filter(ProjectId=project_id).values('Member')
        owner_id = []
        team_list = []
        project_owners = ProjectMember.objects.all().filter(ProjectId=project_id).values('Owner')
        if project_owners != None:
            for name in project_owners:
                name_id = name.get('Owner')
                owner_id.append(name_id)
        if team_members != None:
            for name in team_members:
                name_id = name.get('Member')
                team_list.append(name_id)
        if (user.id in team_list) | (user.id in owner_id):
            team = ProjectMember.objects.all().filter(ProjectId=project_id)
            query = Task.objects.get(id=task_id)
            form = EditTaskForm(instance=query)
            return render(request, self.template_name, {'form': form, 'team': team})
        elif user.id == task_owner:
            query = Task.objects.get(id=task_id, user=user)
            form = EditTaskForm(instance=query)
            return render(request, self.template_name, {'form': form})

        else:
            return redirect('tracker:project')

    def post(self, request, **kwargs):
        user = request.user
        task_id = self.kwargs['pk']
        query = Task.objects.get(id=task_id)
        task_data = Task.objects.all().filter(id=task_id)
        project_id = task_data.values_list('Project')[0][0]
        project = Project.objects.get(id=project_id)
        assigned_user = request.POST.get('user')
        if assigned_user != None:
            taskOwner = User.objects.get(id=assigned_user)
            query.user = taskOwner
        else:
            query.user = user
        query.Project = project
        query.Task_Name = request.POST.get('task')
        query.Category = request.POST.get('category')
        query.Status = request.POST.get('status')
        query.Notes = request.POST.get('notes')
        query.Goal_Date = request.POST.get('Goal_Date')
        if request.POST.get('shortList') == None:
            query.Short_list = False
        else:
            query.Short_list = True
        if query.Status == 'CO':
            query.Complete_Date = datetime.now().date()
        query.save()
        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)


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
