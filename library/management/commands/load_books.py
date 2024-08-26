import json
from django.core.management.base import BaseCommand
from django.db import transaction

from library.models import Author, Book


class Command(BaseCommand):
    help = 'Load JSON Lines data into the database in chunks'

    def handle(self, *args, **kwargs):
        chunk_size = 1000  # Number of records per chunk
        authors_to_create = []
        books_to_create = []

        # Replace with the path to your JSON Lines file
        file_path = '/Users/muhammad/PycharmProjects/django-assessment/authors.json'

        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                entry = json.loads(line.strip())

                # Prepare author data
                author_data = {
                    'name': entry['name'],
                    'gender': entry.get('gender', ''),
                    'image_url': entry.get('image_url', ''),
                    'about': entry.get('about', ''),
                    'fans_count': entry.get('fans_count', 0),
                    'ratings_count': entry.get('ratings_count', 0),
                    'average_rating': entry.get('average_rating', 0.0),
                    'text_reviews_count': entry.get('text_reviews_count', 0),
                    'work_ids': entry.get('work_ids', []),
                }

                # Add to list
                authors_to_create.append(author_data)

                # Prepare book data
                for book_id in entry.get('book_ids', []):
                    book_data = {
                        'title': f"Book {book_id}",  # Adjust title based on actual data
                        'author': entry['name'],  # We'll link this later
                        'ratings_count': entry.get('ratings_count', 0),
                        'average_rating': entry.get('average_rating', 0.0),
                        'text_reviews_count': entry.get('text_reviews_count', 0),
                        'work_ids': entry.get('work_ids', []),
                        'book_ids': entry.get('book_ids', []),
                    }
                    books_to_create.append(book_data)

                # Process the chunk if it reaches the specified size
                if line_number % chunk_size == 0:
                    self.process_chunk(authors_to_create, books_to_create)
                    # Reset lists for next chunk
                    authors_to_create = []
                    books_to_create = []

            # Process any remaining records
            if authors_to_create or books_to_create:
                self.process_chunk(authors_to_create, books_to_create)

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))

    def process_chunk(self, authors_data, books_data):
        with transaction.atomic():
            # Bulk create authors
            authors = [Author(**data) for data in authors_data]
            Author.objects.bulk_create(authors, ignore_conflicts=True)

            # Fetch authors to link with books
            author_dict = {author.name: author for author in Author.objects.all()}

            # Prepare book data with author references
            books_to_create = [
                Book(
                    title=data['title'],
                    author=author_dict[data['author']],
                    ratings_count=data['ratings_count'],
                    average_rating=data['average_rating'],
                    text_reviews_count=data['text_reviews_count'],
                    work_ids=data['work_ids'],
                    book_ids=data['book_ids']
                ) for data in books_data
            ]

            # Bulk create books
            Book.objects.bulk_create(books_to_create, ignore_conflicts=True)
