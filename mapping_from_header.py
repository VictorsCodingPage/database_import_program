def map_from_header(file, delimiter):
    with open(file, "r") as f:
        return f.readline().split(delimiter)