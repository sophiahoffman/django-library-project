import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from libraryapp.models import Library

def get_library(library_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT l.id, l.title, l.address
        FROM libraryapp_library l
        WHERE l.id = ?
        """,
        (library_id,))

        library_to_view = db_cursor.fetchone()

        return library_to_view

@login_required
def library_details(request, library_id):
    if request.method == 'GET':
        library = get_library(library_id)

        template = 'libraries/detail.html'
        context = {'library': library}

        return render(request, template, context)
