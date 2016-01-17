import re

# Functions that take key and value and figure out whether its a match or not


def match_value(key, value_str_tuple, unique_tuple):
    # print("str_tuple = " + str(value_str_tuple))
    if value_str_tuple[0] == value_str_tuple[1]:
        return True, "Match: " + value_str_tuple[0]  # True means match
    else:
        return False, "X-Mismatch: " + value_str_tuple[0] + " -> " + value_str_tuple[1]


def call_match_functions_in_order(function_list, key_value1_value2_tuple, unique_tuple):
    two_part_tuple = call_match_functions_in_order_helper(function_list, key_value1_value2_tuple, unique_tuple)
    return two_part_tuple[1]


def call_match_functions_in_order_helper(function_list, key_value1_value2_tuple, unique_tuple):
    key = key_value1_value2_tuple[0]
    value_tuple = (key_value1_value2_tuple[1], key_value1_value2_tuple[2])
    initial_result = match_value(key, value_tuple, unique_tuple)
    if initial_result[0] == True:
        return initial_result
    else:
        for my_func in function_list:
            my_new_result = my_func(key, value_tuple, unique_tuple)
            if my_new_result != None:
                return my_new_result
    return(initial_result)


def string_contains(my_string, regex_string):
    regex = re.compile(".*"+regex_string+".*")
    return regex.match(my_string)

