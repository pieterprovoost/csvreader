import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from csvreader import CSVReader

#names = {"scientificName": 7}
#occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quoteChar="\"", indexFields=["scientificName"], fieldNames=names)
#print occurrence.indexes()
#records = occurrence.getLines("scientificName", "Neomysis integer")
#print records

#names = ["id", "basisOfRecord", "occurrenceID", "sex", "lifeStage", "eventID", "scientificNameID", "scientificName"]
#occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quoteChar="\"", indexFields=["scientificName"], fieldNames=names)
#print occurrence.indexes()
#records = occurrence.getLines("scientificName", "Neomysis integer")
#print records


names = {'eventID': 2, 'decimalLatitude': 10, 'minimumDepthInMeters': 8, 'habitat': 5, 'locality': 7, 'parentEventID': 3, 'modified': 1, 'footprintWKT': 13, 'decimalLongitude': 11, 'maximumDepthInMeters': 9, 'locationID': 6, 'id': 0, 'coordinateUncertaintyInMeters': 12, 'eventDate': 4}
occurrence = CSVReader("data/event2.txt", delimiter="\t", quoteChar=None, indexFields=["eventID", "parentEventID", "id"], fieldNames=names)
print occurrence.indexes()

