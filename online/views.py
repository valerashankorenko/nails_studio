from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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
            messages.error(
                self.request,
                f'Вы не можете записаться более 3 раз в месяц '
                f'(месяц записи: {appointment_date.strftime("%B")}).<br>'
                f'Пожалуйста, сделайте запись на другой месяц.'
            )
            return redirect(self.success_url)

        messages.success(self.request, 'Запись успешно создана!')
        return super().form_valid(form)


class OnlineRecUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение онлайн-записи, требующее логина."""
    model = OnlineRec
    form_class = OnlineRecForm
    template_name = 'online_rec/online_rec_update.html'

    def get_success_url(self):
        return reverse_lazy(
            'online:update_online_rec',
            kwargs={'pk': self.object.pk}
        )

    def form_valid(self, form):
        form.instance.user = self.request.user
        appointment_date = form.cleaned_data['appointment_date']
        first_day_of_month = appointment_date.replace(day=1)
        last_day_of_month = ((first_day_of_month
                              + timezone.timedelta(days=32)).replace(day=1)
                             - timezone.timedelta(days=1))

        user_appointments_this_month = OnlineRec.objects.filter(
            user=self.request.user,
            appointment_date__range=(first_day_of_month, last_day_of_month)
        ).exclude(pk=self.object.pk)

        if user_appointments_this_month.count() >= 2:
            messages.error(
                self.request,
                f'Вы не можете иметь более 3 записей в месяц.<br>'
                f'Пожалуйста, перенесите запись на другой месяц.'
            )
            return redirect(self.get_success_url())

        form.instance.service_status = 'postponed'
        messages.success(self.request, 'Запись успешно перенесена!')
        return super().form_valid(form)


class OnlineRecDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление(отмена) онлайн-записи, требующее логина."""
    model = OnlineRec
    template_name = 'online_rec/online_rec_confirm_delete.html'
    success_url = reverse_lazy('pages:index')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
