import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from libraryapp.models import Librarian



def get_librarian(librarian_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT l.id, l.user_id, u.first_name, u.last_name, loc.title, loc.address
        FROM libraryapp_librarian l, auth_user u
        ON l.user_id=u.id
        LEFT JOIN libraryapp_library loc
        ON l.location_id = loc.id
        WHERE l.id = ?
        """, (librarian_id,))

        librarian_to_view = db_cursor.fetchone()

        return librarian_to_view

@login_required
def librarian_details(request, librarian_id):
    if request.method == 'GET':
        librarian = get_librarian(librarian_id)

        template = 'librarians/detail.html'
        context = {'librarian':librarian}

        return render(request, template, context)

