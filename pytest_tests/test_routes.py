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

    try:
        response = client.get(url)
    except Exception as e:
        pytest.fail(f'Ошибка при обращении к странице {name}: {str(e)}')

    assert response.status_code == HTTPStatus.OK, (
        f'Страница {name} должна быть доступна анонимным пользователям. '
        f'Получен статус: {response.status_code}'
    )


@pytest.mark.parametrize(
    'name',
    (
            # Users app
            'logout',

            # Reviews app
            'reviews:add_review',

            # Online app
            'online:add_online_rec',
    ),
    ids=[
        'Страница выхода',
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

    try:
        response = author_client.get(url)
    except Exception as e:
        pytest.fail(f'Ошибка при обращении к странице {name}: {str(e)}')

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
        # Users app
        ('users:profile', {'username': 'Автор'}),
        ('users:edit_profile', None),
        ('password_reset', None),

        # Reviews app
        ('reviews:update_review', {'pk': 1}),
        ('reviews:delete_review', {'pk': 1}),

        # Online app
        ('online:update_online_rec', {'pk': 1}),
        ('online:delete_online_rec', {'pk': 1}),
    ],
    ids=[
        'Профиль пользователя',
        'Редактирование профиля',
        'Сброс пароля',
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
    client = request.getfixturevalue(client_fixture)

    # Подставляем актуальные pk из фикстур
    if url_kwargs and 'pk' in url_kwargs:
        if 'review' in url_name:
            url_kwargs['pk'] = review.pk
        else:
            url_kwargs['pk'] = online_rec.pk

    # Для профиля подставляем правильный username
    if url_name == 'users:profile':
        user = request.getfixturevalue(client_fixture.replace('_client', ''))
        url_kwargs['username'] = user.username

    try:
        url = reverse(url_name, kwargs=url_kwargs or None)
    except Exception as e:
        pytest.fail(f'Ошибка формирования URL для {url_name}: {str(e)}')

    response = client.get(url)
    assert response.status_code == expected_status, (
        f'Ошибка доступа к {url_name} с параметрами {url_kwargs}: '
        f'получен статус {response.status_code}, '
        f'ожидался {expected_status} для клиента {client_fixture}'
    )

