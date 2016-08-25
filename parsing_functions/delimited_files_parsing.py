from data_transfer_objects.data_transfer_objects import *
from data_reading.scan_file_to_list import *
from xml_to_dict import *
from HTMLParser import HTMLParser
import imp
import json
import re

text_formatting = imp.load_source('text_formatting_functions', './text_formatting_functions/text_formatting_functions.py')

def list_zip(listA, listB):
    if len(listA) == len(listB):
        return [ (listA[x], listB[x]) for x in range(len(listA)) ]
    else:
        raise ValueError("Headers contains {} items\nLine contains {} items".format(len(listA), len(listB)))

def list_to_dict(arg):
    ret_dict = {}
    for k, v in arg:
        ret_dict[k] = v
    return ret_dict

def product_variant_init(prod_dict, color_dict, product_category, category_delimiter, dict_level_1, dict_level_2, category_id, gender):
    #headers = "PROGRAMNAME	PROGRAMURL	CATALOGNAME	LASTUPDATED	NAME	KEYWORDS	DESCRIPTION	SKU	MANUFACTURER	MANUFACTURERID	UPC	ISBN	CURRENCY"\
	#"SALEPRICE	PRICE	RETAILPRICE	FROMPRICE	BUYURL	IMPRESSIONURL	IMAGEURL	ADVERTISERCATEGORY	THIRDPARTYID	THIRDPARTYCATEGORY"\
	#"AUTHOR	ARTIST	TITLE	PUBLISHER	LABEL	FORMAT	SPECIAL	GIFT	PROMOTIONALTEXT	STARTDATE	ENDDATE	OFFLINE	ONLINE	INSTOCK	CONDITION"\	
	#"WARRANTY	STANDARDSHIPPINGCOST"
    last_updated = prod_dict.get("LASTUPDATED")
    parser = HTMLParser()

    if last_updated == None or last_updated == '':
        last_updated = datetime.datetime.now()

    small_version_url = prod_dict.get("image.small")
    if small_version_url == None:
        small_version_url = ""

    normal_version_url = prod_dict.get("image.medium")
    if small_version_url == None:
        small_version_url = ""

    large_version_url = prod_dict.get("image.large\n")
    if large_version_url == None:
        large_version_url = ""

    raw_price = prod_dict.get("price.retail")
    # raw_sale_price = prod_dict.get("SALEPRICE")
    # Price = raw_price.replace("$", "USD")
    # result = re.match("([A-Z]{0,3})(\d{1,4}\.{0,1}\d{0,2})(\w{0,3})", Price)
    # if result != None:
    #     Price = result.group(2)
    # else:
    #     Price = raw_price
    #
    # if result.group(1) != None:
    #     currency = result.group(1)
    # else:
    #     currency = result.group(3)

    # if currency == None:
    currency = prod_dict.get("currency")

    # if raw_sale_price != None:
    #     price_range = raw_sale_price + "-" + Price
    # else:
    #     price_range = raw_price

    # if price_range[0] == "-":
    #     price_range = price_range.replace("-","")

    color_id = color_dict.get(prod_dict.get("color"))


    price_range = raw_price + "-" + prod_dict.get("price.sale")

    # target_url = prod_dict.get("BUYURL")
    # if target_url[0] == "<":
    #     target_url = parser.feed(target_url)

    new_product = ProductDTO(
        VariantDTO(description=prod_dict.get("description"),
                   price=raw_price,
                   currency=currency,
                   url=prod_dict.get("URL.product_tracker"),
                   sku=prod_dict.get("\xef\xbb\xbfid"),
                   cover_image=prod_dict.get("URL.product_image"),
                   specification=prod_dict.get("description"),
                   small_version_url=small_version_url,
                   normal_version_url=normal_version_url,
                   large_version_url=large_version_url,
                   updated_at=last_updated,
                   variant_file = json.dumps([{"small_version_url": "{}".format(small_version_url),
                                    "normal_version_url": "{}".format(normal_version_url),
                                    "large_version_url": "{}".format(large_version_url)}])),
        name=prod_dict.get("title"),
        brand=prod_dict.get("brand"),
        description=prod_dict.get("description"),
        product_code=prod_dict.get("\xef\xbb\xbfid"),
        color_id=color_id,
        size = prod_dict.get("length"),
        category=product_category,
        sub_category=prod_dict.get("ADVERTISERCATEGORY"),
        category_level_2=prod_dict.get("ADVERTISERCATEGORY"),
        category_id=category_id,
        category_hierarchy=product_category,
        shipping_info="Cost: "+prod_dict.get("shipping.cost"),
        # price_range=price_range,
        post_id=prod_dict.get(""),
        vendor="Vestiaire Collective",
        vendor_url=prod_dict.get("URL.product_tracker"),
        small_version_url=small_version_url,
        normal_version_url=normal_version_url,
        large_version_url=large_version_url,
        cover_image=normal_version_url,
        product_file=json.dumps([{"small_version_url": "{}".format(small_version_url),
                        "normal_version_url": "{}".format(normal_version_url),
                        "large_version_url": "{}".format(large_version_url)}]),
        updated_at=last_updated)

    return new_product

