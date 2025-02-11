from django.urls import reverse
from datetime import date, timedelta

from reviews.models import Review
from online.models import OnlineRec


def test_anonymous_cannot_create_review_or_online_rec(client):
    """
    Тестирует запрет на создание отзывов и
    онлайн-записей анонимными пользователями.

    Проверяет, что при попытке создания контента без авторизации:
    1. Происходит редирект на страницу авторизации
    2. Записи не создаются в базе данных
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
    Тестирует ограничения для авторизованных пользователей
    при создании контента.

    Проверяет:
    1. Возможность оставить только один отзыв
    2. Лимит в 3 онлайн-записи в месяц
    3. Корректность сообщений об ошибках при превышении лимитов
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
    assert response.status_code == 200
    assert (('Вы не можете создать более 3 записей в месяц. '
            'Пожалуйста, создайте запись в другом месяце.')
            in response.context[
        'form'].errors.get('__all__', [])), \
        'Нельзя сделать более 3 онлайн-записей за месяц'


def test_user_can_edit_own_content(
        author_client,
        review,
        online_rec,
        service_pedicure
):
    """
    Тестирует возможность редактирования собственного контента.

    Проверяет:
    1. Успешное обновление текста отзыва
    2. Корректное изменение типа услуги в онлайн-записи
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
    Тестирует запрет на редактирование чужого контента.

    Проверяет:
    1. Возвращение ошибки 404 при попытке редактирования чужого отзыва
    2. Запрет доступа к изменению чужой онлайн-записи
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
    Тестирует валидацию временных интервалов для онлайн-записей.

    Проверяет:
    1. Невозможность создания двух записей на одно и то же время
    2. Корректность сообщения об ошибке при дублировании времени
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

    author_client.post(online_url, duplicate_data)
    assert OnlineRec.objects.count() == 1
    response = author_client.post(online_url, duplicate_data)

    assert expected_error in response.context['form'].errors['__all__'], \
        'Нельзя записаться в один день на одно и то же время'


def test_user_cannot_create_online_rec_in_past(author_client,
                                               service_manicure):
    """
    Тестирует валидацию даты при создании онлайн-записей.

    Проверяет:
    1. Невозможность создания записи на прошедшую дату
    2. Наличие ошибки в поле appointment_date
    """
    online_url = reverse('online:add_online_rec')
    past_date = date.today() - timedelta(days=1)
    data = {
        'service_type': 'manicure',
        'appointment_date': past_date,
        'appointment_time': '12:00',
        'service_manicure': [service_manicure.pk],
    }
    response = author_client.post(online_url, data)

    assert OnlineRec.objects.count() == 0, \
        'Запись на прошлую дату не должна создаваться'
    form_errors = response.context['form'].errors
    assert 'appointment_date' in form_errors, \
        'Ошибка должна быть в поле appointment_date'
    assert 'Нельзя записаться на прошедшую дату.' in form_errors[
        'appointment_date'], \
        'Должна быть ошибка о записи на прошедшую дату'
