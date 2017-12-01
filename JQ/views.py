from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView, DeleteView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy

from JQ.models import Application, Company, Resources, Notes, Contact, Questions, Ask
from JQ.forms import (CreateCompany, CreateApplication, CreateResource,
CreateNote, CreateContact, CreateQuestion)


class AppView(TemplateView):
    template_name = 'app.html'

    def get(self, request):
        user = request.user
        query = Application.objects.all().exclude(app_status ="CO").filter(user=user).order_by('applied_date')
        args = {'query': query}
        return render(request, self.template_name, args)

class AppDetail(TemplateView):
    template_name = 'appdetail'

class CreateApp(TemplateView):
    template_name = 'create_application.html'

    def get(self, request):
        user=request.user
        form = CreateApplication(user=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user=request.user
        form = CreateApplication(user,request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('JQ:apps')

        args = {'form':form}
        return render(request, self.template_name, args)

class DeleteApp(DeleteView):
    model = Application
    success_url = reverse_lazy('JQ:apps')

class EditApp(UpdateView):
    model = Application
    fields = {'position','app_status','applied_date'}
    success_url = reverse_lazy('JQ:apps')

class CompanyView(TemplateView):
    template_name = 'company.html'

    def get(self, request):
        user = request.user
        query = Company.objects.all().filter(user=user)
        args = {'query': query}
        return render(request, self.template_name, args)

class AddCompany(TemplateView):
    template_name = 'create_company.html'

    def get(self, request):
        form = CreateCompany
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreateCompany(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('JQ:create_app')

        args = {'form':form}
        return render(request, self.template_name, args)

class DeleteCompany(DeleteView):
    model = Company
    success_url = reverse_lazy('JQ:company')

class EditCompany(UpdateView):
    model = Company
    form_class = CreateCompany
    success_url = reverse_lazy('JQ:company')

class DashboardView(TemplateView):
    template_name = 'dashboard_detail.html'

    def get_context_data(self, **kwargs):
        app_id = self.kwargs['pk']
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['Application'] = Application.objects.all().filter(id=app_id)
        context['Contact'] = Contact.objects.all().filter(App=app_id)
        context['Notes'] = Notes.objects.all().filter(App=app_id)
        context['Resources'] = Resources.objects.all().filter(App=app_id)
        context['Ask'] = Ask.objects.all().filter(app=app_id)
        return context

    def post(self, request, **kwargs):
        app_id = self.kwargs['pk']
        return_url = request.POST.get('url')
        new_answer = request.POST.get('response')
        answer_id = request.POST.get('q_id')
        if new_answer != None:
            myAsk = Ask.objects.get(pk=int(answer_id))
            myAsk.answer = new_answer
            myAsk.save()
        return HttpResponseRedirect(return_url)


class AddContact(TemplateView):
    template_name = 'create_contact.html'

    def get(self, request):
        form = CreateContact
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreateContact(request.POST)
        return_url = request.POST.get('app')
        app = int(return_url.rsplit('/')[-1])
        myApp = Application.objects.get(pk=app)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.App = myApp
            post.save()
            return HttpResponseRedirect(return_url)

        args = {'form':form}
        return render(request, self.template_name, args)

class DeleteContact(DeleteView):
    model = Contact
    success_url = reverse_lazy('JQ:apps')

class EditContact(UpdateView):
    model = Contact
    form_class = CreateContact
    success_url = reverse_lazy('JQ:apps')

class AddNote(TemplateView):
    template_name = 'create_note.html'

    def get(self, request):
        form = CreateNote
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreateNote(request.POST)
        return_url = request.POST.get('app')
        app = int(return_url.rsplit('/')[-1])
        myApp = Application.objects.get(pk=app)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.App = myApp
            post.save()
            return HttpResponseRedirect(return_url)

        args = {'form':form}
        return render(request, self.template_name, args)

class DeleteNote(DeleteView):
    model = Notes
    success_url = reverse_lazy('JQ:apps')

class EditNote(UpdateView):
    model = Notes
    form_class = CreateNote
    success_url = reverse_lazy('JQ:apps')

class AddResource(TemplateView):
    template_name = 'create_resource.html'

    def get(self, request):
        form = CreateResource
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreateResource(request.POST)
        return_url = request.POST.get('app')
        app = int(return_url.rsplit('/')[-1])
        myApp = Application.objects.get(pk=app)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.App = myApp
            post.save()
            return HttpResponseRedirect(return_url)

        args = {'form':form}
        return render(request, self.template_name, args)

class DeleteResource(DeleteView):
    model = Resources
    success_url = reverse_lazy('JQ:apps')

class EditResource(UpdateView):
    model = Resources
    form_class = CreateResource
    success_url = reverse_lazy('JQ:apps')

class AddQuestion(TemplateView):
    template_name = 'create_question.html'

    def get(self, request):
        form = CreateQuestion
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreateQuestion(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('JQ:apps')

        args = {'form':form}
        return render(request, self.template_name, args)

class DeleteQuestion(DeleteView):
    model = Questions
    success_url = reverse_lazy('JQ:questions')

class EditQuestion(UpdateView):
    model = Questions
    form_class = CreateQuestion
    success_url = reverse_lazy('JQ:apps')

class QuestionView(TemplateView):
    template_name = 'question.html'

    def get(self, request):
        user = request.user
        query = Questions.objects.filter(user=user).order_by('category')
        args = {'query': query}
        return render(request, self.template_name, args)

    def post(self, request):
        id_list = request.POST.getlist('selected_q')
        return_url = request.POST.get('app')
        app = int(return_url.rsplit('/')[-1])
        myApp = Application.objects.get(pk=app)
        if id_list != None:
            for item in id_list:
                myQuestion = Questions.objects.get(pk=int(item))
                Ask.objects.create(app=myApp,question=myQuestion)
            return HttpResponseRedirect(return_url)
        else:
            query = Questions.objects.all().order_by('category')
            args = {'query': query}
            return render(request, self.template_name, args)

class DeleteAsk(DeleteView):
    model = Ask
    success_url = reverse_lazy('JQ:apps')
