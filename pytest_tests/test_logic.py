from django.urls import reverse
from datetime import date, timedelta

from reviews.models import Review
from online.models import OnlineRec


def test_anonymous_cannot_create_review_or_online_rec(client):
    """
    Анонимный пользователь не может оставить отзыв и онлайн-запись
    """
    review_data = {'text': 'Анонимный отзыв'}
    response = client.post(reverse('reviews:add_review'), review_data)
    assert response.status_code == 302, 'Должен быть редирект на авторизацию'
    assert Review.objects.count() == 0, 'Отзыв не должен быть создан'

    online_data = {
        'service_type': 'manicure',
        'appointment_date': '2023-01-01',
        'appointment_time': '12:00'
    }
    response = client.post(reverse('online:add_online_rec'), online_data)
    assert response.status_code == 302, 'Должен быть редирект на авторизацию'
    assert OnlineRec.objects.count() == 0, 'Запись не должна быть создана'


def test_authorized_user_review_and_rec_limits(
        author_client,
        author,
        service_manicure,
        service_pedicure
):
    """
    Авторизированный пользователь может оставить один отзыв и онлайн записи,
    но не более 3 онлайн-записей за месяц
    """
    # Тестирование отзывов
    review_url = reverse('reviews:add_review')
    response = author_client.post(review_url, {'text': 'Тестовый отзыв'})
    assert Review.objects.filter(author=author).count() == 1, \
        'Должен быть создан 1 отзыв'

    response = author_client.post(review_url, {'text': 'Второй отзыв'})
    assert '__all__' in response.context['form'].errors, \
        'Пользователь может оставить только 1 отзыв'
    assert ('Вы можете оставить только один отзыв.'
            in response.context['form'].errors['__all__'])

    # Тестирование онлайн-записей
    online_url = reverse('online:add_online_rec')
    base_date = date.today() + timedelta(days=1)

    for i in range(3):
        data = {
            'service_type': 'manicure',
            'appointment_date': base_date,
            'appointment_time': f'{10 + i}:00',
            'service_manicure': [service_manicure.pk],

        }
        response = author_client.post(online_url, data)
        assert response.status_code == 302
        assert OnlineRec.objects.count() == i + 1

    data = {
        'service_type': 'pedicure',
        'appointment_date': base_date,
        'appointment_time': '18:00',
        'service_pedicure': [service_pedicure.pk],
    }
    response = author_client.post(online_url, data)
    assert response.status_code == 200  # Убедитесь, что форма не перенаправляет
    assert 'Вы превысили лимит записей на месяц.' in response.context[
        'form'].errors.get('__all__', []), \
        'Нельзя сделать более 3 онлайн-записей за месяц'

def test_user_can_edit_own_content(
        author_client,
        review,
        online_rec,
        service_pedicure
):
    """
    Авторизированный пользователь может редактировать
    свой отзыв и онлайн-записи
    """
    # Редактирование отзыва
    edit_review_url = reverse(
        'reviews:update_review',
        args=[review.pk]
    )
    response = author_client.post(edit_review_url,
                                  {'text': 'Обновленный текст'})
    review.refresh_from_db()
    assert review.text == 'Обновленный текст', \
        'Текст отзыва должен обновиться'

    # Редактирование онлайн-записи
    edit_rec_url = reverse(
        'online:update_online_rec',
        args=[online_rec.pk]
    )
    new_data = {
        'service_type': 'pedicure',
        'appointment_date': online_rec.appointment_date.isoformat(),
        'appointment_time': '13:00',
        'service_pedicure': [service_pedicure.pk],
    }
    response = author_client.post(edit_rec_url, new_data)
    online_rec.refresh_from_db()
    assert online_rec.service_type == 'pedicure'


def test_user_cannot_edit_others_content(not_author_client, review,
                                         online_rec):
    """
    Авторизированный пользователь не может редактировать
    чужие отзывы и онлайн-записи
    """
    edit_review_url = reverse(
        'reviews:update_review',
        args=[review.pk]
    )
    response = not_author_client.post(
        edit_review_url,
        {'text': 'Взлом'}
    )
    assert response.status_code == 404, \
        'Доступ к чужому отзыву должен быть запрещен'

    edit_rec_url = reverse(
        'online:update_online_rec',
        args=[online_rec.pk]
    )
    response = not_author_client.post(
        edit_rec_url,
        {}
    )
    assert response.status_code == 404, \
        'Доступ к чужой записи должен быть запрещен'


def test_time_slot_validation(author_client, online_rec):
    """
    Нельзя записаться на занятое время
    """
    online_url = reverse('online:add_online_rec')
    formatted_date = online_rec.appointment_date.strftime('%d.%m.%Y')
    expected_error = (f'На {formatted_date} в '
                      f'{online_rec.appointment_time} уже есть запись. '
                      'Пожалуйста, выберите другое время.')

    # Данные для дублирующей записи
    duplicate_data = {
        'service_type': online_rec.service_type,
        'appointment_date': online_rec.appointment_date.isoformat(),
        'appointment_time': online_rec.appointment_time,
    }

    # Создание первой записи
    author_client.post(online_url, duplicate_data)
    assert OnlineRec.objects.count() == 1
    # Попытка создания второй записи на то же время
    response = author_client.post(online_url, duplicate_data)

    # Проверка на наличие ошибки в форме
    assert expected_error in response.context['form'].errors['__all__'], \
        'Нельзя записаться в один день на одно и то же время'
