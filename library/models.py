from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    fans_count = models.IntegerField(default=0)
    ratings_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    text_reviews_count = models.IntegerField(default=0)
    work_ids = models.JSONField(blank=True, null=True)  # Store work IDs as JSON

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    ratings_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    text_reviews_count = models.IntegerField(default=0)
    work_ids = models.JSONField(blank=True, null=True)
    book_ids = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title

    def __str__(self):
        return self.title
