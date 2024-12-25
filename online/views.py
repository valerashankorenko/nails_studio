from django.contrib import messages
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
    success_url = reverse_lazy('online:add_online_rec')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Запись успешно создана!')
        return super().form_valid(form)


class OnlineRecUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение онлайн-записи, требующее логина."""
    model = OnlineRec
    form_class = OnlineRecForm
    template_name = 'online_rec/online_rec_update.html'
    success_url = reverse_lazy('online:update_online_rec')

    def form_valid(self, form):
        form.instance.user = self.get_object().user
        messages.success(self.request, 'Запись успешно изменена!')
        return super().form_valid(form)


class OnlineRecDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление онлайн-записи, требующее логина."""
    model = OnlineRec
    template_name = 'online_rec/online_rec_confirm_delete.html'
    success_url = reverse_lazy('pages:index')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
