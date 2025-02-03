import pytest
from django.test.client import Client


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Фикстура для автоматического предоставления доступа к БД во всех тестах.

    Особенности:
    - Автоматически активируется для всех тестов благодаря autouse=True
    - Позволяет избежать необходимости маркировать каждый тест декоратором @pytest.mark.django_db
    """
    pass


@pytest.fixture
def author(django_user_model):
    """
    Фикстура создающая пользователя с ролью автора.
    """
    return django_user_model.objects.create(
        username='Автор',
        phone_number='+375291111111',
        email='author@test.ru'
    )


@pytest.fixture
def not_author(django_user_model):
    """
    Фикстура создающая пользователя без прав автора.
    """
    return django_user_model.objects.create(
        username='Не автор',
        phone_number='+375292222222',
        email='not_author@test.ru'
    )


@pytest.fixture
def author_client(author):
    """
    Фикстура создающая аутентифицированный клиент для автора.
    """
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    """
    Фикстура создающая аутентифицированный клиент для обычного пользователя.
    """
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def review(author):
    """
    Фикстура создающая тестовый отзыв.
    """
    from reviews.models import Review
    return Review.objects.create(
        author=author,
        text='Тестовый отзыв'
    )


@pytest.fixture
def online_rec(author):
    """
    Фикстура создающая тестовую запись на онлайн-сервис.
    """
    from online.models import OnlineRec
    return OnlineRec.objects.create(
        user=author,
        service_type='manicure',
        appointment_date='2023-01-01',
        appointment_time='12:00'
    )
