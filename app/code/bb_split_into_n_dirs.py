from os import listdir
import shutil
import os
import re
from time import sleep


def split_into_n_dirs(original_xml_directory_path, analysis_directory_path, regex_and_subdirectory_list):
    """
    :param original_xml_directory_path:
        String. Directory containing the original files
        e.g. "C:\\Users\\John\\Documents\\2016\\Python\\XML compare\\xml_samples\\CombinedDir"
    :param regex_and_subdirectory_list:
        List of strings.  The part of the filename that describes the date or run-number
        E.g. for a file of the format "test_20150301_1a.xml, test_20151030_1a.xml"
        if the following parameter is passed:
        ["20150301", "20151030"]
        this creates sub-directories \analysis\20150301 and \analysis\20151030
        each containing a file named test__1a.xml
    """

    # analysis_directory = os.path.join(source_dir, analysis_dir_string)
    analysis_directory_exits = os.path.isdir(analysis_directory_path)
    if analysis_directory_exits:
        # if bool_delete_previous_files:
            # shutil.rmtree(analysis_directory)
            # while(os.path.isdir(analysis_directory)): #shutil.rmtree removes tree asynchronously, so check it's finished.
            #    print(".")
        print("ERROR - Directory " + analysis_directory_path + " already exists. Please rename or delete first")
        return

    for regex_and_subdirectory_string in regex_and_subdirectory_list:
        find_regex = re.compile(".*" + regex_and_subdirectory_string + ".*")
        substitution_regex = re.compile(regex_and_subdirectory_string)

        new_dir = os.path.join(analysis_directory_path, regex_and_subdirectory_string)
        print("Creating directory " + new_dir)
        os.makedirs(new_dir)  # code has already checked above that analysis directory doesn't already exist

        my_file_and_directory_names = listdir(original_xml_directory_path)  # run this each loop as file list will change
        my_filenames = [filename for filename in my_file_and_directory_names
                        if not os.path.isdir(os.path.join(original_xml_directory_path, filename))]
        # print("my_filenames = " + str(my_filenames))
        for my_filename in my_filenames:
            if re.match(find_regex, my_filename):
                shorter_filename = re.sub(substitution_regex, "", my_filename)
                old_file_with_path = os.path.join(original_xml_directory_path, my_filename)
                new_file_with_path = os.path.join(new_dir, shorter_filename)
                print("\tCreating file " + new_file_with_path)
                shutil.copyfile(old_file_with_path, new_file_with_path)

# def run_split_up():
#     dir_string = "C:\\Users\\John\\Documents\\2016\\Python\\XML compare\\xml_samples\\CombinedDir"
#     split_into_n_dirs(dir_string, ["20150301", "20151030"])
