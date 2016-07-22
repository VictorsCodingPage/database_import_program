def scan_file_to_list(file, delimiter):
    with open(file, "r") as f:
        read_data = f.read()
    f.close()
    list_data = read_data.split(delimiter)
    return list_data
