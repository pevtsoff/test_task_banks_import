import glob
import os
import sys
import config_params
from csv_parser import parse_csv_file, output_fields
from default_logger import logger
from writers import CSVWriter, JSONWriter, XMLWriter


def get_writer(output_type):
    if output_type == 'csv':
       return  CSVWriter
    elif output_type == 'json':
       return JSONWriter
    elif output_type == 'xml':
       return XMLWriter
    else:
       raise RuntimeError(
            "Wrong Output format: Only support csv format for now!"
       )


def get_exit_code(error_file):
    if error_file.tell():
        logger.info('Import finished with errors')
        return 1
    else:
        logger.info('Import finihsed without errors')
        return 0


def main():
    input_file_path = f'{config_params.BANK_FILES_PATH}/*.csv'
    output_file_path = config_params.OUTPUT_FILE_PATH
    error_file_path = config_params.ERROR_FILE_PATH
    files = [*glob.iglob(input_file_path, recursive=True)]

    with open(output_file_path, 'w') as output_file:
        with open(error_file_path, 'w') as error_file:

            writer = get_writer(
                config_params.OUTPUT_TYPE
            )(output_file, output_fields)

            for file_path in files:
                parse_csv_file(file_path, writer, error_file)

            sys.exit(get_exit_code(error_file))



if __name__ == '__main__':
    main()

