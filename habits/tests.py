from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from habits.models import Habit
from actions.models import Action
from places.models import Place
from users.models import User


class HabitAPITests(APITestCase):

    def setUp(self):
        """Начальные установки для тестирования"""
        self.user = User.objects.create(id=1, email="user@mail.ru", is_staff=True)

        self.access_token = str(AccessToken.for_user(self.user))
        self.client = APIClient()

        # Создаем необходимые объекты Action и Place для тестирования
        self.place = Place.objects.create(title='Test Place')
        self.action = Action.objects.create(title='Test Action')

        # Создаем привычки для тестирования
        self.habit_pleasant = Habit.objects.create(
            owner=self.user,
            place=self.place,
            action=self.action,
            time='12:00:00',
            periodicity=5,
            is_pleasant=True,
            duration=60,
            is_public=False
        )

        self.habit_non_pleasant = Habit.objects.create(
            owner=self.user,
            place=self.place,
            action=self.action,
            time='12:00:00',
            periodicity=5,
            is_pleasant=False,
            duration=30,
            is_public=False
        )

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_correct_habit(self):
        """Тестирование создания правильной привычки"""
        self.authenticate()
        data = {
            'owner': self.user.id,
            'place': self.place.id,
            'action': self.action.id,
            'time': '12:45:00',
            'periodicity': 5,
            'is_pleasant': False,
            'duration': 30,
            'is_public': False,
        }
        response = self.client.post('/habits/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['time'], '12:45:00')

    def test_create_habit_with_reward_and_related_habit(self):
        """Тестирование создания привычки с одновременно заданными reward и related_habit"""
        self.authenticate()
        data = {
            'owner': self.user.id,
            'place': self.place.id,
            'action': self.action.id,
            'time': '12:00:00',
            'periodicity': 5,
            'is_pleasant': False,
            'duration': 30,
            'reward': 'Some reward',
            'is_public': False,
            'related_habit': self.habit_non_pleasant.id,
        }
        response = self.client.post('/habits/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Нельзя одновременно задать поля 'Вознаграждение' и 'Связанная привычка'. Заполните только одно из них.",
            response.data['non_field_errors'])

    def test_create_habit_with_non_pleasant_related_habit(self):
        """Тестирование создания привычки с неприятной связанной привычкой"""
        self.authenticate()
        data = {
            'owner': self.user.id,
            'place': self.place.id,
            'action': self.action.id,
            'time': '12:00:00',
            'periodicity': 5,
            'is_pleasant': False,
            'duration': 30,
            'is_public': False,
            'related_habit': self.habit_non_pleasant.id,
        }
        response = self.client.post('/habits/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Привычка может быть связана только с теми, у которых установлена отметка 'Приятная привычка'",
                      response.data['non_field_errors'])

    def test_create_habit_with_exceeding_duration(self):
        """Тестирование создания привычки с превышающей продолжительностью"""
        self.authenticate()
        data = {
            'owner': self.user.id,
            'place': self.place.id,
            'action': self.action.id,
            'time': '12:00:00',
            'periodicity': 5,
            'is_pleasant': False,
            'is_public': False,
            'duration': 130,
        }
        response = self.client.post('/habits/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Максимальное время выполнения привычки — 120 секунд.", response.data['non_field_errors'])

    def test_create_habit_with_invalid_periodicity(self):
        """Тестирование создания привычки с недопустимой периодичностью"""
        self.authenticate()
        data = {
            'owner': self.user.id,
            'place': self.place.id,
            'action': self.action.id,
            'time': '12:00:00',
            'is_pleasant': False,
            'is_public': False,
            'duration': 30,
            'periodicity': 8,
        }
        response = self.client.post('/habits/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Минимальная частота выполнения привычки — раз в 1 день, максимальная — раз в 7 дней.",
                      response.data['non_field_errors'])

    def test_no_reward_for_pleasant_habit(self):
        """Тестирование создания приятной привычки с вознаграждением"""
        self.authenticate()
        data = {
            'owner': self.user.id,
            'place': self.place.id,
            'action': self.action.id,
            'time': '12:00:00',
            'is_pleasant': True,
            'is_public': False,
            'duration': 30,
            'periodicity': 5,
            'reward': 'Some reward',
        }
        response = self.client.post('/habits/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Приятной привычке нельзя присваивать вознаграждение или связанную привычку.",
                      response.data['non_field_errors'])

    def test_no_both_reward_and_related_habit_on_update(self):
        """Тестирование обновления привычки с одновременными reward и related_habit"""
        self.authenticate()
        data = {
            'owner': self.user.id,
            'place': self.place.id,
            'action': self.action.id,
            'time': '12:00:00',
            'is_pleasant': True,
            'is_public': False,
            'duration': 30,
            'periodicity': 5,
            'reward': 'Some reward',
            'related_habit': self.habit_non_pleasant.id,
        }
        response = self.client.put(f'/habits/{self.habit_pleasant.id}/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Нельзя одновременно задать поля 'Вознаграждение' и 'Связанная привычка'. Заполните только одно из них.",
            response.data['non_field_errors'])

    def test_unauthenticated_user_access(self):
        """Тестирование доступа неаутентифицированного пользователя"""
        response = self.client.get('/habits/list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        data = {
            'owner': self.user.id,
            'place': self.place.id,
            'action': self.action.id,
            'time': '12:00:00',
            'is_pleasant': True,
            'is_public': False,
            'duration': 30,
            'periodicity': 5,
        }
        response = self.client.post('/habits/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_public_habits(self):
        """Тестирование получения публичных привычек"""
        self.authenticate()
        self.habit_pleasant.is_public = True
        self.habit_pleasant.save()

        response = self.client.get('/habits/public/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_update_habit(self):
        """Тестирование обновления привычки"""
        self.authenticate()
        data = {
            'owner': self.user.id,
            'place': self.place.id,
            'action': self.action.id,
            'time': '12:30:00',
            'is_pleasant': True,
            'is_public': False,
            'duration': 30,
            'periodicity': 5,
        }
        response = self.client.put(f'/habits/{self.habit_pleasant.id}/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit_pleasant.refresh_from_db()
        self.assertEqual(response.data['time'], '12:30:00')

    def test_get_habits_list_pagination(self):
        """Тестирование получения списка привычек и пагинации"""
        self.authenticate()
        for i in range(4):
            data = {
                'owner': self.user.id,
                'place': self.place.id,
                'action': self.action.id,
                'time': '12:45:00',
                'periodicity': 5,
                'is_pleasant': False,
                'duration': 30,
                'is_public': False,
            }
            self.client.post('/habits/create/', data, format='json')
        response = self.client.get('/habits/list/')
        print(response.data['next'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 6)
        self.assertNotEqual(response.data['next'], 'None')

    def test_ditail_habits(self):
        """Тестирование вывода информации по конредной привычке"""
        self.authenticate()
        response = self.client.get(f'/habits/{self.habit_non_pleasant.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['time'], '12:00:00')
        self.assertEqual(str(self.habit_non_pleasant), 'Test Action Test Place 12:00:00 30')
