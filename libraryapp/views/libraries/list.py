import sqlite3
from ..connection import Connection
from libraryapp.models import Library, Book
from django.shortcuts import render, redirect
from django.urls import reverse

def library_list(request):
    if request.method == "GET":
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = create_library

            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT li.id,
            li.title, 
            li.address,
            b.id book_id,
            b.title book_title,
            b.author,
            b.year,
            b.isbn_number
            FROM libraryapp_library li, libraryapp_book b
            ON li.id = b.location_id
            """)
            all_libraries = []
            library_groups = {}
            libraries = db_cursor.fetchall()

            for (library, book) in libraries:
                if library.id not in library_groups:
                    library_groups[library.id] = library
                    library_groups[library.id].books.append(book)
                else:
                    library_groups[library.id].books.append(book)

                all_libraries.append(library)

            template = 'libraries/list.html'

            context = {'all_libraries': all_libraries}

            return render(request, template, context)

    elif request.method == "POST":
        form_data = request.POST
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()
            db_cursor.execute("""
            INSERT INTO libraryapp_library (title, address)
            VALUES (?,?)""",
            (form_data['title'], form_data['address'])
            )
        return redirect(reverse('libraryapp:libraries'))

def create_library(cursor, row):
    _row = sqlite3.Row(cursor, row)

    library = Library()
    library.id = _row["id"]
    library.title = _row["title"]
    library.address = _row["address"]

    library.books = []

    book = Book()
    book.id = _row["id"]
    book.title = _row["book_title"]
    book.author = _row["author"]
    book.isbn_number = _row["isbn_number"]
    book.year = _row["year"]

    return (library, book, )


