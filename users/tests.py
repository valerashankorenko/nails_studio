from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTestCase(TestCase):
    def test_create_user(self):
        """Тест создания пользователя."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Петя',
            last_name='Иванов',
            phone_number='+37529111111',
            password='testpassword'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Петя')
        self.assertEqual(user.last_name, 'Иванов')
        self.assertEqual(user.phone_number, '+37529111111')
        self.assertTrue(user.check_password('testpassword'))
