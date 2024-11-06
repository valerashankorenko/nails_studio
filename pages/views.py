from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from http import HTTPStatus

from pages.models import PriceList, Foto, Info


class IndexPage(TemplateView):
    template_name = 'pages/index.html'


class PriceListView(ListView):
    model = PriceList
    template_name = 'pages/price.html'
    context_object_name = 'price_list'


class FotoPage(TemplateView):
    template_name = 'pages/foto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotos'] = Foto.objects.all()
        return context


class ContactPage(TemplateView):
    template_name = 'pages/contact.html'


class InfoPage(ListView):
    model = Info
    template_name = 'pages/info.html'
    context_object_name = 'infos'
    ordering = ['-id']
    paginate_by = 3


class DetailInfoPage(DetailView):
    model = Info
    template_name = 'pages/detail_info.html'
    context_object_name = 'info'

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return get_object_or_404(Info, id=id)


def page_not_found(request, exception):
    return render(request,
                  'pages/404.html',
                  status=HTTPStatus.NOT_FOUND)


def csrf_failure(request, reason=''):
    return render(request,
                  'pages/403csrf.html',
                  status=HTTPStatus.FORBIDDEN)


def server_error(request):
    return render(request,
                  'pages/500.html',
                  status=HTTPStatus.INTERNAL_SERVER_ERROR)


def permission_denied(request, exception):
    return render(request,
                  'pages/403csrf.html',
                  status=HTTPStatus.FORBIDDEN)
