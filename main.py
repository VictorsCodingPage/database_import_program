def set_directory_to_read_from(main_directory, sub_directory):
    return "database_files_to_send/{}/{}_files".format(main_directory, sub_directory)

def main():
    from data_verification.file_exemption_filter import compare_exempt_files_to_all_files,\
                                                        update_exempt_files_file
    from os import listdir
    from os.path import isfile, join
    from database_input_output.data_sending_functions import data_sending
    from database_input_output.data_retrieval_functions import data_retrieval
    import psycopg2
    from parsing_functions.delimited_files_parsing import delimited_files_parsing_general, json_parsing, xml_parsing
    from mapping_from_header import map_from_header
    from data_reading.scan_file_to_dict import scan_file_to_dict

    # BOOLEAN FLAGS
    test = False
    json_input = False
    xml_input = False
    mr_porter = False

    # FILE_PATH None = DEFAULT PATH
    if json_input == True:
        file_path = "files_json"
    elif mr_porter == True:
        file_path = "LS_MrPorter"
    elif xml_input  == True:
        file_path = "Watches_reimport"
    else:
        file_path = "VC_import"


    # FILES TO OPEN
    exemption_file = "logfile.txt"
    if xml_input == True:
        dict_level_2_file= "LinkShare_Categories_mapped.csv"
        index_of_key = 3
        index_of_value = 2
        index_of_value_2 = 1
        level_1_index_key = 1
        level_1_index_val = 2
    elif mr_porter == True:
        dict_level_2_file = "mrporter_categories_mapped.csv"
        index_of_key = 1
        index_of_value = 2
        level_1_index_key = 0
        level_1_index_val = 0
    else:
        dict_level_2_file= "CJ_Categories_mapped_new.csv"
        index_of_key = 2
        index_of_value = 1
        index_of_value_2 = 0
        level_1_index_key = 1
        level_1_index_val = 0
    # dict_level_1_file= "HotCatToID.csv"
    dict_level_1_file = "VC_mapping.csv"

    # DELIMITERS
    delimiter_file_to_parse = "\t"
    mapping_delimiter = "\t"
    exemptions_delimiter = "\t"
    dict_delimiter = "\t"

    # CONNECTION STRING
    host="example_host"
    dbname="example_dbname"
    user="example_user"
    password="exaple_password"
    port="example_port"

    connection_string = "host={} dbname={} user={} password={} port={}".format(host, dbname, user, password, port)

    print "Destination database: ", connection_string

    # READ ALL FILE NAMES TO MEMORY
    if file_path == None:
        file_path = set_directory_to_read_from("CJ", "txt")
    filesInPath = [f for f in listdir(file_path) if isfile(join(file_path, f))]

    # EXEMPT ANY PREVIOUSLY READ FILES FROM THE LIST OF FILE NAMES
    onlyfiles = compare_exempt_files_to_all_files(filesInPath, "\t", exemption_file)
    onlyfiles_length = len(onlyfiles)

    # CREATE DICT FILTERS
    if mr_porter == False or xml_input == False:
        category_to_gender_dict = scan_file_to_dict(dict_level_2_file, index_of_key, index_of_value_2, dict_delimiter)
    level_2_cat_dict = scan_file_to_dict(dict_level_2_file, index_of_key, index_of_value, dict_delimiter)
    level_1_cat_dict = scan_file_to_dict(dict_level_1_file, level_1_index_key, level_1_index_val, dict_delimiter)
    color_dict = scan_file_to_dict("Color_mapping.txt", 2, 0, ";")

    print level_1_cat_dict

    level_1_cat_dict_male = scan_file_to_dict("HotCatToID_Male.csv", 1, 0, dict_delimiter)
    level_1_cat_dict_female = scan_file_to_dict("HotCatToID_Female.csv", 1, 0, dict_delimiter)

    # ITERATE THROUGH THE LIST OF FILE NAMES
    file_counter = 0
    product_counter = 0
    for file in onlyfiles:
        print "Parsing {}".format(file)
        complete_file_path = file_path+"/"+file

        # PARSE FUNCTION(S)
        if json_input == True:
            product_list = json_parsing(complete_file_path, level_1_cat_dict, level_2_cat_dict, category_to_gender_dict)
        elif xml_input == True or mr_porter == True:
            product_list = xml_parsing(complete_file_path, level_1_cat_dict, level_2_cat_dict, category_to_gender_dict)
        else :
            data_mapping_list = map_from_header(complete_file_path, mapping_delimiter)
            product_list = delimited_files_parsing_general(complete_file_path, delimiter_file_to_parse, data_mapping_list, level_1_cat_dict, level_2_cat_dict, color_dict)

        if len(product_list) >= 1:

            print len(product_list)

            # SET UP CONNECTION
            dbconn = psycopg2.connect(connection_string)
            cursor = dbconn.cursor()

            # GET STORE LISTS
            store_name_list = data_retrieval.get_store_name_list(cursor)
            store_bool_list = [True] * len(store_name_list)

            # RETRIEVE STORE_ID FROM SERVER
            vendor = product_list[0].vendor
            store_id = data_retrieval.get_store_id_from_stores(vendor, cursor)
            if store_id == -1:
                data_sending.insert_store(cursor, vendor, store_name_list, store_bool_list)
                store_id = data_retrieval.get_store_id_from_stores(vendor, cursor)

            # SEND DATA TO SERVER
            product_counter += data_sending.export_data_to_database(product_list, store_id, cursor)

            # DATA UPDATE
            # data_sending.update_data_in_database(product_list, store_id, cursor)

            dbconn.commit()
            dbconn.close()

        file_counter += 1
        print "Finished sending {} products, contained in \n{} out of {} files".format(product_counter, file_counter, onlyfiles_length)
        update_exempt_files_file(exemption_file, exemptions_delimiter, file)


if __name__ == "__main__":
    main()