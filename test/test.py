import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from csvreader import CSVReader


class TestCSVReader(unittest.TestCase):

    def test_read(self):
        occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quote_char="\"", index_fields=["id", "eventID"])

        indexes = occurrence.indexes()
        self.assertTrue("id" in indexes)
        self.assertTrue("eventID" in indexes)
        self.assertTrue("Cruise68:Station593:EventSorbeSledge9887:Subsample16687" in indexes["eventID"])
        self.assertTrue(len(indexes["eventID"]["Cruise68:Station593:EventSorbeSledge9887:Subsample16687"]) == 39)

        records = list(occurrence.get_lines("id", "Cruise68:Station565:EventSorbeSledge9781:Subsample17409"))
        self.assertTrue(len(records) > 0)
        self.assertTrue(records[0]["eventID"] == "Cruise68:Station565:EventSorbeSledge9781:Subsample17409")
        self.assertTrue(records[0]["scientificNameID"] == "urn:lsid:marinespecies.org:taxname:131495")

        records = list(occurrence.get_lines("eventID", "Cruise68:Station622:EventSorbeSledge10018:Subsample15224"))
        self.assertTrue(records[21]["eventID"] == "Cruise68:Station622:EventSorbeSledge10018:Subsample15224")
        self.assertTrue(records[21]["scientificNameID"] == "urn:lsid:marinespecies.org:taxname:120144")

    def test_field_names_dict(self):
        names = {"scientificName": 7}
        occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quote_char="\"", index_fields=["scientificName"], field_names=names)
        records = list(occurrence.get_lines("scientificName", "Neomysis integer"))
        self.assertTrue(records[0]["scientificName"] == "Neomysis integer")
        self.assertTrue(records[0]["col_6"] == "urn:lsid:marinespecies.org:taxname:120136")

    def test_field_names_list(self):
        names = ["id", "basisOfRecord", "occurrenceID", "sex", "lifeStage", "eventID"]
        occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quote_char="\"", index_fields=["eventID"], field_names=names)
        records = list(occurrence.get_lines("eventID", "Cruise68:Station593:EventSorbeSledge9887:Subsample16687"))
        self.assertTrue(records[0]["eventID"] == "Cruise68:Station593:EventSorbeSledge9887:Subsample16687")
        self.assertTrue(records[0]["occurrenceID"] == "Ugenthyperbenthos51168")
        self.assertTrue(records[0]["col_6"] == "Sagitta elegans")

    def test_not_indexed(self):
        occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quote_char="\"")
        with self.assertRaises(RuntimeError):
            records = list(occurrence.get_lines("eventID", "Cruise68:Station593:EventSorbeSledge9887:Subsample16687"))

    def test_str(self):
        self.assertTrue(isinstance(str(CSVReader("data/occurrence.txt", delimiter="\t", quote_char="\"", index_fields=["scientificName"])), str))
        self.assertTrue(isinstance(str(CSVReader("data/occurrence.txt", delimiter="\t", quote_char="\"")), str))

    def test_get_line(self):
        occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quote_char="\"")
        record = occurrence.get_line(0)
        self.assertTrue(record["occurrenceID"] == "Ugenthyperbenthos45979")
        record = occurrence.get_line(5)
        self.assertTrue(record["occurrenceID"] == "Ugenthyperbenthos95454")

    def test_iterator(self):
        occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quote_char="\"")
        for line in occurrence:
            self.assertTrue(line["occurrenceID"] == "Ugenthyperbenthos45979")
            break

    def test_len(self):
        occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quote_char="\"")
        self.assertTrue(len(occurrence) == 8434)

    def test_skip_blank(self):
        occurrence = CSVReader("data/occurrence_blanklines.txt", delimiter="\t", quote_char="\"", index_fields=["institutionCode"], skip_blank=False)
        self.assertTrue("" in occurrence.indexes()["institutionCode"])
        occurrence = CSVReader("data/occurrence_blanklines.txt", delimiter="\t", quote_char="\"", index_fields=["institutionCode"], skip_blank=True)
        self.assertFalse("" in occurrence.indexes()["institutionCode"])

if __name__ == "__main__":
    unittest.main()