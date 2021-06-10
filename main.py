import glob
import sys
import time
from api import config_params
from api.csv_parser import parse_csv_file, output_fields
from api.default_logger import logger
from api.writers import CSVWriter, JSONWriter, XMLWriter


NO_ERRORS = 0
PARSING_ERRORS_OCCURED = 1
FATAL_ERRORS_OCCURED = 2


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
        return ERRORS_OCCURED

    else:
        logger.info('Import finished without errors')
        return NO_ERRORS


def get_input_files_list():
    input_file_path = f'{config_params.BANK_FILES_PATH}/*.csv'
    return [*glob.iglob(input_file_path, recursive=True)]

def check_input_files(files):
    if not files:
        raise RuntimeError(
            f"No input files found by a specified path: {config_params.BANK_FILES_PATH}"
        )


def main():
    output_file_path = config_params.OUTPUT_FILE_PATH
    error_file_path = config_params.ERROR_FILE_PATH

    files = get_input_files_list()
    start = time.time()
    logger.info('Starting parser')

    try:
        with open(output_file_path, 'w') as output_file:
            with open(error_file_path, 'w') as error_file:
                check_input_files(files)

                writer = get_writer(
                    config_params.OUTPUT_TYPE
                )(output_file, output_fields)

                for file_path in files:
                    parse_csv_file(file_path, writer, error_file)

                logger.info(f'parsing took {time.time() - start:2f} seconds')
                sys.exit(get_exit_code(error_file))

    except Exception as e:
        logger.exception(f'error occured while initializing readers/writers: {e}')

    finally:
        sys.exit(FATAL_ERRORS_OCCURED)

if __name__ == '__main__':
    main()

