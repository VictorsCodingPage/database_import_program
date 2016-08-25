import imp
from data_transfer_objects.data_transfer_objects import ProductDTO, VariantDTO

text_formatting = imp.load_source('text_formatting_functions', './text_formatting_functions/text_formatting_functions.py')

def mogrify_product_data(product_list, cursor):
    prod_data_list = [(product.name, product.brand, product.product_code, product.created_at,
                       product.updated_at, product.description, product.price_range,
                       product.category_hierarchy, product.shipping_info, product.vendor_url, product.product_file) for product in product_list]
    SQL = "INSERT INTO products (name, brand, product_code, created_at, updated_at,"\
        " description, price_range, category_hierarchy, shipping_info, vendor_url, product_files)"\
        " VALUES"
    args_str = ','.join(cursor.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", x) for x in prod_data_list)

    return (SQL, args_str)

def mogrify_variant_data(product_list, product_id_list, cursor):
    cat_count = 0
    product_count = len(product_list)
    variant_data_list = []
    for product in product_list:
        variant_data_list.append((product_id_list[(product_count - 1) - cat_count][0], product.variant.created_at,
                                  product.variant.updated_at, product.variant.description, product.variant.variant_file))
        cat_count += 1
    SQL = "INSERT INTO variants (product_id, created_at, updated_at, description, variant_files) VALUES"
    args_str = ','.join(cursor.mogrify("(%s, %s, %s, %s, %s)", x) for x in variant_data_list)

    return (SQL, args_str)