# library_app/recommendations.py

from accounts.models import Book
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_book_recommendations(user):
    favorite_books = user.profile.favorite_books.all()

    if not favorite_books.exists():
        return []

    # Get a list of all books excluding the user's favorites
    all_books = Book.objects.exclude(id__in=favorite_books.values_list('id', flat=True))

    if not all_books.exists():
        return []

    # Use descriptions for similarity
    all_books_list = list(all_books)
    favorite_books_list = list(favorite_books)

    all_books_descriptions = [book.description for book in all_books_list]
    favorite_books_descriptions = [book.description for book in favorite_books_list]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_books_descriptions + favorite_books_descriptions)

    # Calculate similarity scores
    similarity_scores = cosine_similarity(tfidf_matrix[-len(favorite_books_list):],
                                          tfidf_matrix[:-len(favorite_books_list)])

    # Get the top recommended books based on similarity
    recommended_indices = similarity_scores.mean(axis=0).argsort()[-5:][::-1]
    recommended_books = [all_books_list[i] for i in recommended_indices]

    return recommended_books
