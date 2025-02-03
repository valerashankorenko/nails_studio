from http import HTTPStatus

import pytest
from django.urls import reverse


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
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK, (
        f'Страница {name} должна быть доступна анонимным пользователям. '
        f'Получен статус: {response.status_code}'
    )


@pytest.mark.parametrize(
    'name',
    (
            # Users app
            'logout',
            'password_reset',

            # Reviews app
            'reviews:add_review',

            # Online app
            'online:add_online_rec',
    ),
    ids=[
        'Страница выхода',
        'Сброс пароля',
        'Создание отзыва',
        'Создание онлайн-записи',
    ]
)
def test_pages_availability_for_authorized_user(author_client, name):
    """
    Тестирует доступность страниц для авторизированных пользователей.

    Проверяет, что указанные URL-адреса:
    - Возвращают статус 200 OK
    - Требует аутентификации
    - Доступны без дополнительных параметров

    Параметры теста:
    - name: Имя URL-шаблона в формате 'app:url_name'
    """
    url = reverse(name)
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'Страница {name} должна быть доступна авторизированным пользователям.'
        f' Получен статус: {response.status_code}'
    )


@pytest.mark.parametrize(
    'client_fixture, expected_status',
    [
        ('not_author_client', HTTPStatus.NOT_FOUND),
        ('author_client', HTTPStatus.OK)
    ]
)
@pytest.mark.parametrize(
    ('url_name', 'url_kwargs'),
    [
        ('users:profile', {'username': 'Автор'}),
        ('users:edit_profile', {'username': 'Автор'}),
        ('reviews:update_review', {'pk': 1}),
        ('reviews:delete_review', {'pk': 1}),
        ('online:update_online_rec', {'pk': 1}),
        ('online:delete_online_rec', {'pk': 1}),
    ],
    ids=[
        'Профиль пользователя',
        'Редактирование профиля',
        'Редактирование отзыва',
        'Удаление отзыва',
        'Редактирование записи',
        'Удаление записи',
    ]
)
def test_access_control(
        request,
        client_fixture,
        expected_status,
        url_name,
        url_kwargs,
        review,
        online_rec
):
    """
        Тестирует контроль доступа к страницам для разных типов пользователей.

        Проверяет, что указанные URL-адреса:
        - Возвращают ожидаемый статус ответа (OK или NOT_FOUND)
        - Доступны только авторам связанных объектов (отзывов, записей) или владельцам профиля
        - Корректно обрабатывают динамические параметры (pk объектов)

        Параметры теста:
        - client_fixture: Фикстура клиента (author_client/not_author_client)
        - expected_status: Ожидаемый HTTP-статус ответа
        - url_name: Имя URL-шаблона в формате 'app:url_name'
        - url_kwargs: Параметры для формирования URL (username/pk)
        - review/online_rec: Фикстуры тестовых объектов для проверки доступа

        Тест параметризован для проверки:
        - Разных типов клиентов (автор/не автор)
        - Набора защищенных страниц (профиль, редактирование, удаление)
        - Динамической подстановки pk из тестовых объектов
        """
    client = request.getfixturevalue(client_fixture)

    # Обработка динамических pk
    if url_kwargs and 'pk' in url_kwargs:
        model = review if 'review' in url_name else online_rec
        url_kwargs['pk'] = model.pk
    url = reverse(url_name, kwargs=url_kwargs or None)
    response = client.get(url)
    assert response.status_code == expected_status, (
        f'Ошибка доступа к {url_name} с параметрами {url_kwargs}: '
        f'получен статус {response.status_code}, '
        f'ожидался {expected_status} для клиента {client_fixture}'
    )

