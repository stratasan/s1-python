# s1-python

This python package implements parsing S1 files in python. The S1
encodes data following rather generic rules:

1. Fields in each line are pipe (`|`) delimited.
2. The first field, or record id, denotes how the rest of the line should be parsed.
3. Lines are compromised of the record id, static fields (those that don't
  repeat), and a variable number of repeating blocks. The repeating blocks are
  optional and whether they exist at all depends on the record id.
4. While iterating over lines, lines with specific record IDs denote new entities.

The purpose of the S1 is to encode complex data relationships with a minimum
amount of pomp and circumstance. The S1 doesn't imply field formats or lengths,
as that should be left to downstream processes. The major use case is to encode
entities with various 1:M relationships beneath them.

The S1 does not handle M:M or deeply-nested relationships. Consider using other formats as necessary for your work.

This package ships with parsers and validators to transform data encoded in the
S1 format into more structured data. This package structures the data based on
RecordSpecs, short for Record Specification. We have included our own
"first-party" record specifications, but there are hooks to register other
RecordSpecs.

## Record Specifications

A Record Specification consists of:

* A record_id, a string
* static fields, an ordered list of field names
* optionally, a "RepeatedBlock", which itself has a "key name" and ordered list
  of fields
* a boolean denoting whether it implies the beginning of a new entity

For example, let's take an example where we want to capture information about a
person and the books they own.

We'll say we want to capture the first and last name of the person along with a
book title, author and whether they've read it or not.

A "person" record can look like:

```
1|FirstName|LastName
```

We're saying that the "1" RecordType has two fields, first name and last name.

A "book" record is a bit more complex, due to the 1:M relationship implied
between a person and their books. Since we want to capture the name, author, and
whether it's been read by the owner for each book, that's our repeated block.

So a valid book line could look like:

```
2|BookName|BookAuthor|0|Book2Name|Book2Author|1
```

The first field, `2` is the record id we'll use for "Book" entities. There are
two books encoded in this line, though the format defines no limit. The 0 or 1
is simply a boolean placeholder, the S1 format does not imply anything about
interpretation of encoded data.

## Implementing these structures using s1-python

Implementing the above system, we can write these record specs.

```python
from s1.records import RecordSpec, RepeatedBlock, register_record_spec

Person = RecordSpec(
    record_id="1", denotes_new_set=True, static_fields=["first_name", "last_name"],
)
Book = RecordSpec(
    record_id="2",
    static_fields=[],
    repeated_block=RepeatedBlock(key_name="books", fields=["name", "author", "read"]),
)
register_record_spec(Person)
register_record_spec(Book)
```

s1-python ships with a simple registry to separate the specification of
RecordSpecs from the need to somehow get them to code that actually parses lines.

Having defined and registered these record specs, you can then:

```python
from s1.records import spec_from_record_id
from s1.parsing import parse_line_with_spec, record_id_from_line

person_line = "1|John|Doe"
book_line = "2|Harry Potter and the Sorcerers Stone|JK Rowling|1|Harry Potter and the Chamber of Secrets|JK Rowling|0"

person_spec = spec_from_record_id(record_id_from_line(person_line))
person = parse_line_with_spec(person_line, person_spec))
# {"record_id": "1", "first_name": "John", "last_name": "Doe"}
book_spec = spec_from_record_id(record_id_from_line(book_line))
book = parse_line_with_spec(book_line, book_spec)
# {"record_id": "2", "books": [{"name": "Harry...", "author": "JK Rowling", "read": "1"},...]}
```

## Parser API

While the above is doable, it's onerous and missing one specific
piece, how to reconcile new entities during the parsing of lines?

This functionality is wrapped into the highest-level of the API,
the `S1Parser`. Example usage:

```python
from typing import List
from s1 import S1Parser, RecordSet

parser = S1Parser(batch_size=1000)
for line in data_lines:  # bring your own data
    try:
        parser.feed(line)
    except parser.BatchSizeExceeded:
        records: List[RecordSet] = parser.flush()
        data = [record.as_dict() for record in records]
        # write that data somewhere
# Because there may be RecordSets left in the internal buffer
# finish and flush
parser.finish()
records = parser.flush()
# again, do something with the data: serialize to a file, write to DB, etc
```

Assuming that all `RecordSpec` instances have been defined and
registered, the `S1Parser` API removes any need of worrying about
them, as it's all handled internally.

Given unbounded datasets, the `BatchSizeExceeded` exception allows
callers to break incoming records into chunks, potentially translating a
single S1 file into multiple output files. In practice, tuning the `batch_size`
parameter can help control the size of output files.
