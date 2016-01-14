from app.code.dd_write_to_excel import *
from datetime import date
'''Iterate through the files in the baseline dictionary
Create a dict with schema list as the key.  Add the filename to the values.
This is so we can go through the dict keys in the next step
and for each schema process the set of files which are the values.'''

from app.code.aa_utils import *
from app.code.bb_split_into_n_dirs import *
from os.path import join


def get_schema_dict_and_file_contents_dict_tuple(baseline_dir, separator_string):
    """
    Take a directory (baseline_dir), run through each file in the directory and parse the xml.
    Return a tuple containing two objects.
    The first is a dictionary of string representations of each of the distinct schemas.
    The second is a dictionary with file name: list representation of schema
    :param baseline_dir: directory containing xml files
    :param separator_string:
    :return:
    """
    my_filenames = listdir(baseline_dir)  # run this each loop as file list will reduce after some moved.
    schema_dict = {}
    file_contents_dict = {}
    for my_filename in my_filenames:
        my_file_and_path = join(baseline_dir, my_filename)
        # print(my_file_and_path)
        # first get dict of unique schemas with list of filenames
        with open(my_file_and_path, 'r') as my_file:
            flat_list = get_flat_list(my_file)
            unzipped_list = list(zip(*flat_list))
            tags = list(unzipped_list[0])
            values = list(unzipped_list[1])
            key_string = separator_string.join(tags)
            if key_string not in schema_dict.keys():
                schema_dict[key_string] = []
            schema_dict[key_string].append(my_filename)

            # add key-value pairs to dict
            file_contents_dict[my_filename] = (tags, values)  # in the form [[key,key..],[value,value..]]

    return schema_dict, file_contents_dict


def match_string(my_tuple):
    a_str = str(my_tuple[0])
    b_str = str(my_tuple[1])
    if a_str == b_str:
        return "Match: " + a_str
    else:
        return "Mismatch: " + a_str + " -> " + b_str


def match_tags(schema_dict, my_filename_dict_list):
    # where schema_dict has format {"tag1|tag2.." -> ["filename1", "filename2"..] ..}
    # and filename_dict has format {"filename1" -> ([tag1, tag2..], [value1, value2..]) ..}
    # filename_dict_list is a list containing [baseline_filename_dict, new_filename_dict]
    baseline_filename_dict = my_filename_dict_list[0]
    new_filename_dict = my_filename_dict_list[1]
    results_list = []
    for schema in schema_dict.keys():
        file_list = schema_dict[schema]
        results_list.append([""])  # add a newline to differentiate schemas
        file_no_for_schema = 0
        for file_name in file_list:
            file_no_for_schema += 1
            print("file_name = " + file_name)
            baseline_key_value_tuple = baseline_filename_dict[file_name]
            baseline_keys = baseline_key_value_tuple[0]
            baseline_values = baseline_key_value_tuple[1]
            new_key_value_tuple = new_filename_dict[file_name]
            new_keys = new_key_value_tuple[0]
            new_values = new_key_value_tuple[1]
            if file_no_for_schema == 1:
                # title_row_contents = [""]
                title_row_contents = [""] + baseline_keys
                results_list.append(title_row_contents)
                # Only do this the first time round
                # Prepending the space at the front of the list has effect of adding an extra blank cell above filenames

            if baseline_keys == new_keys:  # check if schemas match
                value_tuples = list(zip(*(baseline_values, new_values)))
                # print("value_tuples:")
                # print(value_tuples)
                match_string_list = [match_string(pair) for pair in value_tuples]  # list of strings
                # results_list_for_one_file = [file_name]
                # print(results_list_for_one_file)
                results_list_for_one_file = [file_name] + match_string_list
                print(str(results_list_for_one_file))
                results_list.append(results_list_for_one_file)
            else:
                results_list.append([file_name, "Mismatch - schemas dont match"])

    return results_list


original_xml_directory_path = "C:\\Users\\John\\Documents\\2016\\Python\\XML compare\\xml_samples\\CombinedDir"
analysis_directory_path = join(original_xml_directory_path, "analysis")
unique_run_id_string_list = ["20150301", "20151030"]
split_into_n_dirs(original_xml_directory_path, analysis_directory_path, unique_run_id_string_list)

delimiter_string = "|"  # ','
# baseline_path = join(analysis_directory_path, unique_run_id_string_list[0])
path_list = [join(analysis_directory_path, my_dir) for my_dir in unique_run_id_string_list]
result_tuple = [get_schema_dict_and_file_contents_dict_tuple(path, delimiter_string) for path in path_list]
# returns [(baseline_schema_dict, baseline_filename_dict), (new_schema_dict, new_filename_dict)}
# where schema_dict has format {"tag1|tag2.." -> ["filename1", "filename2"..] ..}
# and filename_dict has format {"filename1" -> ([tag1, tag2..], [value1, value2..]) ..}
baseline_schema_dict = result_tuple[0][0]
filename_dict_list = [result_tuple[0][1], result_tuple[1][1]]

# print("a = "+str(baseline_schema_dict))
# print("b = " + str(baseline_filename_dict))

results_list = match_tags(baseline_schema_dict, filename_dict_list)
# print(results_list)
file_and_path = join(analysis_directory_path, "results.dat")
'''try:
    os.remove(file_and_path)
except PermissionError:
    print("ERROR - can't delete previous results file. Check if it's open in Excel and close down.")
    # TODO - why does exception still get raised here?  Should be caught.
except FileNotFoundError:
    print("ERROR - file not found - can't delete it")'''
# write_results_list_to_file(file_and_path, results_list) #old way line by line.

# TODO - figure out why last line truncated
# TODO - write in Excel format directly.

excel_file_and_path = join(analysis_directory_path, "results.xlsx")
print("excel_file_and_path = " + excel_file_and_path)

date_string = date.today().strftime("%B %d, %Y")
title_string = "XML Comparison run on " + date_string
subtitle_string = "Baseline = " + unique_run_id_string_list[0] + \
                  ", Latest = " + unique_run_id_string_list[1]

write_with_xlsxwriter(excel_file_and_path, results_list, title_string, subtitle_string)
os.system('start excel.exe "%s"' % excel_file_and_path)
