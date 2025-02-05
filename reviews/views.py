import locale

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import (CreateView, UpdateView,
                                  DeleteView, ListView, View)
from reviews.forms import ReviewForm
from reviews.models import Review, Like


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
    success_url = reverse_lazy('pages:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        if Review.objects.filter(author=self.request.user).exists():
            form.add_error(
                None,
                'Вы можете оставить только один отзыв.'
            )
            return self.form_invalid(form)
        return super().form_valid(form)


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    """Обновление отзыва, требующее логина."""
    model = Review
    fields = ['text']
    template_name = 'reviews/review_update.html'
    success_url = reverse_lazy('pages:index')

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            Review, pk=self.kwargs['pk'], author=self.request.user
        )
        return obj

    def form_valid(self, form):
        review = form.save(commit=False)
        review.is_published = False
        review.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = self.get_object()
        return context


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    """Удаление отзыва, требующее логина."""
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    success_url = reverse_lazy('reviews:review')

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            Review, pk=self.kwargs['pk'], author=self.request.user
        )
        return obj

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class LikeView(LoginRequiredMixin, View):
    """Добавление лайка на отзыв."""
    def post(self, request, pk):
        review = get_object_or_404(
            Review,
            pk=pk
        )
        like, created = Like.objects.get_or_create(
            user=request.user,
            review=review
        )

        if created:
            liked = True
        else:
            like.delete()
            liked = False
        like_count = review.like_count()
        return JsonResponse(
            {'liked': liked,
             'like_count': like_count}
        )
