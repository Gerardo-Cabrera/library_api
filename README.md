# Instructions
- Clone the repository in a folder of your system.
- Create the virtual environment executing this command in the console for Linux or Mac or in **CMD** for Windows: **python -m venv env** or **python3 -m venv env** to install project dependencies (**env** is a convention can any name).
- In the same directory where created the virtual environment, enter to this executing this command in the console for Linux or Mac: **source env/bin/activate**. For Windows execute in **CMD** this command: **.\venv\Scripts\activate**.
- Install project dependencies executing this command in the console for Linux or Mac or in **CMD** for Windows: **pip install -r requirements.txt**.
- Specify the information to connect to the database in the **.env** file. In this case it is used a PostgreSQL database, but can use MySQL perfectly.
- If you have the **authors.json** and **books.json** files, copy in the folder where are the scrips **load_authors.py** and **load_books.py**. Make sure in the directory where is the **manage.py** file to execute this command in the console for Linux or Mac or in **CMD** for Windows: **python manage.py shell** to enter in the interactive console for python once there execute these commands: **from library_api.load_data import load_authors** and then **from library_api.load_data import load_books** to add data to the database.
- After execute this command in the console for Linux or Mac or in **CMD** for Windows: **python manage.py runserver** to run the application. Generally run in this route: **http://127.0.0.1:8000/**. The port could be different if the default one (**8000**) is already in use.
- It is recommended to try **postman**.
- Can access to this endpoints without authenticating:
  - GET **api/authors/** to get the list of authors. The complete route can be for example: **http://127.0.0.1:8000/api/authors/**
  - GET **api/authors/:author_id/** to get the information for a specific author. The complete route can be for example: **http://127.0.0.1:8000/api/authors/1/**
  - GET **api/books/** to get the list of books. The complete route can be **http://127.0.0.1:8000/api/books/**
  - GET **api/authors/:book_id/** to get the information for a specific book. The complete route can be for example: **http://127.0.0.1:8000/api/books/1/**
  - POST **api/register/** to register a user in the api. The complete route can be for example: **http://127.0.0.1:8000/api/register/**
    - Fields required to register a user: **email** and **password**
  - POST **api/login/** to login a user in the api. The complete route can be for example: **http://127.0.0.1:8000/api/login/**
    - Fields required to login in the api: **email** and **password** previously registered.
    - This proccess return a **JSON object** like this:
      
      {
        "refresh_token": "",
        "access_token": ""
      }
    - Of course it will be with data, but it will only be necessary the **access_token** which will be used to add, modify and delete authors, books and favorite books as the case may be.
- The **access_token** obtained when logging in will be used. If you are testing in **postman**, go to the **Authorization** tab and in the option **Auth Type** select **Bearer Token** to put the **access_token** in the **Token** field and in the **Headers** tab add in field **Key**: **Content-Type** and in the field **Value**: **application/json**. To access these endpoints:
  - POST **api/authors/** to add a new author in the api. The complete route can be for example: **http://127.0.0.1:8000/api/authors/**
    - Fields required to add a new book in the api: **name**.
    - More information can be added in additional fields using a **JSON object** like this:

      {
          "name": "J.K. Rowling",
          "gender": "Female",
          "about": "Writer of Harry Potter",
          "average_rating": 5,
          "ratings_count": 100,
          "text_reviews_count": 20,
          "works_count": 7,
          "fans_count": 1000
      }
  - PUT **api/authors/:author_id/** to update an author in the api. The complete route can be for example: **http://127.0.0.1:8000/api/authors/1/**
    - Fields required to update an author in the api: **name**.
    - More information can be added in additional fields using a **JSON object** like the one used to add.

  - POST **api/books/** to add a new book in the api. The complete route can be for example: **http://127.0.0.1:8000/api/books/**
    - Fields required to add a new book in the api: **title**, **authors** and **language**.
    - More information can be added in additional fields using a **JSON object** like this:

      {
          "title": "Book of Python",
          "work_id": ,
          "isbn": "",
          "isbn13": "",
          "asin": "",
          "language": "en",
          "average_rating": 0,
          "ratings_count": 0,
          "text_reviews_count": 0,
          "publication_date": "",
          "original_publication_date": "",
          "format": "",
          "edition_information": "",
          "image_url": "",
          "publisher": "",
          "num_pages": 0,
          "series_name": "",
          "series_position": "",
          "description": "r",
          "authors": [99999]
      }
  - PUT **api/books/:book_id/** to update a book in the api. The complete route can be for example: **http://127.0.0.1:8000/api/books/1/**
    - Fields required to update a book in the api: **title**, **authors** and **language**.
    - More information can be added in additional fields using a **JSON object** like the one used to add.
  - POST **api/favorites/** to add a favorite book for a user. The complete route can be for example: **http://127.0.0.1:8000/api/favorites/**
    - Field required to add a favorite book for a user: **book_id**.
    - More information can be added in additional fields using a **JSON object** like this:
   
      {
          "book_id": "1"
      }
  - GET **api/favorites/** to get a favorite books list of a user. The complete route can be for example: **http://127.0.0.1:8000/api/favorites/**
  - GET **api/recommended-books/** to get a recommended books for a user. The complete route can be for example: **http://127.0.0.1:8000/api/recommended-books/**
  - DELETE **api/authors/:author_id/** to delete an author in the api. The complete route can be for example: **http://127.0.0.1:8000/api/authors/1/**
  - DELETE **api/books/:book_id/** to delete a book in the api. The complete route can be for example: **http://127.0.0.1:8000/api/books/1/**
