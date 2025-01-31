import pytest

from django.test.client import Client


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(
        username='Автор',
        phone_number='+375291111111',
        email='author@test.ru'
    )


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(
        username='Не автор',
        phone_number='+375292222222',
        email='not_author@test.ru'
    )


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def review(author):
    from reviews.models import Review
    return Review.objects.create(
        author=author,
        text='Тестовый отзыв'
    )


@pytest.fixture
def online_rec(author):
    from online.models import OnlineRec
    return OnlineRec.objects.create(
        user=author,
        service_type='manicure',
        appointment_date='2023-01-01',
        appointment_time='12:00'
    )