def delimited_files_parsing_general(file_to_parse, delimiter, mapping_list, dict_level_1, dict_level_2, color_dict):
    headers = mapping_list
    none_category_counter = 0
    products_parsed_counter = 0

    # READ MISSING CATEGORIES ALREADY DOCUMENTED
    failed_categories_file = "categories_not_recognized.txt"

    # LISTS FOR DOCUMENTING MISSING CATEGORIES
    failed_cats_list = scan_file_to_list(failed_categories_file, "\t")
    failed_cats_print_list = []

    list_of_products = []
    with open(file_to_parse) as parse_file:
        content = parse_file.readlines()
        for line in content[1:]:
            # new_line = line.replace("YOURUSERID", "1174133")
            new_line = line
            values = new_line.split(delimiter)
            zipped_list = list_zip(headers, values)
            product_dict = list_to_dict(zipped_list)

            category_list = [product_dict.get("gender"), product_dict.get("product_category"), product_dict.get("product_subCategory"), product_dict.get("brand")]
            product_category = category_list[0]+">"+category_list[1]+">"+category_list[2]
            # print product_category, dict_level_1.get(product_category)
            # level_2_cat = dict_level_2.get(product_category)

            # print dict_level_2

            category_id = dict_level_1.get(product_category)
            # category_id = True
            if category_id != None:
                gender = category_list[0]
                # category_id_switched = switch_gender(category_id, gender)

                category_id_switched = (category_id, True)

                if category_id_switched[1] == True:
                    # log_wrong_gender(product_dict.get("SKU"), category_id_switched[0])
                    list_of_products.append(product_variant_init(product_dict, color_dict, product_category, delimiter,  dict_level_1, dict_level_2, category_id_switched[0], gender))
                products_parsed_counter += 1
            elif product_category != None and product_category != "":
                if product_category not in failed_cats_print_list:
                    failed_cats_print_list.append(product_category)
                if product_category not in failed_cats_list:
                    failed_cats_list = update_failed_cats_list(failed_cats_list, product_category, failed_categories_file)
            else:
                none_category_counter += 1

    # PRINT AND SAVE THE NUMBER OF PRODUCTS WITH CATEGORIES NOT RECOGNIZED
    save_and_print_missing_categories(none_category_counter, file_to_parse, failed_cats_print_list)
    print "{} products parsed!".format(products_parsed_counter)


    return list_of_products

