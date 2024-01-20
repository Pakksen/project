from app import app
from flask import render_template, request, session, redirect, url_for
from utils import get_db_connection
from models.index_model import get_new_photographer

@app.route('/new_photographer', methods=["GET"])
def new_photographer():
    conn = get_db_connection()

    if request.values.get("cancel"):
        return redirect(url_for("index"))

    if request.values.get("add") and request.values.get("new_photographer"):
        new_photographer = request.values.get('new_photographer')
        session['photographer_id'] = get_new_photographer(conn, new_photographer)
        return redirect(url_for("index"))

    html = render_template(
        'new_photographer.html'
    )
    return html