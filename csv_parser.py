import csv
import _io

from default_logger import logger
from writers import DataWriter
from dateutil.parser import parse
from csv import DictReader, DictWriter
from typing import Tuple

############################################### Parse Helpers ##########################################################
import config_params


def date_parser(date: str) -> str:
    return parse(date).date().isoformat()


def parse_cents(cents: str) -> str:
    return '{:.2f}'.format(float(cents)/100)[1:]


def get_output_field_names():
    output_fields = []

    for key, parsing_rules in parsing_map.items():
        if parsing_rules['out_field']:
            output_fields.append(key)

    return output_fields

# Main parsing for a cell level
parsing_map = {
    'date': {
        'single_column': ['timestamp', 'date', 'date_readable'],
        'parser': date_parser, 'out_field': True
    },

    'transaction_type': {
        'single_column': ['type', 'transaction'],
        'parser': str, 'out_field': True
    },

    'amount': {
        'single_column': ['amount', 'amounts'],
        'parser': str, 'out_field': True
    },

    'amount_int': {
        'single_column': ['euro'],
        'parser': str, 'out_field': False
    },

    'amount_dec': {
        'single_column': ['cents'],
        'parser': parse_cents,
        'out_field': False
    },

    'from': {
        'single_column': ['from'],
        'parser': str, 'out_field': True
    },

    'to': {
        'single_column': ['to'],
        'parser': str, 'out_field': True
    },
}

# Columns aggregation on row level
composite_columns = {
  # This columns map means that during csv input file reading, we need to
  # add amount_int + amount_dec. This is done the simplest way and can be easily
  # extended to amount_int.operation([colum1, column2 etc]) so that we can aggregate more
  # than two columns

  'amount_int' : {
      'operand_column': 'amount_dec',
      'operation': '+',
      'output_field_name': 'amount'
  }

}


output_fields = get_output_field_names()

############################################## Main Parser Methods #####################################################

def parse_csv_file(input_file_path: str, writer: DataWriter , error_writer: _io.TextIOWrapper):
    with open(input_file_path, 'r', encoding=config_params.INPUT_ENCODING) as input_file:
        _parse_csv_file(input_file, writer, error_writer)


def _parse_csv_file(csv_file: csv.DictReader, writer: DataWriter, error_writer: _io.TextIOWrapper):
    csv_dict_reader = DictReader(csv_file)

    for row in csv_dict_reader:
        try:
            meta_out_row = {}

            for cell in row.items():
                out_field, parsing_properties = get_parser_map(cell)
                parsed_cell = parsing_properties['parser'](cell[1])
                meta_out_row[out_field] = parsed_cell

            out_row = aggregate_fields(meta_out_row)
            logger.debug(f'Processed this row: {row} --> output_row={out_row}')
            writer.write_row(out_row)

        except Exception as e:
            # this exception handling allows us to complete the parsing of all files
            # and to remember those lines/cells that cause exceptions
            logger.exception(f'Error occured {e}')
            error_writer.write(
                f'Cell "{cell}" in row: "{row}" in file: "{csv_file}" caused exception: "{e}"\n'
            )


def aggregate_fields(meta_out_row: dict) -> dict:
    out_row = {}
    fields_to_delete = []

    for field in meta_out_row.keys():
        cc = composite_columns.get(field)

        if cc and parsing_map[cc['output_field_name']]['out_field']:
            # evaluation for the dynamic operation like "+" defined in composite_columns
            out_row[cc['output_field_name']] = eval(
                f"{meta_out_row[field]} {cc['operation']} {meta_out_row[cc['operand_column']]}"
            )
            fields_to_delete.append(field)

        elif field in output_fields:
            # elif parsing_map[field]['out_field']:
            out_row[field] = meta_out_row[field]

    return out_row


def get_parser_map(cell: str) -> Tuple[str, dict]:

    for out_field, parsing_properties in parsing_map.items():

        if cell[0] in parsing_properties['single_column']:
            return out_field, parsing_properties

    else:
        return None, None
