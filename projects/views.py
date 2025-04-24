from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProjectCreateForm, ProjectUpdateForm, TaskCreateForm, TaskUpdateForm


MY_TEST = "{self.request.user.id == self.get_object().user_id}"

def home(request):
    return render(request, 'home.html')

@login_required
def index(request):
    return render(request, 'index.html')


class ProjectListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "project/projects_list.html"
    ordering = ['order']
    paginate_by = 6
    
    def test_func(self):
        return (self.request.user.id == self.get_object().user_id)

class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ProjectCreateForm
    success_url = 'ProjectsList'
    template_name = 'create.html'

    def test_func(self):
        return (self.request.user.id == self.get_object().user_id)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ProjectUpdateForm
    template_name = 'project/update.html'
    success_url = 'ProjectUpdate'
    

    def test_func(self):
        return (self.request.user.id == self.get_object().user_id)
    

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'project/delete.html'

    def test_func(self):
        return (self.request.user.id == self.get_object().user_id)
    
    def get_success_url(self):
        return reverse('ProjectDelete', args=self.id) 


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = TaskCreateForm
    success_url = 'ProjectUpdate'
    template_name = 'task/task.html'

    def test_func(self):
        return (self.request.user.id == self.get_object().user_id)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = TaskUpdateForm
    success_url = 'ProjectUpdate'
    template_name = 'task/task.html'

    def test_func(self):
        return (self.request.user.id == self.get_object().user_id)
    
class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'task/task.html'

    def test_func(self):
        return (self.request.user.id == self.get_object().user_id)
    
    def get_success_url(self):
        return reverse('ProjectUpdate', args=self.id) 