from django.contrib.auth import get_user_model
from django.test import TestCase

from reviews.models import Review

User = get_user_model()


class ReviewModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password="password123")
        self.review = Review.objects.create(
            text='Текст отзыва',
            author=self.user,
        )

    def test_create_review(self):
        """Тест создания отзыва."""
        self.assertEqual(self.review.text, 'Текст отзыва')
        self.assertEqual(self.review.author, self.user)

    def test_update_review(self):
        """Тест изменения отзыва."""
        new_text = 'Новый текст отзыва'
        self.review.text = new_text
        self.review.save()
        updated_review = Review.objects.get(pk=self.review.pk)
        self.assertEqual(updated_review.text, new_text)

    def test_delete_review(self):
        """Тест удаления отзыва."""
        self.review.delete()
        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(pk=self.review.pk)

    def test_update_review_by_author(self):
        """Тест изменения отзыва автором."""
        self.client.force_login(self.user)
        new_text = 'Новый текст отзыва'
        response = self.client.post('reviews:edit_comment',
                                    data={'text': new_text})
        updated_review = Review.objects.get(pk=self.review.pk)
        self.assertEqual(updated_review.text, new_text)

    def test_delete_review_by_author(self):
        """Тест удаления отзыва автором."""
        self.client.force_login(self.user)
        response = self.client.delete('reviews:delete_comment',
                                      pk=self.review.pk)
        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(pk=self.review.pk)
