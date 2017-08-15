"""This module provides a class to index and query large CSV files."""

import csv
import io
import sys

class CSVReader(object):

    def __init__(self, path, indexFields=None, delimiter="\t", quoteChar="\"", encoding="utf-8", fieldNames=None):

        reload(sys)
        sys.setdefaultencoding("utf8")

        self._path = path
        self._indexFields = indexFields
        self._delimiter = delimiter
        self._quoteChar = quoteChar
        self._encoding = encoding
        self._fieldNames = fieldNames
        self._indexes = {}

        self._index()

    def __str__(self):
        lines = []
        lines.append("-" * len(self._path))
        lines.append(self._path)
        lines.append("-" * len(self._path))
        lines.append("Fields: " + ", ".join(self._headers))
        lines.append("Indexed fields: " + (", ".join(self._indexFields) if self._indexFields is not None else "-"))
        return "\n".join(lines)

    def _expandFieldNames(self, n, names):
        """Expand field names into list of the correct size."""
        result = []
        for i in xrange(n):
            result.append("col_" + str(i))
        if isinstance(names, dict):
            for key, value in names.iteritems():
                if value < n:
                    result[value] = key
        else:
            result[0:min(n, len(names) - 1)] = names
        return result

    def _index(self):
        """Parse the CSV file and create index for the selected fields."""

        # initialize the indexes
        if self._indexFields is not None:
            for indexField in self._indexFields:
                self._indexes[indexField] = {}

        # initialize the row position list
        self._rowPositions = []

        pos = 0
        with open(self._path, "rb") as csvfile:
            for line in csvfile:
                # parse the line using the csv module
                values = list(csv.reader([line.rstrip()], delimiter=self._delimiter, quotechar=self._quoteChar))[0]

                # first line contains the headers
                if pos == 0:
                    # override headers if fieldNames is specified
                    if self._fieldNames is not None:
                        self._headers = self._expandFieldNames(len(values), self._fieldNames)
                    else:
                        self._headers = values
                else:
                    # add position to row positions list
                    self._rowPositions.append(pos)
                    if self._indexFields is not None:
                        for indexField in self._indexFields:
                            if indexField in self._headers:
                                # get the index of the field to be indexed
                                i = self._headers.index(indexField)
                                value = values[i]
                                #  add the value to the index
                                if value not in self._indexes[indexField]:
                                    self._indexes[indexField][value] = [pos]
                                else:
                                    self._indexes[indexField][value].append(pos)

                # increment the position with the length of the line in bytes
                pos = pos + len(line.encode(self._encoding))

    def _getLineByPosition(self, fileStream, pos):
        fileStream.seek(pos, 0)
        line = fileStream.readline().rstrip()
        # parse line using the csv module
        return list(csv.reader([line], delimiter=self._delimiter, quotechar=self._quoteChar))[0]

    def getLine(self, index):
        fileStream = io.open(self._path, mode="r", encoding=self._encoding)
        values = self._getLineByPosition(fileStream, self._rowPositions[index])
        fileStream.close()
        return dict(zip(self._headers, values))

    def getLines(self, field, value):
        if field not in self._indexes:
            raise RuntimeError("Field " + field + " was not indexed")
        if value not in self._indexes[field]:
            return
        """Get all lines for the given field and value as dicts."""
        positions = self._indexes[field][value]

        # open file stream
        fileStream = io.open(self._path, mode="r", encoding=self._encoding)

        for pos in positions:
            values = self._getLineByPosition(fileStream, pos)
            # create dict from the headers and values
            yield dict(zip(self._headers, values))

        fileStream.close()

    def __len__(self):
        return len(self._rowPositions)

    def __iter__(self):
        self._position = 0
        return self

    def next(self):
        if self._position >= len(self._rowPositions):
            raise StopIteration
        else:
            fileStream = io.open(self._path, mode="r", encoding=self._encoding)
            values = self._getLineByPosition(fileStream, self._rowPositions[self._position])
            fileStream.close()
            self._position += 1
            return dict(zip(self._headers, values))

    def indexes(self):
        """Get the indexes."""
        return self._indexes
