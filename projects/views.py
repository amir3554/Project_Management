from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProjectCreateForm, ProjectUpdateForm, TaskCreateForm, TaskUpdateForm
from .models import Project, Task

MY_TEST = "{self.request.user.id == self.get_object().user_id}"

def home(request):
    return render(request, 'home.html')

@login_required
def index(request):
    return render(request, 'index.html')

class UserOwnsProjectMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to ensure the logged-in user owns the project associated with the Task.
    """
    def test_func(self):
        try:
            project_id = self.request.POST.get('project') or self.kwargs.get('project_id')
            if project_id:
                task = get_object_or_404(Task, pk=self.kwargs['pk'])
                return task.project.user == self.request.user
            return False
        except Task.DoesNotExist:
            return False

    def handle_no_permission(self):
        # Optionally, you can redirect the user or raise a different exception
        # For now, the default behavior of UserPassesTestMixin will apply (403 Forbidden)
        return super().handle_no_permission()



class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "project/projects_list.html"
    ordering = ['updated_at']
    paginate_by = 6
    
    def get_queryset(self):
        query_set = super().get_queryset()
        where = {'user_id': self.request.user}
        q = self.request.GET.get('q', None)
        if q:
            where['title__icontains'] = q
        return query_set.filter(**where)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = 'project/create.html'
    success_url = reverse_lazy('ProjectsList')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectUpdateForm
    template_name = 'project/update.html'
    
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('ProjectUpdate', args=[self.object.id]) 
    

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'project/delete.html'
    success_url = reverse_lazy('ProjectsList')




class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['project', 'description']
    http_method_names = ['post']


    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ProjectUpdate', args=[self.object.project.id])
    


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['is_completed']
    template_name = 'project/update.html'
    http_method_names = ['post', 'get']
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['project_id'] = self.request.POST.get('project', self.object.project.id if self.object else None)        
        return context

    
    def get_success_url(self):
        return reverse('ProjectUpdate', kwargs={ 'pk' : self.object.project.id}) 
    
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    fields = ['project']
    pk_url_kwarg = 'pk'


    def get_success_url(self):
        return reverse('ProjectUpdate', args=[self.get_object().project.id]) 