# s1-python

This python package implements parsing S1 files in python. The S1 encodes data in the
in the following rather generic rules:

1. Fields in each line are pipe (`|`) delimited.
2. The first field, or record id, denotes how the rest of the line should be parsed.
3. Lines are compromised of the record id, static fields (those that don't repeat), and a
  variable number of repeating blocks. The repeating blocks are optional and whether they
  exist at all depends on the record id.
4. While iterating over lines, lines with specific record IDs denote new entities.

The purpose of the S1 is to encode complex data relationships with a minimum amount of
pomp and circumstance. The S1 doesn't imply field formats or lengths, as that should be left to
downstream processes.

This package ships with parsers and validators to transform data encoded in the S1 format
into more structured data. This package structures the data based on RecordSpecs, short for
Record Specification. This package includes our own "first-party" record specifications, but there are hooks to register other "RecordSpecs".

## Record Specifications

A Record Specification consists of:

* A record_id, a string
* static fields, an ordered list of field names
* optionally, a "RepeatedBlock", which itself has a "key name" and ordered list of fields
* a boolean denoting whether it implies the beginning of a new entity.

For example, let's take an example where we want to capture information about a person
and how many books they own.

We'll say we want to capture the first and last name of the person along with a book title, author and whether they've read it or not.

A "person" record can look like:

```
1|FirstName|LastName
```

We're saying that the "1" RecordType has two fields, first name and last name.

A "book" record is a bit more complex, due to the 1:M relationship implied between a person
and their books. Since we want to capture the name, author, and whether it's been read by the owner for each book, that's our repeated block.

So a valid line could look like:

```
2|BookName|BookAuthor|0|Book2Name|Book2Author|1
```

The first field, `2` is the record id we'll use for "Book" entities. There are two books encoded
in this line, though there could be quite a few. The 0 or 1 is simply a boolean placeholder, the
S1 format does not imply anything about interpretation of encoded data.

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

s1-python ships with a simple registry to separate the specification of Record Types from the
need to somehow get them to code that actually parses lines.

Having defined and registered these record specs, you can then:

```python
from s1.records import spec_from_record_id
from s1.parsing import parse_line_with_spec, record_id_from_line

person_line = "1|John|Doe"
book_line = "2|Harry Potter and the Sorcerers Stone|JK Rowling|1|Harry Potter and the Chamber of Secrets|JK Rowling|0"

person = parse_line_with_spec(person_line, spec_from_record_id(record_id_from_line(person_line))))
book = parse_line_with_spec(book_line, spec_from_record_id(record_id_from_line(book_line))))
# person is {"record_id": "1", "first_name": "John", "last_name": "Doe"}
# book is {"record_id": "2", "books": [{"name": "Harry...", "author": "JK Rowling", "read": "1"},...]}
```
