def hierarchy_formatter(hierarchy_list, input_delimiter, output_delimiter, gender):
    hierarchy_object_list = hierarchy_list
    formatted_hierarchy = "{}".format(gender)
    for number in range(0, len(hierarchy_object_list)):
        formatted_hierarchy += " {} {}".format(output_delimiter, hierarchy_object_list[number].lstrip(" "))
    return formatted_hierarchy

def hierarchy_formatter_xml(primary_category, secondary_category, gender):
    formatted_hierarchy = "{}".format(primary_category)
    if secondary_category != None:
        # arrowsplit_scategory = secondary_category.split(">")
        # dashsplit_scategory = secondary_category.split("-")
        # finished_split_scategory = which_is_longest(arrowsplit_scategory, dashsplit_scategory)
        finished_split_scategory = secondary_category.split("~~")
        if finished_split_scategory != None:
            for category in finished_split_scategory:
                formatted_hierarchy += " {} {}".format(">", category.strip())

    return formatted_hierarchy

def which_is_longest(listA, listB):
    if len(listA) > len(listB):
        longest = listA
    elif len(listA) < len(listB):
        longest = listB
    else:
        longest = None

    return longest



