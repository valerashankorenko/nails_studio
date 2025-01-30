from http import HTTPStatus

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name',
    (
            # Pages app
            'pages:index',
            'pages:price',
            'pages:foto',
            'pages:contact',
            'pages:info',

            # Users app
            'users:registration',
            'login',

            # Reviews app
            'reviews:review',

    ),
    ids=[
        'Главная страница',
        'Прайс лист',
        'Фото работ',
        'Контакты',
        'Советы',
        'Регистрация пользователя',
        'Страница входа',
        'Список отзывов',
    ]
)
def test_pages_availability_for_anonymous_user(client, name):
    """
    Тестирует доступность публичных страниц для анонимных пользователей.

    Проверяет, что указанные URL-адреса:
    - Возвращают статус 200 OK
    - Не требуют аутентификации
    - Доступны без дополнительных параметров

    Параметры теста:
    - name: Имя URL-шаблона в формате 'app:url_name'
    """
    url = reverse(name)

    try:
        response = client.get(url)
    except Exception as e:
        pytest.fail(f'Ошибка при обращении к странице {name}: {str(e)}')

    assert response.status_code == HTTPStatus.OK, (
        f'Страница {name} должна быть доступна анонимным пользователям. '
        f'Получен статус: {response.status_code}'
    )
