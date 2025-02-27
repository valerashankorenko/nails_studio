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
- Pytest.
- Онлайн-запись на услуги.

В разработке/планируется:
- Интеграция Telegram-бота для оповещений.

## Автор проекта:
Валерий Шанкоренко<br/>
Github: 👉 [Valera Shankorenko](https://github.com/valerashankorenko)<br/>
Telegram: 📱 [@valeron007](https://t.me/valeron007)<br/>
E-mail: 📧 valerashankorenko@yandex.by<br/>

## Стек технологий
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=flat-square&logo=bootstrap&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=flat-square&logo=css3&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-EBEEEE?style=flat-square&logo=pillow&logoColor=black)
![Pytest](https://img.shields.io/badge/Pytest-0E5E6F?style=flat-square&logo=pytest&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)

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
7. В корневой директории создать файл .env и заполнить своими данными:
```
DJANGO_DEBUG=True(для разработки)
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=секретный ключ Django
YANDEX_EMAIL_USER=почта Яндекс
YANDEX_EMAIL_PASSWORD=пароль приложения почты Яндекс
Данные для суперпользователя
DJANGO_SUPERUSER_USERNAME=your_first_username
DJANGO_SUPERUSER_EMAIL=email
DJANGO_SUPERUSER_PASSWORD=password
DJANGO_SUPERUSER_FIRST_NAME=your_first_name
DJANGO_SUPERUSER_LAST_NAME=your_last_name
DJANGO_SUPERUSER_PHONE_NUMBER=your_phone_number(Формат номера: +375XXXXXXXXX)
```
8. Создать суперпользователя
```shell
python manage.py create_superuser
```
9. Наполнение базы данных тестовыми данными
```shell
python manage.py load_database
python manage.py load_datainfo
```
10. Запуск тестов 
```shell
pytest 
или
python manage.py test
```
11. Запуск проекта
```shell
python manage.py runserver
```