def json_parsing(file_to_parse, dict_level_1, dict_level_2, category_to_gender_dict):
    failed_categories_file = "categories_not_recognized.txt"
    failed_cats_list = scan_file_to_list(failed_categories_file, "\t")
    failed_cats_print_list = []
    none_category_counter = 0

    # categories_that_match = set()

    list_of_products = []

    switch_dict_female_to_male = {3: 23, 4: 22, 5: 25, 6: 21, 8: 27, 16: 32, 17: 33, 18: 34, 20: 37, 39: 35, 38: 36}
    switch_dict_male_to_female = {23: 3, 22: 4, 25: 5, 21: 6, 27: 8, 32: 16, 33: 17, 34: 18, 37: 20, 35: 39, 36: 38}

    with open(file_to_parse, "r") as f:
        json_product_list = json.load(f)
        merchant = json_product_list.get("MerchantName")
        print merchant

        for product in json_product_list["Items"]:
            product_category = product.get("Category").encode('ascii', 'ignore')

            category_id = None
            lowest_mapped_cat = None
            category_delimiter = ">"
            split_cats = product_category.split(category_delimiter)
            for cat in split_cats:
                cat_strip = cat.strip()
                if dict_level_1.get(dict_level_2.get(cat_strip)) != None:
                    lowest_mapped_cat = cat_strip
                    category_id = dict_level_1.get(dict_level_2.get(cat_strip))
                    # categories_that_match.add(cat_strip)

            # Reset categories_that_match
            categories_that_match = set()

            category_delimiter = "|"
            if lowest_mapped_cat == None:
                split_cats2 = product_category.split(category_delimiter)
                for cat in split_cats2:
                    cat_strip = cat.strip()
                    if dict_level_1.get(dict_level_2.get(cat_strip)) != None:
                        lowest_mapped_cat = cat_strip
                        category_id = dict_level_1.get(dict_level_2.get(cat_strip))
                        # categories_that_match.add(cat_strip)

            if  dict_level_2.get(lowest_mapped_cat) != None:
                gender = category_to_gender_dict.get(lowest_mapped_cat)
                gender_switched = switch_gender(category_id, gender)
                if gender_switched[1] == True:
                    # log_wrong_gender(json_product_list.get("SKU"), gender_switched[0])

                    parser = HTMLParser()

                    small_version_url = product.get("Image50Url")
                    if small_version_url == None:
                        small_version_url = ""

                    normal_version_url = product.get("ImageUrl")
                    if small_version_url == None:
                        small_version_url = ""

                    large_version_url = product.get("Image400Url")
                    if large_version_url == None:
                        large_version_url = ""

                    target_url = product.get("TargetUrl")
                    if target_url[0] == "<":
                        target_url = parser.feed(target_url)

                    last_updated = datetime.datetime.now()

                    vendor = product.get("MerchantName")

                    new_product = ProductDTO(
                        VariantDTO(description=product.get("Description"),
                                   # price=Price,
                                   # currency=currency,
                                   url=target_url,
                                   sku=product.get("SKU"),
                                   cover_image=normal_version_url,
                                   specification=product.get("Description"),
                                   small_version_url=small_version_url,
                                   normal_version_url=normal_version_url,
                                   large_version_url=large_version_url,
                                   updated_at=last_updated,
                                   variant_file=json.dumps([{"small_version_url": "{}".format(small_version_url)},
                                                            {"normal_version_url": "{}".format(normal_version_url)},
                                                            {"large_version_url": "{}".format(large_version_url)}])),
                        name=product.get("Name"),
                        brand=product.get("Manufacturer"),
                        description=product.get("Description"),
                        product_code=product.get("UPC"),
                        category=product_category,
                        sub_category=product.get("Category"),
                        category_level_2=product.get("Category"),
                        category_id=gender_switched[0],
                        category_hierarchy=text_formatting.hierarchy_formatter(product_category.replace(u'\ufffd', "?"),
                                                                               category_delimiter, ">", gender),
                        shipping_info=product.get(""),
                        # price_range=price_range,
                        post_id=product.get(""),
                        vendor=vendor,
                        vendor_url=target_url,
                        small_version_url=small_version_url,
                        normal_version_url=normal_version_url,
                        large_version_url=large_version_url,
                        cover_image=normal_version_url,
                        product_file=json.dumps([{"small_version_url": "{}".format(small_version_url)},
                                                 {"normal_version_url": "{}".format(normal_version_url)},
                                                 {"large_version_url": "{}".format(large_version_url)}]),
                        updated_at=last_updated)

                    list_of_products.append(new_product)
            elif product_category != None and product_category != "":
                if product_category not in failed_cats_print_list:
                    failed_cats_print_list.append(product_category)
                if product_category not in failed_cats_list:
                    failed_cats_list = update_failed_cats_list(failed_cats_list, product_category,
                                                               failed_categories_file)
            else:
                none_category_counter += 1

    # save_and_print_missing_categories(none_category_counter, file_to_parse, failed_cats_print_list)
    return list_of_products


