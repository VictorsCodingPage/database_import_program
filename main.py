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
    from parsing_functions.delimited_files_parsing import delimited_files_parsing_general
    from mapping_from_header import map_from_header
    from data_reading.scan_file_to_dict import scan_file_to_dict

    # TEST RUN OR REAL RUN
    test = True

    # FILE_PATH None = DEFAULT PATH
    file_path = "files_to_read"

    # FILES TO OPEN
    exemption_file = "logfile.txt"
    dict_level_2_file= "CJ_Categories.csv"
    dict_level_1_file= "HotCatToID.csv"

    # DELIMITERS
    parse_file_delimiter = "\t"
    mapping_delimiter = "\t"
    exemptions_delimiter = "\t"
    dict_delimiter = "\t"

    # CONNECTION STRING
    connection_string = ""

    if test:
        connection_string = "host=localhost dbname=CJtestdb user=postgres password=1234 port=5432"
    else:
        connection_string = "host=hotspottingdevelopment2.cd3jzpbeunmh.ap-southeast-1.rds.amazonaws.com dbname=hotspotting_production user=hotspotting password=kae5eesh5FahPh0e port=5432"

    # READ ALL FILE NAMES TO MEMORY
    if file_path == None:
        file_path = set_directory_to_read_from("CJ", "txt")
    filesInPath = [f for f in listdir(file_path) if isfile(join(file_path, f))]

    # EXEMPT ANY PREVIOUSLY READ FILES FROM THE LIST OF FILE NAMES
    onlyfiles = compare_exempt_files_to_all_files(filesInPath, "\t", exemption_file)
    onlyfiles_length = len(onlyfiles)

    #CREATE DICT FILTERS
    level_2_cat_dict = scan_file_to_dict(dict_level_2_file, 2, 1, dict_delimiter)
    level_1_cat_dict = scan_file_to_dict(dict_level_1_file, 1, 0, dict_delimiter)

    # ITERATE THROUGH THE LIST OF FILE NAMES
    file_counter = 0
    for file in onlyfiles:
        print "Parsing {}".format(file)
        complete_file_path = file_path+"/"+file

        # PARSE FUNCTION(S)
        data_mapping_list = map_from_header(complete_file_path, mapping_delimiter)
        product_list =  delimited_files_parsing_general(complete_file_path, parse_file_delimiter, data_mapping_list, level_1_cat_dict, level_2_cat_dict)

        if len(product_list) >= 1:

            # SET UP CONNECTION
            dbconn = psycopg2.connect(connection_string)
            cursor = dbconn.cursor()

            # GET STORE LISTS
            store_name_list = data_retrieval.get_store_name_list(cursor)
            store_bool_list = [True] * len(store_name_list)

            # RETRIEVE STORE_ID FROM SERVER
            vendor = product_list[0].vendor
            store_id = data_retrieval.get_store_id_from_stores(vendor, cursor)
            if not store_id:
                data_sending.insert_store(cursor, vendor, store_name_list, store_bool_list)

            # SEND DATA TO SERVER
            data_sending.export_data_to_database(product_list, store_id, cursor)

            dbconn.commit()
            dbconn.close()

        file_counter += 1
        print "Finished sending {} out of {} files".format(file_counter, onlyfiles_length)
        update_exempt_files_file(exemption_file, exemptions_delimiter, file)


if __name__ == "__main__":
    main()