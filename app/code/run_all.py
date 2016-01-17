from os import system
from os.path import join
from app.code.bb_split_into_n_dirs import split_into_n_dirs
from app.code.cc_get_schemas import create_results_list
from app.code.dd_write_to_excel import write_with_xlsxwriter
from app.code.ff_user_match_functions import *

original_xml_directory_path = "C:\\Users\\John\\Documents\\2016\\Python\\XML compare\\xml_samples\\CombinedDir"
analysis_directory_path = join(original_xml_directory_path, "analysis")
unique_run_id_string_tuple = ("20150301", "20151030")
excel_file_and_path = join(analysis_directory_path, "results.xlsx")

matching_function_list = [match_messageid_in_key, diff_in_unique_tuple]

split_into_n_dirs(original_xml_directory_path, analysis_directory_path, unique_run_id_string_tuple)
results_list = create_results_list(analysis_directory_path, unique_run_id_string_tuple, matching_function_list)
write_with_xlsxwriter(excel_file_and_path, results_list, unique_run_id_string_tuple)
system('start excel.exe "%s"' % excel_file_and_path)

# TODO pass colours along with functions.
# TODO put complexity of excel formatting in the Excel code.
# TODO create pivotable format
# TODO don't copy files, but instead create a dict of longname to shortname
# TODO test to time performance
