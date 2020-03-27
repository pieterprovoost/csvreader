"""This module provides a class to index and query large CSV files."""

import csv
import io
import sys


class CSVReader(object):

    def __init__(self, path, index_fields=None, delimiter="\t", quote_char="\"", encoding="utf-8", field_names=None, skip_blank=True):

        self._path = path
        self._index_fields = index_fields
        self._delimiter = delimiter
        self._quote_char = quote_char
        self._encoding = encoding
        self._field_names = field_names
        self._skip_blank = skip_blank
        self._indexes = {}

        self._index()

    def __str__(self):
        lines = []
        lines.append("-" * len(self._path))
        lines.append(self._path)
        lines.append("-" * len(self._path))
        lines.append("Fields: " + ", ".join(self._headers))
        lines.append("Indexed fields: " + (", ".join(self._index_fields) if self._index_fields is not None else "-"))
        return "\n".join(lines)

    def _expand_field_names(self, n, names):
        """Expand field names into list of the correct size."""
        result = []
        for i in range(n):
            result.append("col_" + str(i))
        if isinstance(names, dict):
            for key, value in names.items():
                if value < n:
                    result[value] = key
        else:
            result[0:min(n, len(names) - 1)] = names
        return result

    def _index(self):
        """Parse the CSV file and create index for the selected fields."""

        # initialize the indexes
        if self._index_fields is not None:
            for index_field in self._index_fields:
                self._indexes[index_field] = {}

        # initialize the row position list
        self._row_positions = []

        pos = 0
        with open(self._path, "r") as csvfile:
            for line in csvfile:

                if self._skip_blank is False or not line.isspace():

                    # parse the line using the csv module
                    values = list(csv.reader([line.rstrip("\r\n ")], delimiter=self._delimiter, quotechar=self._quote_char))[0]

                    # first line contains the headers
                    if pos == 0:
                        # override headers if fieldNames is specified
                        if self._field_names is not None:
                            self._headers = self._expand_field_names(len(values), self._field_names)
                        else:
                            self._headers = values
                    else:
                        # add position to row positions list
                        self._row_positions.append(pos)
                        if self._index_fields is not None:
                            for index_field in self._index_fields:
                                if index_field in self._headers:
                                    # get the index of the field to be indexed
                                    i = self._headers.index(index_field)
                                    value = values[i]
                                    #  add the value to the index
                                    if value not in self._indexes[index_field]:
                                        self._indexes[index_field][value] = [pos]
                                    else:
                                        self._indexes[index_field][value].append(pos)

                # increment the position with the length of the line in bytes
                pos = pos + len(line.encode(self._encoding))

    def _get_line_by_position(self, file_stream, pos):
        file_stream.seek(pos, 0)
        line = file_stream.readline().rstrip('\r\n ')
        # parse line using the csv module
        return list(csv.reader([line], delimiter=self._delimiter, quotechar=self._quote_char))[0]

    def get_line(self, index):
        file_stream = io.open(self._path, mode="r", encoding=self._encoding)
        values = self._get_line_by_position(file_stream, self._row_positions[index])
        file_stream.close()
        return dict(zip(self._headers, values))

    def get_lines(self, field, value):
        if field not in self._indexes:
            raise RuntimeError("Field " + field + " was not indexed")
        if value not in self._indexes[field]:
            return
        """Get all lines for the given field and value as dicts."""
        positions = self._indexes[field][value]

        # open file stream
        file_stream = io.open(self._path, mode="r", encoding=self._encoding)

        for pos in positions:
            values = self._get_line_by_position(file_stream, pos)
            # create dict from the headers and values
            yield dict(zip(self._headers, values))

        file_stream.close()

    def __len__(self):
        return len(self._row_positions)

    def __iter__(self):
        self._position = 0
        return self

    def __next__(self):
        if self._position >= len(self._row_positions):
            raise StopIteration
        else:
            file_stream = io.open(self._path, mode="r", encoding=self._encoding)
            values = self._get_line_by_position(file_stream, self._row_positions[self._position])
            file_stream.close()
            self._position += 1
            return dict(zip(self._headers, values))

    def next(self):
        return self.__next__()

    def indexes(self):
        """Get the indexes."""
        return self._indexes
