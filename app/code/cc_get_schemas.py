from app.code.aa_xml_flatten_utils import *
from app.code.bb_split_into_n_dirs import *
from os.path import join
from app.code.ee_system_match_functions import call_match_functions_in_order


def get_schema_dict_and_file_contents_dict_tuple(baseline_dir):

    """
    Take a directory (baseline_dir), run through each file in the directory and parse the xml.
    Return a tuple containing two objects.
    The first is a dictionary of string representations of each of the distinct schemas.
    The second is a dictionary with file name: list representation of schema
    :param baseline_dir: directory containing xml files
    :return: tuple (schema_dict, file_contents_dict)
                    schema_dict = {schema_string: [file_name, ..]}
                        schema_string = flattened, pipe delimited string of keys from xml file eg "tag1|tag2.."
                        [file_name, ..] = list of filenames with this schema
                    file_contents_dict = {file_name: ordered_dict_of_key_value_pairs}
                        ordered_dict_of_key_value_pairs = flattened dict of {key: value} of xml file
    """

    my_filenames = listdir(baseline_dir)  # run this each loop as file list will reduce after some moved.
    schema_dict = {}
    file_contents_dict = {}
    for my_filename in my_filenames:
        my_file_and_path = join(baseline_dir, my_filename)
        with open(my_file_and_path, 'r') as my_file:
            flat_list = get_flat_list(my_file)
            unzipped_list = list(zip(*flat_list))
            tags = list(unzipped_list[0])
            values = list(unzipped_list[1])
            key_string = '|'.join(tags)
            if key_string not in schema_dict.keys():
                schema_dict[key_string] = []
            schema_dict[key_string].append(my_filename)

            # add key-value pairs to dict
            file_contents_dict[my_filename] = (tags, values)  # in the form [[key,key..],[value,value..]]

    return schema_dict, file_contents_dict


'''def match_string(my_tuple):

    """
    Return a string that goes in an Excel cell, to indicate whether or not there's a match
    :param my_tuple: tuple containing (baseline_value, new_value)
    :return: string that describes whether the values match or not
    """

    a_str = str(my_tuple[0])
    b_str = str(my_tuple[1])
    if a_str == b_str:
        return "Match: " + a_str
    else:
        return "Mismatch: " + a_str + " -> " + b_str'''


def match_tags(schema_dict, my_filename_dict_list, matching_function_list, unique_string_tuple):

    """
    This takes in schema and value information for a number of files and returns a list of lists
    which represents the match information for each schema, that can be easily converted into Excel
    format.
    :param schema_dict: {"tag1|tag2.." -> ["filename1", "filename2"..] ..}
    :param my_filename_dict_list: [baseline_filename_dict, new_filename_dict]
                                    filename_dict = OrderedDict {tag1: value1, ..}
    :return: [schema_row_list, match_row_list, match_row_list, , schema_row_list, match_row_list...]
                 schema_row_list is a list of tag strings
                 match_row_list is a list of strings indicating whether or not the values match.
                            The first string in the match_row_list is the filename
    """

    print("Comparing files")
    baseline_filename_dict = my_filename_dict_list[0]
    new_filename_dict = my_filename_dict_list[1]
    my_results_list = []
    for schema in schema_dict.keys():
        file_list = schema_dict[schema]
        my_results_list.append([""])  # add a newline to differentiate schemas
        file_no_for_schema = 0
        for file_name in file_list:
            file_no_for_schema += 1
            print("\tfile_name = " + file_name)
            baseline_key_value_tuple = baseline_filename_dict[file_name]
            baseline_keys = baseline_key_value_tuple[0]
            baseline_values = baseline_key_value_tuple[1]
            new_key_value_tuple = new_filename_dict[file_name]
            new_keys = new_key_value_tuple[0]
            new_values = new_key_value_tuple[1]
            if file_no_for_schema == 1:
                title_row_contents = [""] + baseline_keys
                my_results_list.append(title_row_contents)

            if baseline_keys == new_keys:  # check if schemas match
                # value_tuples = list(zip(*(baseline_values, new_values)))
                # print("baseline_keys = "+str(baseline_keys))
                # print("baseline_values = " + str(baseline_values))
                # print("new_values = " + str(new_values))
                key_value1_value2_tuples = list(zip(baseline_keys, baseline_values, new_values))
                print("key_value1_value2_tuple = "+ str(key_value1_value2_tuples))
                # match_string_list = [match_string(pair) for pair in value_tuples]  # list of strings
                match_string_list = [call_match_functions_in_order(
                        matching_function_list,
                        key_value1_value2_tuple,
                        unique_string_tuple)
                                           for key_value1_value2_tuple in key_value1_value2_tuples]
                results_list_for_one_file = [file_name] + match_string_list
                my_results_list.append(results_list_for_one_file)
            else:
                my_results_list.append([file_name, "Mismatch - schemas dont match"])

    return my_results_list


def create_results_list(my_analysis_directory_path, my_unique_run_id_string_tuple, matching_function_list):

    """
    :param my_analysis_directory_path: path to the 'analysis' directory
    :param my_unique_run_id_string_tuple: e.g. ('10102015', '03012016')
    :param matching_function_list: list of functions which carry out the matching
    :return: a results list that can easily be processed in Excel.
    """

    path_list = [join(my_analysis_directory_path, my_dir) for my_dir in my_unique_run_id_string_tuple]
    result_tuple = [get_schema_dict_and_file_contents_dict_tuple(path) for path in path_list]
    print("result_tuple = "+str(result_tuple))
    baseline_schema_dict = result_tuple[0][0]
    filename_dict_list = [result_tuple[0][1], result_tuple[1][1]]
    results_list = match_tags(baseline_schema_dict, filename_dict_list, matching_function_list, my_unique_run_id_string_tuple)
    return results_list
