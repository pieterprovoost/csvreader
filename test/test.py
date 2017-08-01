import unittest
from csvreader import CSVReader

class TestCSVReader(unittest.TestCase):

    def testRead(self):
        occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quoteChar="\"", indexFields=["id", "eventID"])

        indexes = occurrence.indexes()
        self.assertTrue("id" in indexes)
        self.assertTrue("eventID" in indexes)
        self.assertTrue("Cruise68:Station593:EventSorbeSledge9887:Subsample16687" in indexes["eventID"])
        self.assertTrue(len(indexes["eventID"]["Cruise68:Station593:EventSorbeSledge9887:Subsample16687"]) == 39)

        records = occurrence.getLines("id", "Cruise68:Station565:EventSorbeSledge9781:Subsample17409")
        self.assertTrue(len(records) > 0)
        self.assertTrue(records[0]["eventID"] == "Cruise68:Station565:EventSorbeSledge9781:Subsample17409")
        self.assertTrue(records[0]["scientificNameID"] == "urn:lsid:marinespecies.org:taxname:131495")

        records = occurrence.getLines("eventID", "Cruise68:Station622:EventSorbeSledge10018:Subsample15224")
        self.assertTrue(records[21]["eventID"] == "Cruise68:Station622:EventSorbeSledge10018:Subsample15224")
        self.assertTrue(records[21]["scientificNameID"] == "urn:lsid:marinespecies.org:taxname:120144")

    def testFieldNamesDict(self):
        names = {"scientificName": 7}
        occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quoteChar="\"", indexFields=["scientificName"], fieldNames=names)
        records = occurrence.getLines("scientificName", "Neomysis integer")
        self.assertTrue(records[0]["scientificName"] == "Neomysis integer")
        self.assertTrue(records[0]["col_6"] == "urn:lsid:marinespecies.org:taxname:120136")

    def testFieldNamesList(self):
        names = ["id", "basisOfRecord", "occurrenceID", "sex", "lifeStage", "eventID"]
        occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quoteChar="\"", indexFields=["eventID"], fieldNames=names)
        records = occurrence.getLines("eventID", "Cruise68:Station593:EventSorbeSledge9887:Subsample16687")
        self.assertTrue(records[0]["eventID"] == "Cruise68:Station593:EventSorbeSledge9887:Subsample16687")
        self.assertTrue(records[0]["occurrenceID"] == "Ugenthyperbenthos51168")
        self.assertTrue(records[0]["col_6"] == "Sagitta elegans")

    def testNotIndexed(self):
        occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quoteChar="\"")
        with self.assertRaises(RuntimeError):
            records = occurrence.getLines("eventID", "Cruise68:Station593:EventSorbeSledge9887:Subsample16687")

    def testStr(self):
        self.assertTrue(isinstance(str(CSVReader("data/occurrence.txt", delimiter="\t", quoteChar="\"", indexFields=["scientificName"])), basestring))
        self.assertTrue(isinstance(str(CSVReader("data/occurrence.txt", delimiter="\t", quoteChar="\"")), basestring))

if __name__ == "__main__":
    unittest.main()