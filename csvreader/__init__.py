"""This module provides a class to index and query large CSV files."""

import csv
import io
import sys

class CSVReader(object):

    def __init__(self, path, indexFields=["id"], delimiter="\t", quoteChar="\"", encoding="utf-8", fieldNames=None):

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

    def _index(self):
        """Parse the CSV file and create index for the selected fields."""
        for indexField in self._indexFields:
            # Initialize the indexes.
            self._indexes[indexField] = {}

        pos = 0
        with open(self._path, "rb") as csvfile:
            for line in csvfile:
                # Parse the line using the csv module.
                values = list(csv.reader([line.rstrip()], delimiter=self._delimiter, quotechar=self._quoteChar))[0]

                if pos == 0:
                    # First line contains the headers.
                    self._headers = values
                else:
                    for indexField in self._indexFields:
                        if indexField in self._headers:
                            # Get the index of the field to be indexed.
                            i = self._headers.index(indexField)
                            value = values[i]
                            # Add the value to the index.
                            if value not in self._indexes[indexField]:
                                self._indexes[indexField][value] = [pos]
                            else:
                                self._indexes[indexField][value].append(pos)

                # Increment the position with the length of the line in bytes.
                pos = pos + len(line.encode(self._encoding))

    def getLines(self, field, value):
        """Get all lines for the given field and value as dicts."""
        positions = self._indexes[field][value]
        results = []

        # Open file stream.
        fileStream = io.open(self._path, mode="r", encoding=self._encoding)

        for pos in positions:
            fileStream.seek(pos, 0)
            line = fileStream.readline().rstrip()
            # Parse line using the csv module.
            values = list(csv.reader([line], delimiter=self._delimiter, quotechar=self._quoteChar))[0]
            # Create dict from the headers and values.
            results.append(dict(zip(self._headers, values)))

        fileStream.close()
        return results

    def indexes(self):
        """Get the indexes."""
        return self._indexes