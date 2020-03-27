# csvreader

Indexes and queries large CSV files.

## Usage
### Indexing

```python
from csvreader import CSVReader
occurrence = CSVReader("data/occurrence.txt", delimiter="\t", quote_char="\"", index_fields=["scientificName"])
print occurrence.indexes()
```

```json
{
  "scientificName": {
    "Gammaropsis species 1": [447521, 469879],
    "Nebaliacea sp.": [359201],
    ...
```

### Querying

```python
for record in occurrence.get_lines("scientificName", "Neomysis integer"):
    print record
```

```json
[
  {
    "eventID": "Cruise66:Station570:EventSorbeSledge9801:Subsample15202",
    "scientificNameID": "urn:lsid:marinespecies.org:taxname:120136",
    "occurrenceID": "Ugenthyperbenthos49454",
    "basisOfRecord": "HumanObservation",
    "lifeStage": "Juvenile",
    "sex": "Unknown",
    "scientificName": "Neomysis integer",
    "id": "Cruise66:Station570:EventSorbeSledge9801:Subsample15202"
  },
  {
    "eventID": "Cruise66:Station577:EventSorbeSledge9808:Subsample17110",
    "scientificNameID": "urn:lsid:marinespecies.org:taxname:120136",
    "occurrenceID": "Ugenthyperbenthos89117",
    "basisOfRecord": "HumanObservation",
    "lifeStage": "Adult, empty",
    "sex": "female",
    "scientificName": "Neomysis integer",
    "id": "Cruise66:Station577:EventSorbeSledge9808:Subsample17110"
  },
  ...
```