def xml_parsing(file_to_parse, level_1_cat_dict, dict_level_2, category_to_gender_dict):
    failed_categories_file = "categories_not_recognized.txt"
    failed_cats_list = scan_file_to_list(failed_categories_file, "\t")
    failed_cats_print_list = []
    none_category_counter = 0
    parser = HTMLParser()

    products_parsed_counter = 0
    cats_recognized = []

    list_of_products = []

    with open(file_to_parse, "r") as f:
        f.readline()
        root = ElementTree.XML(f.readline())
        xmldict = XmlDictConfig(root)

        merchant_name = xmldict.get("merchantName")

        for line in f:
            try:
                root = ElementTree.XML(line)
            except:
                if line.find("trailer"):
                    root = None
                    pass
                else:
                    raise Exception(line)
            if root != None:
                xmldict = XmlDictConfig(root)
                product_category = xmldict.get("category").get("primary")
                product_category_secondary = xmldict.get("category").get("secondary")
                category_id = level_1_cat_dict.get(product_category_secondary)

                # if category_id_2 in range(0, 21, 1) or category_id_2 in range(38, 40, 1):
                #     category_id = level_1_cat_dict_female.get(category_id_2)
                # else:
                #     category_id = level_1_cat_dict_male.get(category_id_2)

                if category_id != None:
                    products_parsed_counter += 1
                    # if category_to_gender_dict != None:
                    #     gender = category_to_gender_dict.get(product_category)
                    #     gender_switched = switch_gender(category_id, gender)
                    # else:
                    #     gender_switched = (category_id, True)

                    gender_switched = (category_id, True)

                    if category_id == 18 or category_id == 38:
                        gender = 'Women'
                    else:
                        gender = 'Man'

                    if gender_switched[1] == True:
                        # log_wrong_gender(xmldict.get("SKU"), merchant_name)
                        if xmldict.get("category") not in cats_recognized:
                            cats_recognized.append(xmldict.get("category"))

                        price_range = xmldict.get("price").get("retail") + " - " + xmldict.get("price").get("sale")

                        # REPEATED ASSIGNED VALUES
                        normal_url = xmldict.get("URL").get("productImage")
                        update_time = datetime.datetime.now()
                        currency = xmldict.get("price").get("currency")
                        tracking_url = xmldict.get("URL").get("product")

                        # EXCEPTIONS
                        if price_range[0] == "-":
                            price_range.replace("-", "")

                        shipping_info = None
                        shipping_amount = xmldict.get("shipping").get("amount")
                        shipping_availability = xmldict.get("shipping").get("availability")
                        if shipping_amount != None and shipping_availability != None:
                            shipping_info = "Cost: " + shipping_amount + " " + currency + " availability: " + shipping_availability

                        # NORMAL CASES ASSIGNMENTS
                        new_product = ProductDTO(
                            VariantDTO(description=xmldict.get("description").get("long"),
                                        price=xmldict.get("price").get("retail"),
                                        currency=currency,
                                        url=tracking_url,
                                        sku=xmldict.get("sku_number"),
                                        cover_image=xmldict.get("URL").get("productImage"),
                                        specification=xmldict.get(""),
                                        small_version_url=xmldict.get(""),
                                        normal_version_url=normal_url,
                                        large_version_url=xmldict.get(""),
                                        updated_at=update_time,
                                        variant_file=json.dumps([{"small_version_url": "{}".format(None),
                                                                "normal_version_url": "{}".format(normal_url),
                                                                "large_version_url": "{}".format(None)}])),
                            name=xmldict.get("name"),
                            brand=xmldict.get("manufacturer_name"),
                            description=xmldict.get("description").get("long"),
                            product_code=xmldict.get("product_id"),
                            category=product_category,
                            category_secondary=product_category_secondary,
                            category_id=gender_switched[0],
                            shipping_info=shipping_info,
                            category_hierarchy=text_formatting.hierarchy_formatter_xml(product_category, product_category_secondary, gender),
                            post_id=xmldict.get(""),
                            vendor=merchant_name,
                            vendor_url=tracking_url,
                            small_version_url=xmldict.get(""),
                            normal_version_url=normal_url,
                            large_version_url=xmldict.get(""),
                            cover_image=normal_url,
                            product_file=json.dumps([{"small_version_url": "{}".format(None),
                                                     "normal_version_url": "{}".format(normal_url),
                                                     "large_version_url": "{}".format(None)}]),
                            updated_at=update_time)

                        list_of_products.append(new_product)

                elif product_category != None and product_category != "":
                    cat = str(xmldict.get("category"))
                    if cat not in failed_cats_print_list:
                        failed_cats_print_list.append(cat)
                    if cat not in failed_cats_list:
                        failed_cats_list = update_failed_cats_list(failed_cats_list, cat,
                                                                   failed_categories_file)
                else:
                    none_category_counter += 1

    recognized_cats_file = open("categories_recognized.txt", "a")
    for cat in cats_recognized:
        recognized_cats_file.write(str(cat)+"\n")
    recognized_cats_file.close()
    save_and_print_missing_categories(none_category_counter, file_to_parse, failed_cats_print_list)
    print "{} products parsed!".format(products_parsed_counter)
    return list_of_products


