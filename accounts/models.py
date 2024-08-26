from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from library.models import Book


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    favorite_books = models.ManyToManyField(Book, related_name='favorited_by', blank=True)

    def add_favorite(self, book):
        """Add a book to the user's favorites list, with a max limit of 20."""
        if self.favorite_books.count() >= 20:
            raise ValueError("You can only have 20 favorite books.")
        self.favorite_books.add(book)
        self.save()

    def remove_favorite(self, book):
        """Remove a book from the user's favorites list."""
        self.favorite_books.remove(book)
        self.save()

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
