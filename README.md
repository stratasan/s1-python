# s1-python

Stratasan's python parser for the S1 file format. This parser does not validate datatypes and will capture all elements as strings. Type and data validation should be applied downstream from this library.

## Installation

`$ pip install s1-python`

## Some vocabulary

* encounter: a point of care for a patient. Typically, but not always, encounters contain multiple revenue codes, diagnoses, procedures and payers. There may be specific patient information including PII for the patient as well.
* line translation: the process of converting a raw, |-delimited string into a structured object. Because there are not headers in the S1, translating connects data elements to their specific fields by use of position.
* record type: every line in a S1 begins with a record type element, typically an integer. This guides how the line should be translated.


The `s1` package provides two parsers, `S1Validator` and `S1Parser`.

## S1Validator

This parser validates lines but does not accumulate them. This can be used to validate files before attempting to fully parse & accumulate them into encounters. Exceptions are raised for unknown record types or lines that don't translate correctly.

```python
from s1 import S1Validator
from s1.exceptions import UnknownRecordType, RecordTranslationError

validator = S1Validator()

with open("data.s1", "r") as fobj:
    for line in fobj:
        try:
            validator.validate(line)
        except UnknownRecordType:
            # do something with line
            pass
        except RecordTranslationError:
            # do something with line
            pass
```

## S1Parser

Feed this parser data line-by-line. During this process, the parser translates lines and accumulates the objects into encounter objects. After a configurable amount of fully-parsed encounters, this parser will raise a `BatchSizeExceeded` exception. Clients may use this exception to call `.flush()` which returns parsed encounter objects. Note that flushing within `BatchSizeExceeded` is the best way to ensure all lines from an encounter has been read.

```python
from s1 import S1Parser
from s1.classes import Encounter

parser = S1Parser(batch_size=1000)

def serialize(records):
    return json.dumps({"records": [record.as_dict() for record in records]})

# somehow iterate over your data

for line in data:
    try:
        parser.feed(line)
    except parser.BatchSizeExceeded:
        records: List[Encounter] = parser.flush()
        # serialize and do something w/ results
        serialize(records)

parser.finish()
# Remaining records not flushed during the loop
other_records = parser.flush()
serialize(other_records)

report = parser.report
# {"line_count": int, "encounter_count": int, ...}
```

`S1Parser` may be called without a `batch_size` argument, though memory-usage
will be unbounded and may become large for sizable datasets. Generally, we recommend the streaming approach to write translated data out in separate chunks.


```python
...
parser = S1Parser()

for line in data:  # hopefully this is small, or a big computer
    parser.feed(line)

records = parser.flush()
report = parser.report
```
