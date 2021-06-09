import os

BANK_FILES_PATH = os.environ.get('BANK_FILES_PATH', './bank_files')
OUTPUT_FILE_PATH = os.environ.get('OUTPUT_FILE_PATH', './output/unified_output.txt')
ERROR_FILE_PATH = os.environ.get('ERROR_FILE_PATH', './output/error_output.txt')
INPUT_ENCODING = os.environ.get('INPUT_ENCODING', 'utf-8')
OUTPUT_TYPE = os.environ.get('OUTPUT_TYPE', 'csv')