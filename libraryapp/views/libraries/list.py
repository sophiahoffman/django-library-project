import sqlite3
from ..connection import Connection
from libraryapp.models import Library
from django.shortcuts import render

def library_list(request):
    if request.method == "GET":
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row

            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT title, address
            FROM libraryapp_library
            """)

            all_libraries = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                library = Library()
                library.title = row['title']
                library.address = row['address']

                all_libraries.append(library)

            template = 'libraries/list.html'

            context = {'all_libraries': all_libraries}

            return render(request, template, context)

