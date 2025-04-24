from django.forms.models import ModelForm
from .models import Project, Task
from django import forms


attrs = {'class': 'form-control'}


class ProjectCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta():

        model = Project

        fields = ['title', 'description', 'status', 'category']

        labels = {
            'title' : 'The Title',
            'description' : 'The Description',
            'status' : 'The Project Status:',
            'category' : 'category'
        }

        widgets = {
            'title': forms.TextInput(attrs=attrs),
            'description': forms.Textarea(attrs=attrs),
            'status' : forms.Select(attrs=attrs),
            'category' : forms.Select(attrs=attrs)
        }


class ProjectUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta():

        model = Project

        fields = ['description', 'status']

        labels = {
            'description' : 'The Description',
            'status' : 'The Project Status:',
        }

        widgets = {
            'description': forms.Textarea(attrs=attrs),
            'status' : forms.Select(attrs=attrs),
        }


class TaskCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta():

        model = Task

        fields = ['description']

        labels = {
            'description' : 'The Description',
        }

        widgets = {
            'description': forms.TextInput(attrs=attrs),
        }

class TaskUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta():

        model = Task

        fields = ['is_completed']

        labels = {
            'is_compelete' : 'Is Compelete',
        }

        widgets = {
            'is_completed': forms.Select(attrs=attrs),
        }
