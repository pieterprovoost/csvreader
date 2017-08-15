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

names = ["id", "basisOfRecord", "occurrenceID", "sex", "lifeStage", "eventID"]
occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quoteChar="\"", indexFields=["eventID"], fieldNames=names)
print occurrence.indexes()

records = occurrence.getLines("eventID", "Cruise68:Station593:EventSorbeSledge9887:Subsample16687")
for r in records:
    print r

#print len(occurrence)
#for line in occurrence:
#    print line
#    break