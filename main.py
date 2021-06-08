import glob
import sys

import config_params
from csv import DictWriter
from csv_parser import parse_csv_file, output_fields


def get_exit_code(error_file):
    if error_file.tell():
        print('Import finished with errors')
        return 1
    else:
        print('Import finihsed without errors')
        return 0


def main():
    input_file_path = f'{config_params.BANK_FILES_PATH}/*.csv'
    output_file_path = config_params.OUTPUT_FILE_PATH
    error_file_path = config_params.ERROR_FILE_PATH
    files = [*glob.iglob(input_file_path, recursive=True)]

    with open(output_file_path, 'w') as output_file:
        with open(error_file_path, 'w') as error_file:
            csv_dict_writer = DictWriter(
                output_file, delimiter=',', fieldnames=output_fields
            )
            csv_dict_writer.writeheader()

            for file_path in files:
                parse_csv_file(file_path, csv_dict_writer, error_file)

            sys.exit(get_exit_code(error_file))



if __name__ == '__main__':
    main()

