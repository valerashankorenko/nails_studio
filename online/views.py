from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
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
    success_url = reverse_lazy('online:add_online_rec')

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Получаем текущую дату и определяем границы месяца из даты записи
        appointment_date = form.cleaned_data['appointment_date']
        first_day_of_month = appointment_date.replace(day=1)
        last_day_of_month = ((first_day_of_month
                              + timezone.timedelta(days=32)).replace(day=1)
                             - timezone.timedelta(days=1))

        user_appointments_this_month = OnlineRec.objects.filter(
            user=self.request.user,
            appointment_date__range=(first_day_of_month, last_day_of_month)
        )

        if user_appointments_this_month.count() >= 3:
            form.add_error(None, 'Вы превысили лимит записей на месяц.')
            return self.form_invalid(form)

        messages.success(self.request, 'Запись успешно создана!')
        return super().form_valid(form)

    def form_invalid(self, form):
        if form.cleaned_data.get('appointment_date') < timezone.now().date():
            form.add_error('appointment_date',
                           'Вы не можете записаться на прошедшую дату. '
                           'Пожалуйста, выберите будущую дату.')
        return super().form_invalid(form)


class OnlineRecUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение онлайн-записи, требующее логина."""
    model = OnlineRec
    form_class = OnlineRecForm
    template_name = 'online_rec/online_rec_update.html'

    def get_queryset(self):
        return OnlineRec.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404('У вас нет прав на редактирование этой записи.')
        return obj

    def get_success_url(self):
        return reverse_lazy(
            'online:update_online_rec',
            kwargs={'pk': self.object.pk}
        )

    def form_valid(self, form):
        form.instance.user = self.request.user
        appointment_date = form.cleaned_data['appointment_date']
        first_day_of_month = appointment_date.replace(day=1)
        last_day_of_month = ((first_day_of_month + timezone.timedelta(days=32)
                              ).replace(day=1) - timezone.timedelta(days=1))

        user_appointments_this_month = OnlineRec.objects.filter(
            user=self.request.user,
            appointment_date__range=(first_day_of_month, last_day_of_month)
        ).exclude(pk=self.object.pk)

        if user_appointments_this_month.count() >= 2:
            form.add_error(None, 'Вы не можете иметь более 3 записей '
                                 'в месяц. Пожалуйста, перенесите запись '
                                 'на другой месяц.')
            return self.form_invalid(form)

        form.instance.service_status = 'postponed'
        messages.success(self.request, 'Запись успешно перенесена!')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Проверка на прошедшую дату
        if 'appointment_date' in form.cleaned_data:
            if form.cleaned_data['appointment_date'] < timezone.now().date():
                form.add_error('appointment_date',
                               'Вы не можете записаться на прошедшую дату. '
                               'Пожалуйста, выберите будущую дату.')

        return super().form_invalid(form)


class OnlineRecDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление(отмена) онлайн-записи, требующее логина."""
    model = OnlineRec
    template_name = 'online_rec/online_rec_confirm_delete.html'
    success_url = reverse_lazy('pages:index')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
