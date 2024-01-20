import pandas

def get_photographer(conn):
    return pandas.read_sql('''

        SELECT * FROM photographer
    
    ''', conn)

def get_equipment_photographer(conn, photographer_id):
    return pandas.read_sql('''

        WITH get_type_of_equipments( equipment_id, type_of_equipments_name)
        AS(
            SELECT equipment_id, GROUP_CONCAT(type_of_equipment_name)
            FROM type_of_equipment JOIN equipment_type_of_equipment USING(type_of_equipment_id)
            GROUP BY equipment_id
        )
        SELECT title AS Название, type_of_equipments_name AS Тип_оборудования,
            borrow_date AS Дата_выдачи, return_date AS Дата_возврата,
            equipment_photographer_id
        FROM
            photographer
            JOIN equipment_photographer USING(photographer_id)
            JOIN equipment USING(equipment_id)
            JOIN get_type_of_equipments USING(equipment_id)
        WHERE photographer.photographer_id = :id
        ORDER BY 3

    
    ''', conn, params={"id": photographer_id})

def get_new_photographer(conn, new_photographer):
    cur = conn.cursor()
    cur.execute('''

        insert into photographer (photographer_id, photographer_name) values (null, :new_photographer)

    ''', {"new_photographer": new_photographer})
    conn.commit()
    cur.close()
    
    return cur.lastrowid

def return_equipment(conn, equipment_photographer_id):
    cur = conn.cursor()
    
    cur.execute('''
                
        update equipment as A
        set available_numbers = A.available_numbers + 1
        from equipment as B join equipment_photographer using (equipment_id)   
        where equipment_photographer_id = :curr_equipment_photographer_id
        and A.equipment_id = B.equipment_id;
                
        
                                     
    ''', {"curr_equipment_photographer_id": equipment_photographer_id})

    cur.execute('''
                
        update equipment_photographer
        set return_date = date('now', 'localtime')
        where equipment_photographer_id = :curr_equipment_photographer_id
                                     
    ''', {"curr_equipment_photographer_id": equipment_photographer_id})

    conn.commit()

    cur.close()
    
    return