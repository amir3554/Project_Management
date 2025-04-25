from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProjectCreateForm, ProjectUpdateForm, TaskCreateForm, TaskUpdateForm
from .models import Project, Task

# class UserOwnsProjectMixin(LoginRequiredMixin, UserPassesTestMixin):
#     """
#     Mixin to ensure the logged-in user owns the project associated with the Task.
#     """
#     def test_func(self):
#         try:
#             project_id = self.request.POST.get('project') or self.kwargs.get('project_id')
#             if not project_id:
#                 project_id = self.request.GET.get('project') or self.kwargs.get('project_id')
#             if project_id:
#                 project = get_object_or_404(Project, pk=self.kwargs['pk'])
#                 return project.user == self.request.user.id
#             return False
#         except Project.DoesNotExist:
#             return False

#     def handle_no_permission(self):
#         # Optionally, you can redirect the user or raise a different exception
#         # For now, the default behavior of UserPassesTestMixin will apply (403 Forbidden)
#         return super().handle_no_permission()


def my_test(self):
    return (self.request.user.id == self.get_object().user_id)

def home(request):
    return render(request, 'home.html')

@login_required
def index(request):
    return render(request, 'index.html')




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


class ProjectCreateView( LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = 'project/create.html'
    success_url = reverse_lazy('ProjectsList')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Project
    form_class = ProjectUpdateForm
    template_name = 'project/update.html'
    
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def test_func(self):
        return my_test(self)


    def get_success_url(self):
        return reverse('ProjectUpdate', args=[self.object.id]) 
    

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'project/delete.html'
    success_url = reverse_lazy('ProjectsList')

    def test_func(self):
        return my_test(self)


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    fields = ['project', 'description']
    http_method_names = ['post']

    def test_func(self):
        project_id = self.request.POST.get('project', '')
        return (Project.objects.get(pk=project_id).user_id == self.request.user.id)

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ProjectUpdate', args=[self.object.project.id])
    


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['is_completed']
    template_name = 'project/update.html'
    http_method_names = ['post', 'get']
    pk_url_kwarg = 'pk'

    def test_func(self):
        project_id = self.request.POST.get('project', '')
        return (Project.objects.get(pk=project_id).user_id == self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['project_id'] = self.request.POST.get('project', self.object.project.id if self.object else None)        
        return context

    
    def get_success_url(self):
        return reverse('ProjectUpdate', kwargs={ 'pk' : self.object.project.id}) 
    
class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    fields = ['project']
    http_method_names = ['post']

    def test_func(self):
        project_id = self.request.POST.get('project', '')
        return (Project.objects.get(pk=project_id).user_id == self.request.user.id)
    
    def get_success_url(self):
        return reverse('ProjectUpdate', args=[self.get_object().project.id]) 