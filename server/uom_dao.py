def get_uoms(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM grocery_store.uom")
    cursor.execute(query)
    
    response = []

    for (uom_id, uom_name) in cursor:
        response.append(
            {
                'uom_id': uom_id,
                'uom_name': uom_name
            }
        )

    connection.close()
    
    return response

if __name__ == '__main__':
    from sql_connection import get_connection
    
    connection = get_connection()
    print(get_uoms(connection))