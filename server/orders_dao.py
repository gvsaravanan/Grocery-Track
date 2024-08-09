from datetime import datetime
from sql_connection import get_connection

def add_order(connection, order):
    cursor = connection.cursor()
    order_query = ("INSERT INTO grocery_store.orders(customer_name, total, datetime) VALUES (%s, %s, %s)")
    
    order_data = (order['customer_name'], order['total'], datetime.now())
    cursor.execute(order_query, order_data)
    
    order_id = cursor.lastrowid
    
    order_details_query = ("INSERT INTO grocery_store.order_details(order_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)")
    
    order_details_data = []
    for order_detail in order['order_details']:
        order_details_data.append([
            order_id, 
            int(order_detail['product_id']), 
            float(order_detail['quantity']), 
            float(order_detail['total_price'])
        ])
        
    cursor.executemany(order_details_query, order_details_data)
    connection.commit()
    
    return order_id

def get_order_details(connection, order_id):
    cursor = connection.cursor()

    query = ("SELECT grocery_store.order_details.order_id, grocery_store.order_details.quantity, grocery_store.order_details.total_price, "\
        "grocery_store.products.product_name, grocery_store.products.price_per_unit FROM grocery_store.order_details LEFT JOIN grocery_store.products ON "\
        "grocery_store.order_details.product_id = grocery_store.products.product_id WHERE grocery_store.order_details.order_id = %s")
        
    cursor.execute(query, (order_id,))

    response = []

    for (order_id, quantity, total_price, product_name, price_per_unit) in cursor:
        response.append(
            {
                'order_id': order_id,
                'quantity': quantity,
                'total_price': total_price,
                'product_name': product_name,
                'price_per_unit': price_per_unit
            }
        )

    cursor.close()
    
    return response

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM grocery_store.orders")
    cursor.execute(query)
    
    response = []

    for (order_id, customer_name, total, dt) in cursor:
        response.append(
            {
                'order_id': order_id,
                'customer_name': customer_name,
                'total': total,
                'datetime': dt
            }
        )
    
    for order in response:
        order['order_details'] = get_order_details(connection, order['order_id'])
    
    return response

if __name__ == '__main__':
    connection = get_connection()
    print(get_all_orders(connection))