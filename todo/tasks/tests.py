from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

class TaskTests(APITestCase):
    def test_create_task(self):
        url = reverse('task-list')
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')

    def test_get_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_update_task(self):
        task = Task.objects.create(title='Test Task', description='Test Description', priority=1)
        url = reverse('task-detail', args=[task.id])
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'priority': 2
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get().title, 'Updated Task')

    def test_delete_task(self):
        task = Task.objects.create(title='Test Task', description='Test Description', priority=1)
        url = reverse('task-detail', args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)


