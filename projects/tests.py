from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Project, Task, Category, ProjectStatus


User = get_user_model()

# class TaskDeleteViewTest(TestCase):
#     def setUp(self):
#         # إنشاء مستخدمين
#         self.user1 = User.objects.create_user(username='user1', password='pass123')
#         self.user2 = User.objects.create_user(username='user2', password='pass123')

#         # إنشاء تصنيف
#         self.category = Category.objects.create(title='Web')

#         # مشروع يملكه user1
#         self.project = Project.objects.create(
#             title='Test Project',
#             description='Description',
#             category=self.category,
#             user=self.user1
#         )

#         # مهمة مرتبطة بالمشروع
#         self.task = Task.objects.create(
#             description='Test Task',
#             project=self.project
#         )

#         self.client = Client()

#     def test_owner_can_delete_task(self):
#         # تسجيل دخول user1
#         self.client.login(username='user1', password='pass123')

#         response = self.client.post(reverse('TaskDelete', kwargs={'pk': self.task.pk}), {
#             'project': self.project.pk
#         })

#         self.assertEqual(response.status_code, 302)  # إعادة توجيه بعد الحذف
#         self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

#     def test_other_user_cannot_delete_task(self):
#         # تسجيل دخول user2
#         self.client.login(username='user2', password='pass123')

#         response = self.client.post(reverse('TaskDelete', kwargs={'pk': self.task.pk}), {
#             'project': self.project.pk
#         })

#         self.assertEqual(response.status_code, 403)  # لا يملك الصلاحية
#         self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())


class ProjectDeleteViewTest(TestCase):
    def setUp(self):
        # إنشاء مستخدمين
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

        # إنشاء تصنيف
        self.category = Category.objects.create(title='Web')

        # مشروع يملكه user1
        self.project = Project.objects.create(
            title='Test Project',
            description='Description',
            category=self.category,
            user=self.user1
        )

        # مهمة مرتبطة بالمشروع
        self.task = Task.objects.create(
            description='Test Task',
            project=self.project
        )

        self.client = Client()

    def test_owner_can_delete_project(self):
        # تسجيل دخول user1
        self.client.login(username='user1', password='pass123')

        response = self.client.post(reverse('ProjectDelete', kwargs={'pk': self.project.pk}), {
            'project': self.project.pk
        })

        self.assertEqual(response.status_code, 302)  # إعادة توجيه بعد الحذف
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_other_user_cannot_delete_project(self):
        # تسجيل دخول user2
        self.client.login(username='user2', password='pass123')

        response = self.client.post(reverse('ProjectDelete', kwargs={'pk': self.project.pk}), {
            'project': self.project.pk
        })

        self.assertEqual(response.status_code, 403)  # لا يملك الصلاحية
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())