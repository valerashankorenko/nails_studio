from django.urls import reverse
import pytest

from reviews.models import Review


def test_single_review_per_user(author, review):
    """
    Тестирует ограничение на создание только одного отзыва от одного пользователя.

    Проверяет, что при попытке создать второй отзыв тем же автором возникает исключение
    с нарушением UNIQUE ограничения в базе данных.
    """
    with pytest.raises(Exception) as exc_info:
        Review.objects.create(author=author, text='Еще один отзыв')
    assert 'UNIQUE constraint' in str(exc_info.value)


def test_reviews_count_on_page(client, seven_reviews):
    """
    Тестирует количество отображаемых отзывов на странице.

    Проверяет, что на странице списка отзывов отображается не более 6 записей,
    даже если в базе данных их больше.
    """
    url = reverse('reviews:review')
    response = client.get(url)
    reviews = response.context['review_list']
    assert len(reviews) == 6, 'На странице должно быть не более 6 отзывов'


def test_reviews_order(client, older_review, newer_review):
    """
    Тестирует порядок отображения отзывов на странице.

    Проверяет, что отзывы упорядочены по дате создания в убывающем порядке:
    сначала самый новый, затем более старые.
    """
    url = reverse('reviews:review')
    response = client.get(url)
    reviews = response.context['review_list']
    assert list(reviews) == [newer_review, older_review],\
        'Неверный порядок отзывов'


def test_info_count_on_page(client, four_infos):
    """
    Тестирует количество отображаемых советов на странице.

    Проверяет, что на странице списка советов отображается не более 3 записей,
    даже если в базе данных их больше.
    """
    url = reverse('pages:info')
    response = client.get(url)
    info_list = response.context['infos']
    assert len(info_list) == 3, 'На странице должно быть не более 3 советов'


def test_info_order(client, older_info, newer_info):
    """
    Тестирует порядок отображения советов на странице.

    Проверяет, что советы упорядочены по дате создания в убывающем порядке:
    сначала самый новый, затем более старые.
    """
    url = reverse('pages:info')
    response = client.get(url)
    info_list = response.context['infos']
    assert list(info_list) == [newer_info, older_info], \
        'Неверный порядок советов'


@pytest.mark.parametrize('url_name, form_name', [
    ('reviews:add_review', 'form'),
    ('online:add_online_rec', 'form'),
], ids=[
    'Форма добавления отзыва',
    'Форма онлайн-записи',
])
def test_forms_availability(url_name, form_name, client, author_client):
    """
    Тестирует доступность форм для авторизованных и неавторизованных пользователей.

    Проверяет, что:
    - Неавторизованные пользователи перенаправляются (статус 302) и не видят форму.
    - Авторизованные пользователи получают доступ к форме (статус 200) и форма присутствует в контексте.

    Параметры теста:
    - url_name: Имя URL-шаблона в формате 'app:url_name'.
    - form_name: Название переменной контекста, содержащей форму.
    """
    url = reverse(url_name)

    response = client.get(url)
    assert response.status_code == 302, 'Должен быть редирект для анонима'
    assert response.context is None, \
        'Контекст не должен передаваться при редиректе'

    response = author_client.get(url)
    assert response.status_code == 200, 'Должен быть доступен авторизованному'
    assert form_name in response.context, 'Форма должна быть в контексте'
