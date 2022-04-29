import json
from urllib.parse import urlencode

from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from account.models import Profile
from manager.models import Task


class ManagerViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='Mishaka', password='password', first_name='Mihail', last_name='Topuzov',
                                 email='mihata0000@yahoo.com')
        User.objects.create_user(username='Puk', password='password', first_name='Puk', last_name='Puk',
                                 email='kek@yahoo.com')
        # Create 13 tasks for pagination tests

        number_of_tasks = 13
        user = User.objects.get(username='Mishaka')
        priority = 'low'
        estimate = 15

        for task_id in range(number_of_tasks):
            title = f'Task {task_id}'
            description = f'Description for Task {task_id}'
            Task.objects.create(
                title=title,
                description=description,
                slug=f'task-{task_id}',
                author=user,
                priority=priority,
                estimate=estimate
            )

        employee_group = "Employee"
        manager_group = "Manager"
        admin_group = "Admin"
        Group.objects.create(name=employee_group)
        Group.objects.create(name=manager_group)
        Group.objects.create(name=admin_group)
        admin_group = Group.objects.get(name=admin_group)
        permissions_list = Permission.objects.all()
        admin_group.permissions.set(permissions_list)
        admin_group.save()

    def test_dashboard_url_not_available_to_guests(self):
        User.objects.get(username='Mishaka')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)

    def test_administration_url_not_available_to_guests(self):
        User.objects.get(username='Mishaka')
        response = self.client.get('administration')
        self.assertEqual(response.status_code, 404)

    def test_create_task_url_not_available_to_guests(self):
        User.objects.get(username='Mishaka')
        response = self.client.get('/create_task/')
        self.assertEqual(response.status_code, 404)

    def test_index_url_available_to_guests(self):
        User.objects.get(username='Mishaka')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_url_available_to_guests(self):
        User.objects.get(username='Mishaka')
        response = self.client.get('/account/register/')
        self.assertEqual(response.status_code, 200)

    def test_login_url_available_to_guests(self):
        User.objects.get(username='Mishaka')
        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_url_exists_at_desired_location_for_employees(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Employee')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_dashboard_url_exists_at_desired_location_for_managers(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Manager')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_dashboard_url_exists_at_desired_location_for_admins(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_profile_url_exists_at_desired_location_for_logged_users(self):
        user = User.objects.get(username='Mishaka')
        profile = Profile.objects.create(user=user)
        group = Group.objects.get(name='Employee')
        user.groups.add(group)
        user.save()
        profile.save()
        self.client.force_login(user=user)
        response = self.client.get('/account/profile/Mishaka')
        self.assertEqual(response.status_code, 200)

    def test_administration_url_not_accessed_by_non_admins(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Employee')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        response = self.client.get('/administration/')
        self.assertEqual(response.status_code, 404)

    def test_administration_url_accessed_by_non_admins(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        response = self.client.get('/administration/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administration.html')

    def test_tasks_appear_in_pagination(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        response = self.client.get('/tasks/tasks.json')
        self.assertContains(response,
                            '{"id": 9, "title": "Task 7", "assignee": "None", "priority": "low", "status": "opened"}')

    def test_tasks_listing_for_logged_user(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        response = self.client.get(reverse('tasks-api'))
        self.assertContains(response,
                            '{"id": 9, "title": "Task 7", "assignee": "None", "priority": "low", "status": "opened"}')

    def test_create_tasks_appear_for_logged_user(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        response = self.client.get('/create_task/')
        self.assertEqual(response.status_code, 200)

    def test_create_tasks_does_not_appear_for_guest(self):
        user = User.objects.get(username='Mishaka')
        self.client.force_login(user=user)
        response = self.client.get('/create_task/')
        self.assertEqual(response.status_code, 404)

    def test_task_details_existing_task(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        response = self.client.get('/tasks/14')
        self.assertEqual(response.status_code, 200)

    def test_task_details_inexisting_task(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        response = self.client.get('/tasks/2224')
        self.assertEqual(response.status_code, 404)

    def test_update_task_logged_in(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        data = json.dumps({'assignee': 'Mishaka',
                           'description': 'Heh',
                           'logged': '10',
                           'priority': 'low',
                           'resolution': 'resolved',
                           'status': 'in progress',
                           'title': 'Task 14'})

        response = self.client.post('/update_task/14', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('resolved', Task.objects.get(id=14).resolved)
        self.assertEqual(10, Task.objects.get(id=14).tracked_time)

    def test_update_not_existing_task(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        data = json.dumps({'assignee': 'Mishaka',
                           'description': 'Heh',
                           'logged': '10',
                           'priority': 'low',
                           'resolution': 'resolved',
                           'status': 'in progress',
                           'title': 'Task 14'})

        response = self.client.post('/update_task/144', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_admin_update_user_group(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user2 = User.objects.get(username='Puk')
        profile = Profile.objects.create(user=user2)
        profile.save()
        emp_group = Group.objects.get(name='Employee')
        user.groups.add(group)
        user.save()
        user2.groups.add(emp_group)
        user2.save()

        self.client.force_login(user=user)

        data = {'newGroup': "Manager",
                'userSlug': "Puk"}

        response = self.client.post('/account/update_user_groups/?userSlug=Puk', data=data,
                                    content_type='application/json')
        user2 = User.objects.get(username='Puk')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(True, user2.groups.filter(name='Manager').exists())

    def test_assign_to_me_proper_task(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        data = json.dumps({'task_id': '14',
                           'user_id': '7'})

        response = self.client.post(reverse('assign_to_me'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user, Task.objects.get(assignee=user).assignee)

    def test_assign_to_me_improper_task(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        data = json.dumps({'task_id': '14',
                           'user_id': '1'})

        response = self.client.post(reverse('assign_to_me'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete_existing_task(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        data = json.dumps({'task_id': '4'})

        response = self.client.post('/delete_task/4', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=4)

    def test_delete_inexisting_task(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        self.client.force_login(user=user)
        data = json.dumps({'task_id': '143'})

        response = self.client.post('/delete_task/143', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual('Task does not exist', response.content.decode("utf-8"))

    def test_delete_existing_user(self):
        user = User.objects.get(username='Mishaka')
        user2 = User.objects.get(username='Puk')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        user2.save()
        self.client.force_login(user=user)
        data = json.dumps({'userSlug': 'Puk'})

        response = self.client.post(reverse('delete_user'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_inexisting_user(self):
        user = User.objects.get(username='Mishaka')
        user2 = User.objects.get(username='Puk')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        user2.save()
        self.client.force_login(user=user)
        data = json.dumps({'userSlug': 'NoUser'})

        response = self.client.post(reverse('delete_user'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual('User does not exist', response.content.decode("utf-8"))

    def test_correct_login_user(self):
        data = urlencode({'username': 'Mishaka',
                          'password': 'password'})

        response = self.client.post(reverse('login'), data=data, content_type="application/x-www-form-urlencoded",
                                    follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_incorrect_login_user(self):
        data = urlencode({'username': 'Misha',
                          'password': 'password'})

        response = self.client.post(reverse('login'), data=data, content_type="application/x-www-form-urlencoded",
                                    follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_correct_register_user(self):
        data = urlencode({'username': 'Mishakaveli',
                          'password': 'password',
                          'password2': 'password',
                          'email': 'password@yahoo.com',
                          'first_name': 'Random'})

        response = self.client.post(reverse('register'), data=data, content_type="application/x-www-form-urlencoded",
                                    follow=True)
        self.assertContains(response, 'Welcome Random!')

    def test_incorrect_register_user(self):
        data = urlencode({'username': 'Mishakaveli',
                          'password': 'password',
                          'password2': 'password',
                          'email': 'password',
                          'first_name': 'Random'})

        response = self.client.post(reverse('register'), data=data, content_type="application/x-www-form-urlencoded",
                                    follow=True)
        self.assertContains(response, 'Enter a valid email address.')

    def test_correct_edit_user(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        self.client.force_login(user=user)
        data = urlencode({'first_name': 'Mihail',
                          'last_name': 'Topuzov',
                          'email': 'mihata2022@yahoo.com',
                          'date_of_birth': '1994-02-14',
                          'photo': ''})

        response = self.client.post('/account/edit/Mishaka', data=data, content_type="application/x-www-form-urlencoded",
                                    follow=True)
        self.assertContains(response, 'Profile updated successfully.')

    def test_incorrect_edit_user(self):
        user = User.objects.get(username='Mishaka')
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        user.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        self.client.force_login(user=user)
        data = urlencode({'first_name': 'Mihail',
                          'last_name': 'Topuzov',
                          'email': 'mihata2022@yahoo.com',
                          'date_of_birth': '6545646',
                          'photo': ''})

        response = self.client.post('/account/edit/Mishaka', data=data, content_type="application/x-www-form-urlencoded",
                                    follow=True)
        self.assertContains(response, 'Error while updating your profile.')