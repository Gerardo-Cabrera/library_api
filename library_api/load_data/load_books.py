import json
from library_api.models import Book, Author

def load_books():
    try:
        with open('books.json', 'r') as file:
            for line in file:
                try:
                    # ry convert the line in a JSON object
                    book_data = json.loads(line)
                    # Get the book's authors
                    author_ids = [author['id'] for author in book_data['authors']]
                    authors = Author.objects.filter(id__in=author_ids)
                    
                    # Create or update the book
                    book, created = Book.objects.get_or_create(
                        book_id=book_data['id'],
                        defaults={
                            'title': book_data.get('title', ''),
                            'isbn': book_data.get('isbn', ''),
                            'isbn13': book_data.get('isbn13', ''),
                            'asin': book_data.get('asin', ''),
                            'language': book_data.get('language', ''),
                            'average_rating': book_data.get('average_rating', 0.0),
                            'ratings_count': book_data.get('ratings_count', 0),
                            'text_reviews_count': book_data.get('text_reviews_count', 0),
                            'publication_date': book_data.get('publication_date', ''),
                            'original_publication_date': book_data.get('original_publication_date', ''),
                            'format': book_data.get('format', ''),
                            'edition_information': book_data.get('edition_information', ''),
                            'image_url': book_data.get('image_url', ''),
                            'publisher': book_data.get('publisher', ''),
                            'num_pages': book_data.get('num_pages', None),
                            'series_name': book_data.get('series_name', ''),
                            'series_position': book_data.get('series_position', ''),
                            'description': book_data.get('description', ''),
                            'work_id': book_data.get('work_id', ''),
                        }
                    )
                    
                    # Asign the author or authors to the book
                    if created:
                        book.authors.set(authors)
                        book.save()
                        print(f"Book '{book.title}' added successfully with authors {[a.name for a in authors]}.")
                    else:
                        print(f"Book '{book.title}' already exists.")

                except Exception as e:
                    print(f"Error adding book '{book_data['title']}': {e}")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"General error: {e}")

    print("Load completed successfully")

# Call the function to charge the books data
load_books()
