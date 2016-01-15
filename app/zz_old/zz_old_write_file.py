# write file
def write_results_list_to_file(file_and_path, results_list):
    delimiter_string = "|"
    with open(file_and_path, "w") as text_file:
        for results_line in results_list:
            delimited_string = delimiter_string.join(results_line)
            text_file.write(delimited_string + '\n')


# remove files
    # if bool_delete_previous_files:
    # shutil.rmtree(analysis_directory)
    # while(os.path.isdir(analysis_directory)):
    # shutil.rmtree removes tree asynchronously, so check it's finished.
    #    print(".")


'''try:
    os.remove(file_and_path)
except PermissionError:
    print("ERROR - can't delete previous results file. Check if it's open in Excel and close down.")
    # TODO - why does exception still get raised here?  Should be caught.
except FileNotFoundError:
    print("ERROR - file not found - can't delete it")'''