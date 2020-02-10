import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from libraryapp.models import Book, Library
from ..connection import Connection

def get_book(book_id):
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
        FROM libraryapp_book b
        WHERE b.id = ?
        """, (book_id,))

        # book_to_view = []
        book_to_view = db_cursor.fetchone()

        # for row in data:
        #     book = Book()
        #     book.id = book_id
        #     book.title = row['title']
        #     book.isbn_number = row['isbn_number']
        #     book.author = row['author']
        #     book.year = row['year']
        #     book.librarian = row['librarian_id']
        #     book.location = row['location_id']

        #     book_to_view.append(book)

        return book_to_view

@login_required
def book_details(request, book_id):
    if request.method == 'GET':
        book = get_book(book_id)

        template = 'books/detail.html'
        context = {
            'book': book
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST
        #check if this is an update PUT

        if("actual_method" in form_data and form_data["actual_method"] == "PUT"):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE libraryapp_book
                SET title = ?, author = ?, isbn_number = ?, year = ?, location_id = ?
                WHERE id= ?
                """,
                (form_data['title'], form_data['author'], form_data['isbn_number'], form_data['year'], form_data['location'], book_id,))

            return redirect(reverse('libraryapp:books'))

    # Check if this POST is for deleting a book
    #
    # Note: You can use parenthesis to break up complex
    # 'if' statements for higher readability

        if ("actual_method" in form_data and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                db_cursor.execute("""
                DELETE FROM libraryapp_book
                WHERE id = ?
                """, (book_id,))

            return redirect(reverse('libraryapp:books'))

    

@login_required
def book_edit_form(request, book_id):
    if request.method == 'GET':
        book = get_book(book_id)
        libraries = get_libraries()
        template = 'books/form.html'
        context = {'book': book, 'all_libraries': libraries}

        return render(request, template, context)
