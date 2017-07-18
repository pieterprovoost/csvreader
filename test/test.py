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

    def testDev(self):
        occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quoteChar="\"", indexFields=["scientificName"])

        print occurrence.indexes()

        records = occurrence.getLines("scientificName", "Neomysis integer")
        print records

if __name__ == "__main__":
    unittest.main()