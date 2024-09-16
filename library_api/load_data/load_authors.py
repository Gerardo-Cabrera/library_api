import json
from library_api.models import Author

def load_authors():
    with open('authors.json', 'r') as file:
        # Read file line by line
        for line in file:
            try:
                # Try convert the line in a JSON object
                author_data = json.loads(line)
                
                # Process and save the author information
                Author.objects.update_or_create(
                    author_id=author_data['id'],
                    defaults={
                        'name': author_data['name'],
                        'gender': author_data.get('gender', ''),
                        'image_url': author_data.get('image_url', ''),
                        'about': author_data.get('about', ''),
                        'ratings_count': author_data.get('ratings_count', 0),
                        'average_rating': author_data.get('average_rating', 0.0),
                        'text_reviews_count': author_data.get('text_reviews_count', 0),
                        'works_count': author_data.get('works_count', 0),
                        'fans_count': author_data.get('fans_count', 0),
                    }
                )
            except json.JSONDecodeError as e:
                print(f"Error de JSON en la línea: {line[:50]}... \n{str(e)}")

    print("Load completed successfully")

# Call the function to charge the authors data
load_authors()
