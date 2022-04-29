from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from manager.models import Task
from account.models import Profile
from django.utils import timezone
from django.conf import settings
from django.test import TestCase
from django.urls import reverse

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TaskManager.settings")


# models test
class ProfileTests(TestCase):

    def create_user(self, name, password, first_name, last_name, email):
        user = User(username=name, password=password, first_name=first_name, last_name=last_name, email=email)
        return user

    def create_profile(self, user, position, date_of_birth):
        profile = Profile(user=user, position=position, date_of_birth=date_of_birth)
        return profile

    def test_correct_User_and_Profile_creation(self):
        username = 'Mishaka'
        password = 'password'
        first_name = 'Mihail'
        last_name = 'Topuzov'
        email = 'mihata0000@yahoo.com'
        position = 'Manager'
        date_of_birth = '1994-02-14'

        user = self.create_user(username, password, first_name, last_name, email)
        profile = self.create_profile(user, position, date_of_birth)
        user.save()
        profile.save()
        self.assertTrue(isinstance(user, User))
        self.assertTrue(isinstance(profile, Profile))
        self.assertEqual(user.username, username)
        self.assertEqual(user.password, password)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.email, email)
        self.assertEqual(profile.position, position)
        self.assertEqual(profile.date_of_birth, date_of_birth)
        self.assertEqual(str(profile), f"Profile for user {username}")

    def test_incorrect_date_form_Profile(self):
        username = 'Mishaka'
        password = 'password'
        first_name = 'Mihail'
        last_name = 'Topuzov'
        email = 'mihata0000@yahoo.com'
        position = 'Manager'
        date_of_birth = 'Test1'
        user = self.create_user(username, password, first_name, last_name, email)
        profile = self.create_profile(user, position, date_of_birth)
        user.save()
        self.assertRaises(ValidationError, profile.save)


class TaskTests(TestCase):

    def setUp(self):
        User.objects.create(username='Mishaka', password='password', first_name='Mihail', last_name='Topuzov',
                            email='mihata0000@yahoo.com')

    def test_correct_Task_creation(self):
        user = User.objects.get(username='Mishaka')
        title = 'Task 1'
        description = 'Description for Task 1'
        priority = 'low'
        estimate = 15
        task = Task(title=title, description=description,slug='task-1', author=user, priority=priority, estimate=estimate)
        task.full_clean()
        task.save()
        self.assertTrue(isinstance(task, Task))
        self.assertEqual(task.title, title)
        self.assertEqual(task.description, description)
        self.assertEqual(task.slug, 'task-1')
        self.assertEqual(task.author, user)
        self.assertEqual(task.assignee, None)
        self.assertEqual(task.status, 'opened')
        self.assertEqual(task.priority, priority)
        self.assertEqual(task.estimate, estimate)
        self.assertEqual(task.tracked_time, 0)
        self.assertEqual(task.resolved, 'unresolved')

    def test_inexisting_user_Task_creation(self):
        user = ''
        title = 'Task 1'
        description = 'Description for Task 1'
        priority = 'Low'
        estimate = 15
        error = None
        try:
            Task(title=title, description=description, author=user, priority=priority, estimate=estimate)
        except ValueError as e:
            error = e
        self.assertIsNotNone(error)
        self.assertEqual('Cannot assign "\'\'": "Task.author" must be a "User" instance.', str(error))

    def test_wrong_priority_user_Task_creation(self):
        user = User.objects.get(username='Mishaka')
        title = 'Task 1'
        description = 'Description for Task 1'
        priority = 'No_Status'
        estimate = 15
        error = None
        try:
            task = Task(title=title,slug='task-1', description=description, author=user, priority=priority, estimate=estimate)
            task.full_clean()
            task.save()
        except ValidationError as e:
            error = e
        self.assertEqual("{'priority': [\"Value 'No_Status' is not a valid choice.\"]}", str(error))

    def test_wrong_status_user_Task_creation(self):
        user = User.objects.get(username='Mishaka')
        title = 'Task 1'
        description = 'Description for Task 1'
        priority = 'low'
        status = 'No_Status'
        estimate = 15
        error = None
        try:
            task = Task(title=title,slug='task-1',status=status, description=description, author=user, priority=priority, estimate=estimate)
            task.full_clean()
            task.save()
        except ValidationError as e:
            error = e
        self.assertEqual("{'status': [\"Value 'No_Status' is not a valid choice.\"]}", str(error))





