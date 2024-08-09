from sql_connection import get_connection

def get_all_products(connection):
    cursor = connection.cursor()
    query = "SELECT grocery_store.products.product_id, grocery_store.products.product_name, grocery_store.products.uom_id, "\
        "grocery_store.products.price_per_unit, grocery_store.uom.uom_name FROM grocery_store.products inner join "\
        "grocery_store.uom on grocery_store.products.uom_id = grocery_store.uom.uom_id"
    cursor.execute(query)
    
    response = []

    for (product_id, product_name, uom_id, price_per_unit, uom_name) in cursor:
        response.append(
            {
                'product_id': product_id,
                'product_name': product_name,
                'uom_id': uom_id,
                'uom_name': uom_name,
                'price_per_unit': price_per_unit
            }
        )

    connection.close()
    
    return response

def add_product(connection, product):
    cursor = connection.cursor()
    query = ("INSERT INTO grocery_store.products(product_name, uom_id, price_per_unit) VALUES (%s, %s, %s)")
    data = (product['product_name'], product['uom_id'], product['price_per_unit'])
    
    cursor.execute(query, data)
    connection.commit()
    
    return cursor.lastrowid

def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = ("DELETE FROM grocery_store.products WHERE product_id = %s")
    
    cursor.execute(query, (product_id,))
    connection.commit()
    
    return cursor.lastrowid

if __name__ == '__main__':
    connection = get_connection()
    print(add_product(connection, {
        'product_name': 'cereal', 
        'uom_id': '1', 
        'price_per_unit': '3'
    }))
    