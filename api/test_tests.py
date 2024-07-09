import os
import django
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Item
from django.contrib.auth import get_user_model

os.environ['DJANGO_SETTINGS_MODULE'] = 'your_project_name.settings'
django.setup()

User = get_user_model()

class ItemViewsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.item = Item.objects.create(user=self.user, name='Test Item', quantity=10, phone='1234567890')

    def test_create_item(self):
        url = reverse('create_item')
        data = {
            'name': 'New Item',
            'quantity': 5,
            'phone': '0987654321', 
            'user': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Data is saved')
        self.assertEqual(Item.objects.count(), 2)

    def test_read_item(self):
        url = reverse('read_item', args=[self.item.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], self.item.name)
        self.assertEqual(data['quantity'], self.item.quantity)
        self.assertEqual(data['phone'], self.item.phone)

    def test_update_item(self):
        url = reverse('update_item', args=[self.item.pk])
        data = {
            'name': 'Updated Item',
            'quantity': 20,
            'phone': '1122334455'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        updated_item = Item.objects.get(pk=self.item.pk)
        self.assertEqual(updated_item.name, data['name'])
        self.assertEqual(updated_item.quantity, data['quantity'])
        self.assertEqual(updated_item.phone, data['phone'])

    def test_delete_item(self):
        url = reverse('delete_item', args=[self.item.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Item.objects.filter(pk=self.item.pk).count(), 0)
