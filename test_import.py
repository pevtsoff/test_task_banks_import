import os
import pytest
import glob
from main import main
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

    with open(output_file_path, 'w+') as output_file:
        with open(error_file_path, 'w+') as error_file:
            csv_dict_writer = DictWriter(
                output_file, delimiter=',', fieldnames=output_fields
            )
            csv_dict_writer.writeheader()
            yield output_file, csv_dict_writer, error_file



@pytest.mark.parametrize('expected_output', [*expected_output.items()])
def test_valid_import(setup_output_files, expected_output):
    output_file = setup_output_files[0]
    parse_csv_file(expected_output[0], setup_output_files[1], setup_output_files[2])
    expected_data = expected_output[1]
    actual_data = _get_output_data(output_file)

    assert actual_data == expected_data


def _get_output_data(output_file):
    output_file.flush()
    output_file.seek(0)

    return output_file.read()