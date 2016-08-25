import json

def map_from_header(file, delimiter):
    with open(file, "r") as f:
        mapping = f.readline().split(delimiter)
        print mapping
        return mapping