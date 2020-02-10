import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from libraryapp.models import Book
from django.contrib.auth.decorators import login_required
from ..connection import Connection

@login_required
def book_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                b.id,
                b.title,
                b.isbn_number,
                b.author,
                b.year,
                b.librarian_id,
                b.location_id
            from libraryapp_book b
            """)

            all_books = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                book = Book()
                book.id = row['id']
                book.title = row['title']
                book.isbn_number = row['isbn_number']
                book.author = row['author']
                book.year = row['year']
                book.librarian_id = row['librarian_id']
                book.location_id = row['location_id']
                
                all_books.append(book)

            template = 'books/list.html'

            context = {'all_books': all_books}

            return render(request, template, context)

        
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO libraryapp_book (title, author, isbn_number, year, location_id, librarian_id)
            VALUES (?,?,?,?,?,?)""",
            (form_data['title'], form_data['author'], form_data['isbn_number'], form_data['year'], form_data["location"], request.user.librarian.id))

        return redirect(reverse('libraryapp:books'))