def update_failed_cats_list(failed_cats_list, product_category, failed_categories_file):
    failed_cats_list.append(product_category)
    failed_cats = open(failed_categories_file, "a")
    failed_cats.write(product_category + "\n")
    failed_cats.close()
    return failed_cats_list

def save_and_print_missing_categories(none_category_counter, file_to_parse, failed_cats_print_list):
    # PRINT AND SAVE THE NUMBER OF PRODUCTS WITH CATEGORIES NOT RECOGNIZED
    if none_category_counter >= 1:
        print "Category for {} products DOES NOT EXIST".format(none_category_counter)
        files_with_missing_categories = open("files_with_missing_categories.txt", "a")
        files_with_missing_categories.write("{} {}\n".format(file_to_parse, none_category_counter))
        files_with_missing_categories.close()
    else:
        print "Every product has categories!"

    # PRINT THE CATEGORIES NOT MAPPED
    # if len(failed_cats_print_list) >= 1:
    #     print "Categories "
    #     for category in failed_cats_print_list:
    #         print "\t{}".format(category)
    #     print "NOT RECOGNIZEABLE!"

def find_delimiters(string):
    if string.find(">"):
        delimiter = " > "
        print string
    elif string.find("-"):
        delimiter = "-"
        print string
    else:
        delimiter = ""

    return delimiter

# def log_wrong_gender(sku, category_id):
    # with open("wrong_gender_file_sku.txt", "a") as f:
    #     f.write("{}, ".format(sku))
    # with open("wrong_gender_file_cat_id_json.txt", "a") as f:
    #     f.write("{}, ".format(category_id))

def switch_gender(category_id, gender):
    f_to_m = {"3": 23, "4": 22, "5": 25, "6": 26, "8": 27, "15":31, "16": 32, "17": 33, "18": 34, "20": 37, "39": 35, "38": 36}
    m_to_f = {"23": 3, "22": 4, "25": 5, "26": 6, "27": 8, "31":15, "32": 16, "33": 17, "34": 18, "37": 20, "35": 39, "36": 38}

    category_id_2 = None
    gender_switched = False

    if gender == "Women":
        # print gender, "is", "Women"
        if category_id in range(22, 38, 1):
            category_id_2 = m_to_f.get(str(category_id))
            # print "Man to Women, {} to {}".format(category_id, category_id_2)
    elif category_id not in range(22, 38, 1):
            category_id_2 = f_to_m.get(str(category_id))
            # print "Women to Man, {} to {}".format(category_id, category_id_2)
    else:
        print "{} kept category_id {}".format(gender, category_id)

    if category_id_2 is not None:
        category_id = category_id_2
        gender_switched = True

    return (category_id, gender_switched)






