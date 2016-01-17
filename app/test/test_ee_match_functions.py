from app.code.ff_user_match_functions import *
from app.code.ee_system_match_functions import *
import unittest


class TestUtils(unittest.TestCase):
    def test_match_value_match_returns_false_green(self):
        actual_result = match_value("any_key", ("val1", "val1"), ("111", "222"))
        expected_result = (True, 'Match: val1')
        print("actual result = ")
        print(actual_result)
        assert(expected_result == actual_result)

    def test_match_value_match_returns_true_red(self):
        actual_result = match_value("any_key", ("val1", "val2"), ("111", "222"))
        expected_result = (False, 'X-Mismatch: val1 -> val2')
        print("actual result = ")
        print(actual_result)
        assert(expected_result == actual_result)

    def test_match_match_messageid_in_key_match_returns_false(self):
        actual_result = match_messageid_in_key("any_key_messageId", ("val1", "val2"), ("111", "222"))
        expected_result = (True, 'Ignore: Key contains messageId, key = any_key_messageId, val1 -> val2')
        print("actual result = ")
        print(actual_result)
        assert(expected_result == actual_result)

    def test_match_messageid_in_key_no_match_returns_true(self):
        actual_result = match_messageid_in_key("any_key", ("val1", "val2"), ("111", "222"))
        expected_result = None
        print("actual result = ")
        print(actual_result)
        assert(expected_result == actual_result)

    def test_diff_in_unique_tuple_positive(self):
        actual_result = diff_in_unique_tuple("any_key", ("val_111_1", "val_222_1"), ("111", "222"))
        expected_result = (True, 'Ignore: Values only differ by unique parts of filename, val_111_1 -> val_222_1')
        print("actual result = ")
        print(actual_result)
        assert(expected_result == actual_result)

    def test_diff_in_unique_tuple_negative(self):
        actual_result = diff_in_unique_tuple("any_key", ("val_111_1", "val_22_1"), ("111", "222"))
        expected_result = None
        print("actual result = ")
        print(actual_result)
        assert(expected_result == actual_result)

    # FUNCTIONS IN ORDER
    function_list = [match_messageid_in_key, diff_in_unique_tuple]

    def test_call_functions_in_order_match(self):
        actual_result = call_match_functions_in_order(
                TestUtils.function_list,
                ("any_key", "val1", "val1"),
                ("111", "222"))
        expected_result = ('Match: val1')
        print(actual_result)
        assert(expected_result == actual_result)

    def test_call_functions_in_order_no_match(self):
        actual_result = call_match_functions_in_order(
                TestUtils.function_list,
                ("any_key", "val1", "val2"),
                ("111", "222"))
        expected_result = ('X-Mismatch: val1 -> val2')
        print(actual_result)
        assert(expected_result == actual_result)

    def test_call_functions_in_order_special_key(self):
        actual_result = call_match_functions_in_order(
                TestUtils.function_list,
                ("any_key_messageId", "val1", "val2"),
                ("111", "222"))
        expected_result = ('Ignore: Key contains messageId, key = any_key_messageId, val1 -> val2')
        print(actual_result)
        assert(expected_result == actual_result)

    def test_call_functions_in_order_diff_in_unique_tuple(self):
        actual_result = call_match_functions_in_order(
                TestUtils.function_list,
                ("any_key", "val_111_1", "val_222_1"),
                ("111", "222"))
        expected_result = ('Ignore: Values only differ by unique parts of filename, val_111_1 -> val_222_1')
        print(actual_result)
        assert(expected_result == actual_result)

if __name__ == '__main__':
    unittest.main()
