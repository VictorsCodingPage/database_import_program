import datetime
import psycopg2

def get_store_name_list(cursor):
    temp_name_list = []
    SQL = "SELECT name FROM stores"
    cursor.execute(SQL)
    store_names = cursor.fetchall()
    for name in store_names:
        temp_name_list.append(name[0])
    return temp_name_list



def get_store_id_from_stores(vendor_name, cursor):
    SQL = "SELECT id FROM stores WHERE name = '{}'".format(vendor_name.replace("\'", "''"))
    cursor.execute(SQL)
    store_id_as_list = cursor.fetchone()
    if store_id_as_list == None:
        store_id = -1
    else:
        store_id = store_id_as_list[0]
    return store_id



def get_store_id_list(cursor):
    temp_id_list = []
    SQL = "SELECT id FROM stores".format()
    cursor.execute(SQL)
    store_id = cursor.fetchall()
    for ID in store_id:
        temp_id_list.append(ID[0])
    return temp_id_list



def get_product_id_from_products(product_code, cursor):
    SQL = "SELECT id FROM products WHERE product_code = %s"
    cursor.execute(SQL, (product_code,))
    fetch_value = cursor.fetchone()
    if fetch_value != None:
        product_id = fetch_value[0]
    else:
        product_id = None
    return product_id



def get_variant_id_from_variants(product_id, cursor):
    SQL = "SELECT id FROM variants WHERE product_id = %s"
    cursor.execute(SQL, (product_id,))
    fetch_value = cursor.fetchone()
    variant_id = fetch_value[0]
    return variant_id
