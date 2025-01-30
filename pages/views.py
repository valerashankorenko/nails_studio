from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from http import HTTPStatus

from pages.models import PriceList,PriceList1, Foto, Info


class IndexPage(TemplateView):
    """
    Представление для главной страницы сайта.
    """
    template_name = 'pages/index.html'


class PriceListView(ListView):
    """
    Представление для отображения прайс-листа.
    """
    template_name = 'pages/price.html'
    context_object_name = 'price_list'

    def get_context_data(self, **kwargs):
        # Получаем контекст от родительского класса
        context = super().get_context_data(**kwargs)

        # Добавляем второй прайс-лист в контекст
        context['price_list1'] = PriceList1.objects.all()

        return context

    def get_queryset(self):
        # Возвращаем первый прайс-лист
        return PriceList.objects.all()


class FotoPage(TemplateView):
    """
    Представление для отображения фотографий.
    """
    template_name = 'pages/foto.html'

    def get_context_data(self, **kwargs):
        """
        Добавляет список всех объектов Foto в контекст.
        """
        context = super().get_context_data(**kwargs)
        context['fotos'] = Foto.objects.all()
        return context


class ContactPage(TemplateView):
    """
    Представление для страницы контактов.
    """
    template_name = 'pages/contact.html'


class InfoPage(ListView):
    """
    Представление для отображения списка советов.
    """
    model = Info
    template_name = 'pages/info.html'
    context_object_name = 'infos'
    ordering = ['-id']
    paginate_by = 3


class DetailInfoPage(DetailView):
    """
    Представление для отображения конкретного совета.
    """
    model = Info
    template_name = 'pages/detail_info.html'
    context_object_name = 'info'

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return get_object_or_404(Info, id=id)


def page_not_found(request, exception):
    """
    Обрабатывает ошибки 404 Not Found.
    """
    return render(request,
                  'pages/404.html',
                  status=HTTPStatus.NOT_FOUND)


def csrf_failure(request, reason=''):
    """
    Обрабатывает сбои проверки токена CSRF.
    """
    return render(request,
                  'pages/403csrf.html',
                  status=HTTPStatus.FORBIDDEN)


def server_error(request):
    """
    Обрабатывает ошибки 500 Internal Server Error.
    """
    return render(request,
                  'pages/500.html',
                  status=HTTPStatus.INTERNAL_SERVER_ERROR)


def permission_denied(request, exception):
    """
    Обрабатывает ошибки 403 Forbidden.
    """
    return render(request,
                  'pages/403csrf.html',
                  status=HTTPStatus.FORBIDDEN)
