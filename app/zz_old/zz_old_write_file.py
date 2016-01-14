
def write_results_list_to_file(file_and_path, results_list):
    # print("file_and_path = " + file_and_path)
    # file = os.open(file_and_path)
    # print("filexx = " + str(file))
    with open(file_and_path, "w") as text_file:
        for results_line in results_list:
            delimited_string = delimiter_string.join(results_line)
            # print(delimited_string)
            text_file.write(delimited_string + '\n')