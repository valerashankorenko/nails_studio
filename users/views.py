import locale
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import UpdateView, CreateView, DetailView

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
    Просмотр профиля пользователя
    """
    model = User
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_list'] = Review.objects.filter(author=self.object)

        locale.setlocale(locale.LC_TIME, 'ru_RU')

        # Получаем текущий месяц и год
        current_month = timezone.now().month
        current_year = timezone.now().year

        # Получаем месяц и год из GET параметров, если они есть
        month = int(self.request.GET.get('month', current_month))
        year = int(self.request.GET.get('year', current_year))

        # Фильтруем записи по выбранному месяцу и году
        context['online_rec'] = OnlineRec.objects.filter(
            user=self.object,
            appointment_date__month=month,
            appointment_date__year=year
        )

        # Передаем список доступных месяцев и текущий месяц
        context['months'] = [
            datetime(2023, m, 1).strftime('%B') for m in range(1, 13)
        ]  # Список названий месяцев

        context['years'] = range(current_year - 1,
                                 current_year + 1)
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

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super(ProfileUpdateView, self).form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('users:profile',
                            kwargs={'username': self.request.user.username})
