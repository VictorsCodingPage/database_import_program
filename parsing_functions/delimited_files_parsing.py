from data_transfer_objects.data_transfer_objects import *
from data_reading.scan_file_to_list import *
import json

def list_zip(listA, listB):
    if len(listA) == len(listB):
        return [ (listA[x], listB[x]) for x in range(len(listA)) ]
    else:
        print("Headers contains {} items\nLine contains {} items".format(len(listA), len(listB)))
        print(listB[-2:])

def list_to_dict(arg):
    ret_dict = {}
    for k, v in arg:
        ret_dict[k] = v
    return ret_dict

def product_variant_init(headers, prod_dict, product_category, dict_level_1, dict_level_2):
    last_updated = prod_dict.get("LASTUPDATED")
    if last_updated == None:
        last_updated = datetime.datetime.now()
    new_product = ProductDTO(
        VariantDTO(description=prod_dict.get("DESCRIPTION"),
                   price=prod_dict.get("PRICE"),
                   currency=prod_dict.get("CURRENCY"),
                   url=prod_dict.get("BUYURL"),
                   sku=prod_dict.get("SKU"),
                   cover_image=prod_dict.get("IMAGEURL"),
                   specification=prod_dict.get("DESCRIPTION"),
                   small_version_url=prod_dict.get(""),
                   normal_version_url=prod_dict.get("IMAGEURL"),
                   large_version_url=prod_dict.get(""),
                   updated_at=last_updated,
                   variant_file = json.dumps([{"small_version_url": "{}".format(prod_dict.get(""))},
                                    {"normal_version_url": "{}".format(prod_dict.get("IMAGEURL"))},
                                    {"large_version_url": "{}".format(prod_dict.get(""))}])),
        name=prod_dict.get("NAME").title(),
        brand=prod_dict.get("MANUFACTURER").title(),
        description=prod_dict.get("DESCRIPTION"),
        product_code=prod_dict.get("UPC"),
        category=product_category.title(),
        category_level_2=dict_level_2.get(product_category),
        category_id=dict_level_1.get(dict_level_2.get(product_category)),
        shipping_info=prod_dict.get(""),
        price_range=prod_dict.get(""),
        post_id=prod_dict.get(""),
        vendor=prod_dict.get("PROGRAMNAME").title(),
        vendor_url=prod_dict.get("BUYURL"),
        small_version_url=prod_dict.get(""),
        normal_version_url=prod_dict.get("IMAGEURL"),
        large_version_url=prod_dict.get(""),
        cover_image=prod_dict.get("IMAGEURL"),
        product_file=json.dumps([{"small_version_url": "{}".format(prod_dict.get(""))},
                        {"normal_version_url": "{}".format(prod_dict.get("IMAGEURL"))},
                        {"large_version_url": "{}".format(prod_dict.get(""))}]),
        updated_at=last_updated)

    return new_product

def delimited_files_parsing_general(file_to_parse, delimiter, mapping_list, dict_level_1, dict_level_2):
    headers = mapping_list
    none_category_counter = 0

    # READ MISSING CATEGORIES ALREADY DOCUMENTED
    failed_categories_file = "categories_not_recognized.txt"

    # LISTS FOR DOCUMENTING MISSING CATEGORIES
    failed_cats_list = scan_file_to_list(failed_categories_file, delimiter)
    failed_cats_print_list = []

    list_of_products = []
    with open(file_to_parse) as parse_file:
        content = parse_file.readlines()
        for line in content[1:]:
            values = line.split(delimiter)
            zipped_list = list_zip(headers, values)
            product_dict = list_to_dict(zipped_list)

            # PRODUCT CATEGORY
            product_category = product_dict.get("ADVERTISERCATEGORY")

            if dict_level_1.get(dict_level_2.get(product_category)) != None:
                list_of_products.append(product_variant_init(headers, product_dict, product_category, dict_level_1, dict_level_2))
            elif product_category != None and product_category != "":
                if product_category not in failed_cats_print_list:
                    failed_cats_print_list.append(product_category)
                if product_category not in failed_cats_list:
                    failed_cats_list.append(product_category)
                    failed_cats = open(failed_categories_file, "a")
                    failed_cats.write(product_category+delimiter)
                    failed_cats.close()
            else:
                none_category_counter += 1

    # PRINT AND SAVE THE NUMBER OF PRODUCTS WITH CATEGORIES NOT RECOGNIZED
    if none_category_counter >= 1:
        print "Category for {} products DOES NOT EXIST".format(none_category_counter)
        files_with_missing_categories = open("files_with_missing_categories.txt", "a")
        files_with_missing_categories.write("{} {}\t".format(file_to_parse, none_category_counter))
        files_with_missing_categories.close()
    else:
        print "Every product has categories!"

    # PRINT THE CATEGORIES NOT MAPPED
    if len(failed_cats_print_list) >= 1:
        print "Categories "
        for category in failed_cats_print_list:
            print "\t{}".format(category)
        print "NOT RECOGNIZEABLE!"

    return list_of_products
