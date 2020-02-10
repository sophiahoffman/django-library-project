import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from libraryapp.models import Book, Library, Librarian
# from libraryapp.models import model_factory
from ..connection import Connection
from .details import get_book

def get_libraries():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row

        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT id, title, address
        FROM libraryapp_library
        """)

        all_libraries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            library = Library()
            library.id=row['id']
            library.title = row['title']
            library.address = row['address']

            all_libraries.append(library)
        
        return all_libraries

# def get_librarians():
#     with sqlite3.connect(Connection.db_path) as conn:
#         conn.row_factory = sqlite3.Row

#         db_cursor = conn.cursor()
#         db_cursor.execute("""
#         SELECT u.id, u.first_name, u.last_name
#         FROM libraryapp_librarian ll, auth_user u
#         ON u.id = ll.id
#         """)

#         all_librarians = []
#         dataset = db_cursor.fetchall()

#         for row in dataset:
#             librarian = Librarian()
#             librarian.first_name = row['first_name']
#             librarian.last_name = row['last_name']

#             all_librarians.append(librarian)
        
#         return all_librarians


@login_required    
def book_form(request):
    if request.method == 'GET':
        libraries = get_libraries()
        # librarians = get_librarians()
        template = 'books/form.html'
        context = {'all_libraries': libraries}

    return render(request, template, context)

@login_required
def book_edit_form(request, book_id):
    if request.method == 'GET':
        book = get_book(book_id)
        libraries = get_libraries()

        template = 'books/form.html'
        context={'book': book, 'all_libraries': libraries}

        return render(request, template, context)