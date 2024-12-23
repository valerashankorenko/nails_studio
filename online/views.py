from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView

from online.forms import OnlineRecForm
from online.models import OnlineRec


class OnlineRecCreateView(LoginRequiredMixin, CreateView):
    """Создание онлайн-записи, требующее логина."""
    model = OnlineRec
    form_class = OnlineRecForm
    template_name = 'online_rec/online_rec_add.html'

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Проверка на максимальное количество услуг
        if OnlineRec.objects.filter(user=self.request.user).count() >= 3:
            form.add_error(None, 'Вы можете записаться только на 3 услуги.')
            return self.form_invalid(form)

        # Проверка на дубликаты по дате и времени
        if OnlineRec.objects.filter(
                user=self.request.user,
                appointment_date=form.instance.appointment_date,
                appointment_time=form.instance.appointment_time
        ).exists():
            form.add_error(None, 'Запись на это время уже существует.')
            return self.form_invalid(form)

        # Проверка на прошлое время
        appointment_datetime = datetime.combine(
            form.instance.appointment_date,
            form.instance.appointment_time
        )
        if appointment_datetime < timezone.now():
            form.add_error(None, 'Время не может быть в прошлом.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_slots'] = [f'{hour:02}:00' for hour in
                                 range(8, 21)]  # От 8:00 до 20:00
        return context


class OnlineRecUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение онлайн-записи, требующее логина."""
    model = OnlineRec
    fields = ['appointment_date',
              'appointment_time',
              'service_type',
              'service_manicure',
              'service_pedicure']
    template_name = 'online_rec/online_rec_update.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('pages:index')


class OnlineRecDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление онлайн-записи, требующее логина."""
    model = OnlineRec
    template_name = 'online_rec/online_rec_confirm_delete.html'
    success_url = reverse_lazy('pages:index')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
