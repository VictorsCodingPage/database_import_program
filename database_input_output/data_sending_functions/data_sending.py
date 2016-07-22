import datetime
import psycopg2
import imp
import json
from data_transfer_objects.data_transfer_objects import ProductDTO, VariantDTO

mogrify = imp.load_source('data_sending_functions', './database_input_output/data_sending_functions/mogrify_functions.py')

def insert_store(cursor, vendor_name, store_name_list, store_bool_list):
    print "{} does not exist in the stores table".format(vendor_name)
    store_bool_list.append(False)
    store_name_list.append(vendor_name)

    store_bool_list[store_name_list.index(vendor_name)] = True
    timestamp = datetime.datetime.now()
    SQL = "INSERT INTO stores VALUES (%s, %s, %s)"
    cursor.execute(SQL, (vendor_name, timestamp, timestamp))

    return (vendor_name in store_name_list) and store_bool_list[store_name_list.index(vendor_name)]

def export_data_to_database(product_list, store_id, cursor):
    product_count = len(product_list)

    product_data_tuple = mogrify.mogrify_product_data(product_list, cursor)
    cursor.execute(product_data_tuple[0] + product_data_tuple[1])

    get_product_ids = "SELECT id from products order by id desc limit {};".format(product_count)
    print "Sending products"
    cursor.execute(get_product_ids)
    product_id_list = cursor.fetchall()

    cat_count = 0
    prod_cat_list = []
    var_store_list = []

    variant_data_tuple = mogrify.mogrify_variant_data(product_list, product_id_list, cursor)
    cursor.execute(variant_data_tuple[0] + variant_data_tuple[1])

    get_variant_id = "SELECT id from variants order by id desc limit {};".format(len(product_list))
    print "Sending variants"
    cursor.execute(get_variant_id)
    var_IDs = cursor.fetchall()

    for product in product_list:
        temp_variant = product.variant
        product_id = product_id_list[(product_count - 1) - cat_count][0]

        # ProductCategory
        prodCatDATA = (product_id, product.category_id, product.created_at, product.updated_at)
        prod_cat_list.append(prodCatDATA)

        # VariantStore
        varStoreDATA = (temp_variant.price, temp_variant.currency, temp_variant.url,
                        var_IDs[(product_count - 1) - cat_count][0], temp_variant.created_at,
                        temp_variant.updated_at, temp_variant.sku, store_id, 1)
        var_store_list.append(varStoreDATA)

        cat_count += 1

    args_str2 = ','.join(cursor.mogrify("(%s, %s, %s, %s)", x) for x in prod_cat_list)
    print "Sending product category"
    cursor.execute(
        "INSERT INTO product_categories (product_id, category_id, created_at, updated_at) VALUES" + args_str2)

    args_str8 = ','.join(cursor.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s)", x) for x in var_store_list)
    print "Sending variant store"
    cursor.execute(
        "INSERT INTO variant_stores (price, currency, url, variant_id, created_at, updated_at, sku, store_id,"
        "quantity) VALUES" + args_str8)

    print "{} products sent to server!".format(len(product_list))
