import locale
from datetime import datetime

from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import UpdateView, CreateView, DetailView, DeleteView

from online.models import OnlineRec
from reviews.models import Review
from users.forms import ProfileCreateUpdateForm

User = get_user_model()


class ProfileCreateView(CreateView):
    """
    Создание пользователя
    """
    model = User
    form_class = ProfileCreateUpdateForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр профиля пользователя с проверкой прав доступа
    """
    model = User
    template_name = 'users/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        user = get_object_or_404(
            User,
            username=self.kwargs.get(self.slug_url_kwarg)
        )

        if user != self.request.user:
            raise Http404('Доступ к чужому профилю запрещен')

        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_list'] = Review.objects.filter(author=self.object)

        locale.setlocale(locale.LC_TIME, 'ru_RU')
        current_month = timezone.now().month
        current_year = timezone.now().year

        month = int(self.request.GET.get('month', current_month))
        year = int(self.request.GET.get('year', current_year))

        context['online_rec'] = OnlineRec.objects.filter(
            user=self.object,
            appointment_date__month=month,
            appointment_date__year=year
        )

        context['months'] = [
            datetime(2023, m, 1).strftime('%B') for m in range(1, 13)
        ]
        context['years'] = range(current_year - 1, current_year + 1)
        context['selected_month'] = month
        context['selected_year'] = year

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование профиля, требующее логина.
    """
    model = User
    form_class = ProfileCreateUpdateForm
    template_name = 'users/user.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):

        obj = get_object_or_404(
            User, username=self.kwargs.get(self.slug_url_kwarg)
        )

        if obj != self.request.user:
            raise Http404('Редактирование чужого профиля запрещено')
        return obj

    def get_success_url(self):
        return reverse_lazy(
            'users:profile',
            kwargs={'username': self.request.user.username}
        )


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление профиля, требующее логина.
    """
    model = User
    template_name = 'users/profile_confirm_delete.html'
    success_url = reverse_lazy('pages:index')
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if user != self.request.user:
            raise Http404('Удаление чужого профиля запрещено')
        return user

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        logout(request)
        return response
