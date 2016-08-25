from xml_to_dict import *

path = "Watches_reimport/"

with open("VC_Workbook.txt", "r") as f:
    f.readline()
    unique_list = set()
    for line in f:
        listed_line = line.split("\t")
        unique_list.add(listed_line[5]+">"+listed_line[6]+">"+listed_line[7])
    with open("VC_mapping.csv", "a") as k:
        for element in unique_list:
            k.write(element+"\t\n")



# with open(path+"24522_3267514_mp.xml", "r") as f:
#     f.readline()
#     f.readline()
#     for line in f:
#         root = ElementTree.XML(line)
#         xmldict = XmlDictConfig(root)
#         with open("clock_mappings.csv", "a") as k:
#             k.write(xmldict.get("category").get("primary")+"\t"+xmldict.get("category").get("secondary")+"\t\n")
#
#
# with open(path+"38128_3267514_mp.xml", "r") as f:
#     f.readline()
#     f.readline()
#     for line in f:
#         root = ElementTree.XML(line)
#         xmldict = XmlDictConfig(root)
#         with open("clock_mappings.csv", "a") as k:
#             k.write(xmldict.get("category").get("primary") + "\t" + xmldict.get("category").get("secondary") + "\t\n")



# with open(path+"38129_3267514_mp.xml", "r") as f:
#     f.readline()
#     f.readline()
#     for line in f:
#         root = ElementTree.XML(line)
#         xmldict = XmlDictConfig(root)
#         with open("clock_mappings.csv", "a") as k:
#             k.write(xmldict.get("category").get("primary")+"\t"+xmldict.get("category").get("secondary")+"\t\n")


# with open("clock_mappings.csv", "r") as f:
#     unique_list = set()
#     for line in f:
#         unique_list.add(line)
#
#     for element in unique_list:
#         with open("clock_mappings_unique.csv", "a") as k:
#             if element[0] == 'W':
#                 if element.split("\t")[1].split("~~")[0] == "Watches":
#                     k.write(element.replace("\n", "")+"18\n")
#                 else:
#                     k.write(element.replace("\n", "") + "38\n")
#             else:
#                 if element.split("\t")[1].split("~~")[0] == "Watches":
#                     k.write(element.replace("\n", "") + "34\n")
#                 else:
#                     k.write(element.replace("\n", "") + "36\n")