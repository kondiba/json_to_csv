#!/usr/bin/python
from types import *
import argparse
import json
import csv


def main():

    parser = argparse.ArgumentParser(
        description='Convert json file to csv'
    )

    parser.add_argument(
        '-i',
        '--input_file',
        dest='input_file',
        default=None,
        required=True,
        help='Source json file (mandatory)'
    )
    parser.add_argument(
        '-o',
        '--output_file',
        dest='output_file',
        default=None,
        required=True,
        help='Destination csv file (mandatory)'
    )

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file

    json_data = []
    data = None
    write_header = True
    item_keys = []

    with open(input_file) as json_file:
        json_data = json_file.read()

    try:
        data = json.loads(json_data)
    except Exception as e:
        raise e

    with open(output_file, 'wb') as csv_file:
        writer = csv.writer(csv_file)

        value_dict = {}
        item_values = []
        item_values1 = []
        i = 0
        for key in data:
            i += 1
            value = data.get(key,'')
            if 'list' in str(type(value)):
                item_keys.append(key)
                for k in range(len(value)):
                    if value_dict.has_key(k):
                        for l in range(0,i):
                            try :
                                value_dict[k][l]
                            except:
                                value_dict[k].append("")
                    else:
                        value_dict[k] = [""]
                        for l in range(0,i-1):
                            value_dict[k].append("")

                    value_dict[k][i-1]= value[k]
            elif 'dict' in str(type(value)):
                for k,v in value.items():
                    item_keys.append(key+'_'+str(k))
                    if value_dict.has_key(0):
                        value_dict[0].append(v)
                    else:
                        value_dict[0] = [v]
            else:
                item_keys.append(key)
                value_dict[0].append(value)

        if write_header:
            writer.writerow(item_keys)
            write_header = False
        for k in range(0,i):
            if value_dict.has_key(k):
                writer.writerow(value_dict[k])

if __name__ == "__main__":
    main()