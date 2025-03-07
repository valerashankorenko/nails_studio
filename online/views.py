from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from datetime import datetime

from online.forms import OnlineRecForm
from online.models import OnlineRec


class GetAvailableTimeSlotsView(View):
    """
    Представление для получения доступных временных слотов.
    """
    def get(self, request, *args, **kwargs):
        appointment_date = request.GET.get('appointment_date')
        if not appointment_date:
            return JsonResponse({'time_slots': []})

        try:
            # Преобразуем строку даты в объект date
            selected_date = datetime.strptime(
                appointment_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Неверный формат даты.'}, status=400)

        # Получаем занятые временные слоты для выбранной даты
        occupied_slots = OnlineRec.objects.filter(
            appointment_date=selected_date
        ).values_list('appointment_time', flat=True)

        # Приводим занятые слоты к формату HH:MM
        occupied_slots = [slot.strftime('%H:%M') for slot in occupied_slots]

        # Генерируем все возможные слоты
        start_hour = 8
        end_hour = 19
        time_slots = []

        # Текущее время и дата с учетом временной зоны
        now = timezone.localtime(timezone.now())
        current_time = now.time()
        current_date = now.date()

        for hour in range(start_hour, end_hour + 1):
            time_slot = f'{hour:02}:00'
            slot_time = datetime.strptime(time_slot, '%H:%M').time()

            # Проверяем, не занят ли слот и не прошел ли он
            if time_slot not in occupied_slots:
                if selected_date > current_date or (
                        selected_date == current_date
                        and slot_time > current_time):
                    time_slots.append((time_slot, time_slot))

        # Если нет свободных слотов
        if not time_slots:
            return JsonResponse(
                {'error': 'Извините свободное время закончилось.'
                          'Запишитесь на другую дату.'})

        return JsonResponse({'time_slots': time_slots})


class OnlineRecCreateView(LoginRequiredMixin, CreateView):
    """Создание онлайн-записи, требующее логина."""
    model = OnlineRec
    form_class = OnlineRecForm
    template_name = 'online_rec/online_rec_add.html'
    success_url = reverse_lazy('online:add_online_rec')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['get_available_time_slots_url'] = (
            reverse_lazy('online:get_available_time_slots'))
        return context

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
            form.add_error(
                None, 'Вы не можете создать более 3 записей в месяц. '
                      'Пожалуйста, запишитесь на другой месяц.')
            return self.form_invalid(form)

        messages.success(self.request, 'Запись успешно создана!')
        return super().form_valid(form)

    def form_invalid(self, form):
        appointment_date = form.cleaned_data.get('appointment_date')
        if appointment_date and appointment_date < timezone.now().date():
            form.add_error(
                'appointment_date',
                'Вы не можете записаться на прошедшую дату. '
                'Пожалуйста, выберите будущую дату.'
            )
        return super().form_invalid(form)


class OnlineRecUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение онлайн-записи, требующее логина."""
    model = OnlineRec
    form_class = OnlineRecForm
    template_name = 'online_rec/online_rec_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['get_available_time_slots_url'] = (
            reverse_lazy('online:get_available_time_slots'))
        return context

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

        original_date = self.object.appointment_date
        original_time = self.object.appointment_time
        new_date = form.cleaned_data['appointment_date']
        new_time = form.cleaned_data['appointment_time']

        first_day_of_month = appointment_date.replace(day=1)
        last_day_of_month = (
            (first_day_of_month + timezone.timedelta(days=32))
            .replace(day=1)
            - timezone.timedelta(days=1)
        )

        user_appointments_this_month = OnlineRec.objects.filter(
            user=self.request.user,
            appointment_date__range=(first_day_of_month, last_day_of_month)
        ).exclude(pk=self.object.pk)

        if user_appointments_this_month.count() >= 3:
            form.add_error(
                None,
                'Вы не можете иметь более 3 записей в месяц. '
                'Пожалуйста, перенесите запись на другой месяц.'
            )
            return self.form_invalid(form)

        if form.cleaned_data.get('service_type'):
            form.instance.service_type = form.cleaned_data['service_type']

        if (original_date != new_date) or (original_time != new_time):
            form.instance.service_status = 'postponed'

        messages.success(self.request, 'Запись успешно обновлена!')
        return super().form_valid(form)

    def form_invalid(self, form):
        appointment_date = form.cleaned_data.get('appointment_date')
        if appointment_date and appointment_date < timezone.now().date():
            form.add_error(
                'appointment_date',
                'Нельзя выбрать прошедшую дату. Выберите будущую дату.'
            )
        return super().form_invalid(form)


class OnlineRecDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление(отмена) онлайн-записи, требующее логина."""
    model = OnlineRec
    template_name = 'online_rec/online_rec_confirm_delete.html'
    success_url = reverse_lazy('pages:index')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
