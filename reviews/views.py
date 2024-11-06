import locale
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from reviews.forms import ReviewForm
from reviews.models import Review


class ReviewListView(ListView):
    """Вывод списка отзывов"""
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'review_list'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(is_published=True)
        paginator = Paginator(reviews, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['reviews'] = page_obj
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        for review in page_obj:
            localized_datetime = timezone.localtime(
                review.created_at, timezone.get_current_timezone())
            review.created_at_formatted = localized_datetime.strftime(
                "%d.%m.%Y в %H:%M")
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """Создание отзыва, требующее логина."""
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_add.html'

    def get_success_url(self):
        return reverse_lazy('pages:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        if Review.objects.filter(author=self.request.user,
                                 is_published=True).exists():
            form.add_error(None,
                           'Вы можете оставить только один отзыв.')
            return self.form_invalid(form)
        return super().form_valid(form)


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    """Обновление отзыва, требующее логина."""
    model = Review
    fields = ['text']
    template_name = 'reviews/review_update.html'

    def form_valid(self, form):
        review = form.save(commit=False)
        review.is_published = False
        review.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('pages:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = self.get_object()
        return context


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    """Удаление отзыва, требующее логина."""
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    success_url = reverse_lazy('reviews:review')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)
