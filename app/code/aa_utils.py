import collections
from collections import OrderedDict
import xmltodict


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():

        if v.__class__ == list:
            new_ordered_dict = OrderedDict()
            for i in range(0, len(v)):
                my_new_key = "<"+str(i)+">"
                new_ordered_dict.update({my_new_key: v[i]})
            v = new_ordered_dict
        new_key = parent_key + sep + k if parent_key else k

        if v.__class__ == collections.OrderedDict:
            items.extend(flatten(v, new_key, sep=sep).items())

        else:
            items.append((new_key, v))
    return OrderedDict(items)


def get_flat_list_from_xml_string(my_string):
    my_ordered_dict = xmltodict.parse(my_string)
    flat_dict = flatten(my_ordered_dict)
    items_list = list(flat_dict.items())
    return items_list


def get_flat_list(file):
    return get_flat_list_from_xml_string(file.read())
