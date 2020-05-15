# s1-python
Stratasan's python parser for the S1 file format


## Some vocabulary

* encounter: a point of care for a patient. Typically, but not always, encounters contain multiple revenue codes, diagnoses, procedures and payers. There may be specific patient information including PII for the patient as well.
* line translation: the process of converting a raw, |-delimited string into a structured object. Because there are not headers in the S1, this connects data elements to their specific fields by use of position.
* record type: every line in a S1 begins with a record type element, typically an integer. This guides how the line should be translated.


The `s1` package provides two parsers, `S1Validator` and `S1StreamingParser`.

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

Feed this parser data line-by-line. During this process, the parser translates lines and accumulates the objects into encounter objects. After a configurable amount of fully-parsed encounters, this parser will raise a `BatchSizeExceeded` exception. Clients may use this exception to call `.flush()` which returns parsed
