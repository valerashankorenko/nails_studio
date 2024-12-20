# Nails studio

## О проекте

Сайт для студии маникюра RumNails:

Уже реализовано:
- Адаптивная верстка для всех устройств.
- Административная панель на русском языке для управления контентом.
- Страница с описанием услуг и прайс-листом.
- Галерея работ мастеров (карусель).
- Страница с контактной информацией и интерактивной картой.
- Страница с отзывами клиентов.
- Страница с полезными советами для клиентов.
- Личный кабинет с возможностью редактирования профиля и отзывов.
- Отправка письма для сброса пароля через почтовый сервер Яндекс.
- Наполнение базы данных тестовыми данными.

В разработке/планируется:
- Онлайн-запись на услуги.
- Интеграция Telegram-бота для оповещений.

## Автор проекта:
Валерий Шанкоренко<br/>
Github: 👉 [Valera Shankorenko](https://github.com/valerashankorenko)<br/>
Telegram: 📱 [@valeron007](https://t.me/valeron007)<br/>
E-mail: 📧 valerashankorenko@yandex.by<br/>

## Стек технологий
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [SQLite](https://www.sqlite.org/)

## Как запустить проект локально:
1. Клонировать репозиторий и перейти в его директорию в командной строке:
```shell
git clone git@github.com:valerashankorenko/nails_studio.git
```
2. Переход в директорию nails_studio
```shell
cd nails_studio
```
3. Cоздать и активировать виртуальное окружение:
 - для Linux/MacOS
```shell
python3 -m venv venv
source venv/bin/activate
```
- для Windows
```shell
python -m venv venv
source venv/Scripts/activate
```
4. Обновить пакетный менеджер pip
```shell
python3 -m pip install --upgrade pip
```
5. Установить зависимости из файла requirements.txt:
```shell
pip install -r requirements.txt
```
6. Применение миграций
```shell
python manage.py migrate
```
7. Создать суперпользователя
```shell
python manage.py createsuperuser
```
8. Наполнение базы данных тестовыми данными
```shell
python manage.py load_database
python manage.py load_datainfo
```
9. В корневой директории создать файл .env и заполнить своими данными:
```
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=секретный ключ Django
YANDEX_EMAIL_USER=почта Яндекс
YANDEX_EMAIL_PASSWORD=пароль приложения почты Яндекс
```
10. Запуск проекта
```shell
python manage.py runserver
```
