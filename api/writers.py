from csv import DictWriter


class DataWriter:
    '''Base class for all future data writers'''

    def write_row(self, row):
        raise NotImplementedError(
            "Please implement this method in subclass!"
        )


class CSVWriter(DataWriter):
    def __init__(self, file, fields):
        self.csv_dict_writer = DictWriter(
            file, delimiter=',', fieldnames=fields
        )
        self.csv_dict_writer.writeheader()

    def write_row(self, row):
        self.csv_dict_writer.writerow(row)


class JSONWriter(DataWriter):
    def __init__(self, file, fields):...

    def write_row(self, row):...


class XMLWriter(DataWriter):
    def __init__(self, file, fields):...

    def write_row(self, row):...
