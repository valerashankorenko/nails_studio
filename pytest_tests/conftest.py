from datetime import date, timedelta

import pytest
from django.test.client import Client
from django.utils import timezone

from pages.models import PriceList, PriceList1


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

    Особенности:
    - Связывает отзыв с автором через фикстуру author
    - Автоматически устанавливает текущее время в поле created_at
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

    Особенности:
    - Использует тестового автора в качестве пользователя
    - Фиксированные дата и время записи (2023-01-01 в 12:00)
    - Тип услуги - маникюр
    """
    from online.models import OnlineRec
    return OnlineRec.objects.create(
        user=author,
        service_type='manicure',
        appointment_date=date.today() + timedelta(days=1),
        appointment_time='12:00'
    )


@pytest.fixture
def seven_reviews(django_user_model):
    """
    Фикстура создающая 7 опубликованных отзывов от разных пользователей.

    Особенности:
    - Генерирует уникальные пользователей для каждого отзыва
    - Все отзывы помечены как опубликованные (is_published=True)
    - Используется для тестирования лимитов отображения и пагинации
    """
    from reviews.models import Review
    reviews = []
    for i in range(7):
        user = django_user_model.objects.create_user(
            username=f'user_{i}',
            password='testpass123',
            phone_number=f'+37529{i:07}',
            email=f'user_{i}@test.ru'
        )
        reviews.append(Review.objects.create(
            author=user,
            text=f'Тестовый отзыв {i}',
            is_published=True
        ))
    return reviews


@pytest.fixture
def older_review(django_user_model):
    """
    Фикстура создающая опубликованный отзыв с датой создания на день раньше текущей.

    Особенности:
    - Используется для тестирования сортировки по времени создания
    - Автор отзыва отличается от основного тестового автора
    """
    from reviews.models import Review
    user = django_user_model.objects.create(
        username='old_author',
        phone_number='+375291111112',
        email='old@test.ru'
    )

    return Review.objects.create(
        author=user,
        text='Старый отзыв',
        created_at=timezone.now() - timezone.timedelta(days=1),
        is_published=True
    )


@pytest.fixture
def newer_review(django_user_model):
    """
    Фикстура создающая опубликованный отзыв с текущей датой создания.

    Особенности:
    - Используется для тестирования сортировки по времени создания
    - Автор отзыва отличается от основного тестового автора
    """
    from reviews.models import Review
    user = django_user_model.objects.create(
        username='new_author',
        phone_number='+375291111113',
        email='new@test.ru'
    )

    return Review.objects.create(
        author=user,
        text='Новый отзыв',
        is_published=True
    )


@pytest.fixture
def four_infos():
    """
    Фикстура создающая 4 тестовых совета для страницы с информацией.

    Особенности:
    - Используется для тестирования лимита отображаемых советов
    - Каждый совет имеет последовательную нумерацию в заголовке и тексте
    """
    from pages.models import Info
    infos = []
    for i in range(4):
        info = Info.objects.create(
            title=f'Совет {i}',
            text=f'Текст совета {i}'
        )
        infos.append(info)
    return infos


@pytest.fixture
def older_info():
    """
    Фикстура создающая тестовый совет с более ранним ID.

    Особенности:
    - Используется для тестирования порядка вывода советов
    - Имитирует более старую запись в базе данных
    """
    from pages.models import Info
    return Info.objects.create(
        id=1,
        title='Старый совет',
        text='Текст'
    )


@pytest.fixture
def newer_info():
    """
    Фикстура создающая тестовый совет с более поздним ID.

    Особенности:
    - Используется для тестирования порядка вывода советов
    - Имитирует более новую запись в базе данных
    """
    from pages.models import Info
    return Info.objects.create(
        id=2,
        title='Новый совет',
        text='Текст'
    )


@pytest.fixture
def service_manicure():
    return PriceList.objects.create(service='Маникюр', price=1000)


@pytest.fixture
def service_pedicure():
    return PriceList1.objects.create(service='Педикюр', price=1500)
