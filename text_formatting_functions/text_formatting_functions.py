def hierarchy_formatter(hierarchy_string_to_format, input_delimiter, output_delimiter):
    hierarchy_object_list = hierarchy_string_to_format.split(input_delimiter)
    formatted_hierarchy = "{}".format(hierarchy_object_list[0].lstrip(" "), output_delimiter)
    for number in range(1, len(hierarchy_object_list)):
        formatted_hierarchy += " {} {}".format(output_delimiter, hierarchy_object_list[number].lstrip(" "))
    return formatted_hierarchy
