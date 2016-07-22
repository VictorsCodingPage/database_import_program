from data_reading.scan_file_to_list import *

def compare_exempt_files_to_all_files(file_list, delimiter, exempt_files_file):
    counter = 0
    updated_file_list = []
    exempt_files_list = scan_file_to_list(exempt_files_file, delimiter)
    for file in file_list:
        if file in exempt_files_list:
            counter += 1
        else:
            updated_file_list.append(file)
    print "Exempted {} out of {} files".format(counter, len(file_list))
    return updated_file_list

def update_exempt_files_file(exempt_files_file, delimiter, string):
    writeTo = open(exempt_files_file, "a")
    writeTo.write(string + delimiter)
    writeTo.close()
