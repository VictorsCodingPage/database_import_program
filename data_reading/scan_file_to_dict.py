def scan_file_to_dict(file_name, index_of_key, index_of_value, delimiter):
    tuple_list = []
    with open(file_name, "r") as f:
        header = f.readline()
        for line in f:
                splitLine = line.split(delimiter)
                tuple = (splitLine[index_of_key].replace("\n", ""), splitLine[index_of_value].replace("\n", ""))
                tuple_list.append(tuple)
    f.close()

    dictionary = dict([(p[0], p[1]) for p in tuple_list])
    return dictionary
