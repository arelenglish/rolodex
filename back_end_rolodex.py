"""Accepts a file of addresses and returns a formatted JSON output.
    
Usage:

    python3 back_end_rolodex.py
"""

import re
import json
from collections import OrderedDict

def filter_addresses(address_file):
    addresses = []
    errors = []
    phone_num_re = re.compile('(\+0?1\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}')
    
    with open(address_file, 'r') as f:
        for idx, line in enumerate(f):
            if re.search(phone_num_re, line):
                addresses.append(line.strip())
            else:
                errors.append(idx)
    return [addresses, errors]


def build_rolodex(address_file):
    addresses = filter_addresses(address_file)[0]
    organized_addresses = {"entries": [], "errors": filter_addresses(address_file)[1]}

    for address in addresses:
        address_object = pick_format(address)
        sorted_address_object = OrderedDict(sorted(address_object.items()))
        organized_addresses["entries"].append(sorted_address_object)
    return organized_addresses


def pick_format(address):
    spaces_re = re.compile('\d{3}\ {1}\d{3}\ {1}\d{4}')
    data = address.split(', ')
    
    if len(data) == 4:
        return address_with_full_name(data)
    elif re.search(spaces_re, address):
        return address_with_spaces(data)
    else:
        return address_with_parens(data)


def address_with_parens(data):
    #format: ['Lastname', 'Firstname', '(703)-742-0996', 'Blue', '10013']
    result = {}
    result["lastname"] = data[0]
    result["firstname"] = data[1]
    result["phonenumber"] = phone_number_formatter(data[2])
    result["color"] = data[3]
    result["zipcode"] = data[4]
    return result


def address_with_full_name(data):
    #format: ['Firstname Lastname', 'Red', '11237', '703 955 0373']
    name = data[0].split()
    result = {}
    result["firstname"] = name[0]
    result["lastname"] = name[1]
    result["color"] = data[1]
    result["zipcode"] = data[2]
    result["phonenumber"] = phone_number_formatter(data[3])
    return result


def address_with_spaces(data):
    #format: ['Firstname', 'Lastname', '10013', '646 111 0101', 'Green']
    result = {}
    result["firstname"] = data[0]
    result["lastname"] = data[1]
    result["zipcode"] = data[2]
    result["phonenumber"] = phone_number_formatter(data[3])
    result["color"] = data[4]
    return result


def phone_number_formatter(phone_number):
    clean_number = re.sub('\D', '', phone_number)
    formatted_number = clean_number[0:3] + "-" + clean_number[3:6] + "-" + clean_number[6:10]
    return formatted_number


def generate_output(address_file):
    f = open('json.out', 'w+')
    sorted_rolodex = OrderedDict(sorted(build_rolodex(address_file).items()))
    f.write(json.dumps(sorted_rolodex, indent=2))


def main():
    generate_output('./data.in')


if __name__ == '__main__':
    main()
    