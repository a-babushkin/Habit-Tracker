from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from actions.models import Action
from users.models import User

class ActionViewSetTests(APITestCase):
    def setUp(self):
        """Начальные установки для тестирования"""
        self.user = User.objects.create(email="user@mail.ru", is_staff=True)

        self.access_token = str(AccessToken.for_user(self.user))
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.action1 = Action.objects.create(title='Action 1')
        self.action2 = Action.objects.create(title='Action 2')

    def test_list_actions(self):
        """Тестирование получения списка действий"""
        response = self.client.get('/actions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Action.objects.count(), 2)

    def test_create_action(self):
        """Тестирование создания действия"""
        data = {
            'title': 'New Action',
        }
        response = self.client.post('/actions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Action.objects.count(), 3)
        self.assertEqual(Action.objects.get(id=response.data['id']).title, 'New Action')

    def test_update_action(self):
        """Тестирование обновления действия"""
        data = {
            'title': 'Updated Action'
        }
        response = self.client.put(f'/actions/{self.action1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.action1.refresh_from_db()
        self.assertEqual(self.action1.title, 'Updated Action')

    def test_delete_action(self):
        """Тестирование удаления действия"""
        response = self.client.delete(f'/actions/{self.action1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Action.objects.count(), 1)  # Должно остаться 1 действие

    def test_unauthenticated_user_access(self):
        """Тестирование доступа неаутентифицированного пользователя"""
        self.client.logout()
        response = self.client.get('/actions/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)