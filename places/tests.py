from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from places.models import Place
from users.models import User

class PlaceViewSetTests(APITestCase):
    def setUp(self):
        """Начальные установки для тестирования"""
        self.user = User.objects.create(email="user@mail.ru", is_staff=True)

        self.access_token = str(AccessToken.for_user(self.user))
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.place1 = Place.objects.create(title='Place 1')
        self.place2 = Place.objects.create(title='Place 2')

    def test_list_places(self):
        """Тестирование получения списка мест"""
        response = self.client.get('/places/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Place.objects.count(), 2)

    def test_create_place(self):
        """Тестирование создания места"""
        data = {
            'title': 'New Place',
        }
        response = self.client.post('/places/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 3)
        self.assertEqual(Place.objects.get(id=response.data['id']).title, 'New Place')

    def test_update_place(self):
        """Тестирование обновления места"""
        data = {
            'title': 'Updated Place'
        }
        response = self.client.put(f'/places/{self.place1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.place1.refresh_from_db()
        self.assertEqual(self.place1.title, 'Updated Place')

    def test_delete_place(self):
        """Тестирование удаления места"""
        response = self.client.delete(f'/places/{self.place1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Place.objects.count(), 1)  # Должно остаться 1 действие

    def test_unauthenticated_user_access(self):
        """Тестирование доступа неаутентифицированного пользователя"""
        self.client.logout()
        response = self.client.get('/places/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ditail_place(self):
        """Тестирование вывода информации по конредному месту"""
        response = self.client.get(f'/places/{self.place1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Place 1')
        self.assertEqual(str(self.place1), 'Place 1')
