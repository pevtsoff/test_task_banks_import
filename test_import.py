import os
import pytest
import glob

import config_params
from main import main, get_writer
from csv import DictWriter
from csv_parser import output_fields, parse_csv_file


input_file_path = './test_data/*.csv'
output_file_path = './test_output/unified_output.txt'
error_file_path = './test_output/error_output.txt'
test_output_folder = './test_output'

expected_output = {
    './test_data/bank1.csv': 'date,transaction_type,amount,from,to\n'
                             '2019-10-01,remove,99.20,198,182\n'
                             '2019-10-02,add,2000.10,188,198\n',
    './test_data/bank2.csv': 'date,transaction_type,amount,from,to\n'
                             '2019-03-10,remove,99.40,198,182\n'
                             '2019-04-10,add,2123.50,188,198\n',
    './test_data/bank3.csv': 'date,transaction_type,amount,from,to\n'
                             '2019-10-05,remove,5.07,198,182\n'
                             '2019-10-06,add,1060.08,188,198\n',
}


@pytest.fixture(scope='function')
def setup_output_files():

    if not os.path.exists(test_output_folder):
        os.mkdir(test_output_folder)

    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    if os.path.exists(error_file_path):
        os.remove(error_file_path)

    with open(output_file_path, 'w+') as output_file:
        with open(error_file_path, 'w+') as error_file:
            writer = get_writer(
                config_params.OUTPUT_TYPE
            )(output_file, output_fields)

            yield output_file, writer, error_file


################################################### Positive Tests #####################################################
@pytest.mark.parametrize('expected_output_item', [*expected_output.items()])
def test_valid_import(setup_output_files, expected_output_item):
    output_file = setup_output_files[0]
    parse_csv_file(expected_output_item[0], setup_output_files[1], setup_output_files[2])
    expected_data = expected_output_item[1]
    actual_data = _get_output_data(output_file)

    assert actual_data == expected_data




################################################### Negative Tests #####################################################
def test_no_input_files(setup_output_files):...


def _get_output_data(output_file):
    output_file.flush()
    output_file.seek(0)

    return output_file.read()