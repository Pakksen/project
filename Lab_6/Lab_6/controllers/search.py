from app import app
from flask import render_template, request, session, redirect, url_for
from utils import get_db_connection
from models.search_model import get_equipment, borrow_equipment, get_color, get_type_of_equipment, get_company

@app.route('/search', methods=["GET"])
def search():
    conn = get_db_connection()

    if request.values.get('borrow_equipment'):
        equipment_id = int(request.values.get('borrow_equipment'))
        borrow_equipment(conn, equipment_id, session['photographer_id'])
        return redirect(url_for("index"))
    
    
    
    if request.values.get('search') and len(request.values.to_dict()) > 1:
    
        filter_dict = dict(filter(lambda item: item[0] not in ('search'), dict(request.values).items()))
        
        chosen_color = {}
        chosen_type_of_equipment = {}
        chosen_company = {}
        
        df_color = get_color(conn)
        df_type_of_equipment = get_type_of_equipment(conn)
        df_company = get_company(conn)

        for i in range(len(df_color)):
            if df_color.loc[i, 'color_name'] in filter_dict:
                chosen_color[df_color.loc[i, 'color_name']] = df_color.loc[i, 'color_id']

        for i in range(len(df_type_of_equipment)):
            if df_type_of_equipment.loc[i, 'type_of_equipment_name'] in filter_dict:
                chosen_type_of_equipment[df_type_of_equipment.loc[i, 'type_of_equipment_name']] = df_type_of_equipment.loc[i, 'type_of_equipment_id']

        for i in range(len(df_company)):
            if df_company.loc[i, 'company_name'] in filter_dict:
                chosen_company[df_company.loc[i, 'company_name']] = df_company.loc[i, 'company_id']

        df_equipment = get_equipment(conn, chosen_color, chosen_type_of_equipment, chosen_company)

        html = render_template(
            'search.html',
            equipment = df_equipment,
            color = df_color,
            type_of_equipment = df_type_of_equipment,
            company = df_company,
            chosen_color = chosen_color,
            chosen_type_of_equipment = chosen_type_of_equipment,
            chosen_company = chosen_company,
            len = len
        )
        

    else:
        df_equipment = get_equipment(conn)
        df_color = get_color(conn)
        df_type_of_equipment = get_type_of_equipment(conn)
        df_company = get_company(conn)

        html = render_template(
                'search.html',
                equipment = df_equipment,
                color = df_color,
                type_of_equipment = df_type_of_equipment,
                company = df_company,
                len = len
        )
        
    return html