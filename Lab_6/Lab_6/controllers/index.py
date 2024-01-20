from app import app
from flask import render_template, request, session, redirect, url_for
from utils import get_db_connection
from models.index_model import get_photographer, get_equipment_photographer, return_equipment

@app.route('/', methods=["GET"])
def index():
    conn = get_db_connection()

    if request.values.get('photographer'):
        photographer_id = int(request.values.get('photographer'))
        session['photographer_id'] = photographer_id
    

    # elif request.values.get('noselect'):
    #     a = 1

    elif request.values.get('return_equipment'):
        return_equipment(conn, request.values.get('return_equipment'))
        return redirect(url_for('index'))

    elif "photographer_id" not in session:
        session['photographer_id'] = 1
        
    df_photographer = get_photographer(conn)
    df_equipment_photographer = get_equipment_photographer(conn, session['photographer_id'])


    html = render_template(
            'index.html',
            photographer_id = session['photographer_id'],
            combo_box = df_photographer,
            equipment_photographer = df_equipment_photographer,
            len = len
    )
    return html