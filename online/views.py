from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
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

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_slots'] = [f'{hour:02}:00' for hour in range(8, 20)]
        return context


class OnlineRecUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение онлайн-записи, требующее логина."""
    model = OnlineRec
    form_class = OnlineRecForm
    template_name = 'online_rec/online_rec_update.html'

    def form_valid(self, form):
        if OnlineRec.objects.filter(
                user=self.request.user
        ).exclude(pk=self.object.pk).count() >= 3:
            form.add_error(None, 'Вы можете записаться только на 3 услуги.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('pages:index')


class OnlineRecDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление онлайн-записи, требующее логина."""
    model = OnlineRec
    template_name = 'online_rec/online_rec_confirm_delete.html'
    success_url = reverse_lazy('pages:index')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
