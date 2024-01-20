import pandas

def get_equipment(conn, chosen_color = {}, chosen_type_of_equipment = {}, chosen_company = {}):
    if len(chosen_color) == 0 and len(chosen_type_of_equipment) == 0 and len(chosen_company) == 0:
        return pandas.read_sql('''
                            
            WITH get_type_of_equipments( equipment_id, type_of_equipments_name)
            AS(
                SELECT equipment_id, GROUP_CONCAT(type_of_equipment_name, ', ')
                FROM type_of_equipment JOIN equipment_type_of_equipment USING(type_of_equipment_id)
                GROUP BY equipment_id
            )

            select
                title as Название, 
                type_of_equipments_name as 'Тип_оборудования', 
                color_name as Цвет,
                company_name as Производитель,
                Year_of_delivery as Год_производства,
                available_numbers as Количество,
                equipment_id
            from equipment join color using(color_id) 
            join company using(company_id) 
            join get_type_of_equipments using(equipment_id)

        ''', conn)
    else:
        cur = conn.cursor()

        df_color = pandas.DataFrame()
        for item in chosen_color:
            df_tmp = pandas.DataFrame(cur.execute('''
                
                select equipment_id from equipment
                where color_id = :item

            ''', {"item": int(chosen_color[item])}))

            df_color = pandas.concat([df_color, df_tmp])
        df_color.reset_index(inplace = True, drop= True)
        df_color = [df_color.loc[i, 0] for i in range(len(df_color))] if len(df_color) != 0 else []
            

        df_type_of_equipment = pandas.DataFrame()
        for item in chosen_type_of_equipment:
            df_tmp = pandas.DataFrame(cur.execute('''
                
                select equipment_id from equipment_type_of_equipment
                where type_of_equipment_id = :item

            ''', {"item": int(chosen_type_of_equipment[item])}))
                
            df_type_of_equipment = pandas.concat([df_type_of_equipment, df_tmp])
        df_type_of_equipment.reset_index(inplace = True, drop = True)
        df_type_of_equipment = [df_type_of_equipment.loc[i, 0] for i in range(len(df_type_of_equipment))] if len(df_type_of_equipment) != 0 else []


        df_company = pandas.DataFrame()
        for item in chosen_company:
            df_tmp = pandas.DataFrame(cur.execute('''
                
                select equipment_id from equipment
                where company_id = :item

            ''', {"item": int(chosen_company[item])}))
                
            df_company = pandas.concat([df_company, df_tmp])
        df_company.reset_index(inplace = True, drop = True)
        if len(df_color) != 0:
            df_company = [df_company.loc[i, 0] for i in range(len(df_company))] if len(df_company) != 0 else []


        index = df_color if len(df_color) != 0 else []
        index = df_type_of_equipment if len(df_type_of_equipment) != 0 else index
        index = df_company if len(df_company) != 0 else index
        index = list(set(index) & set(df_color)) if len(df_color) != 0 else index
        index = list(set(index) & set(df_type_of_equipment)) if len(df_type_of_equipment) != 0 else index
        index = list(set(index) & set(df_company)) if len(df_company) != 0 else index

        df = pandas.DataFrame()
        for item in index:

            df_tmp = pandas.read_sql('''
                            
                WITH get_type_of_equipments( equipment_id, type_of_equipments_name)
                AS(
                    SELECT equipment_id, GROUP_CONCAT(type_of_equipment_name, ', ')
                    FROM type_of_equipment JOIN equipment_type_of_equipment USING(type_of_equipment_id)
                    GROUP BY equipment_id
                )

                select
                    title as Название, 
                    type_of_equipments_name as 'Тип_оборудования', 
                    color_name as Цвет,
                    company_name as Производитель,
                    Year_of_delivery as Год_производства,
                    available_numbers as Количество,
                    equipment_id
                from equipment join color using(color_id) 
                join company using(company_id) 
                join get_type_of_equipments using(equipment_id)
                where equipment_id = :item

            ''', conn, params = {"item": int(item)})  

            df = pandas.concat([df, df_tmp])

        df.reset_index(inplace = True, drop= True)
        return df
    
def get_color(conn):

    return pandas.read_sql('''
                           
        select distinct color.*, count() over(partition by equipment.color_id) as count from color join equipment using(color_id)

    ''', conn)

def get_type_of_equipment(conn):
    return pandas.read_sql('''
                           
        select distinct type_of_equipment.*, count() over(partition by equipment_type_of_equipment.type_of_equipment_id)
        as count from type_of_equipment join equipment_type_of_equipment using(type_of_equipment_id)

    ''', conn)

def get_company(conn):
    return pandas.read_sql('''
                           
        select distinct company.*, count() over(partition by company_id) 
        as count from company join equipment using(company_id)

    ''', conn)

def borrow_equipment(conn, equipment_id, photographer_id):
    cur = conn.cursor()

    cur.execute('''
        
        insert into equipment_photographer (equipment_photographer_id, equipment_id, photographer_id, borrow_date, return_date) values (null, :curr_equipment_id, :curr_photographer_id, date('now', 'localtime'), null)

    ''', {"curr_equipment_id": equipment_id, "curr_photographer_id": photographer_id})

    cur.execute('''
        
        update equipment
        set available_numbers = available_numbers - 1
        where equipment_id = :curr_equipment_id

    ''', {"curr_equipment_id": equipment_id})

    conn.commit()

    cur.close()

    return True