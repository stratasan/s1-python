# First-party specifications


Here we're registering "first-party" or Stratasan-defined RecordSpecs.

Any particular line out of an S1 file contains is a |-delimited string. Splitting by the |,
we get fields embedded within the string:

1. The first field denotes the record id.
2. All subsequent fields will be parsed to the specification matching that record id.

So if we say a line should should use the record id (synonymous with "type") of `1` and this
line contains two static (non-repeating) fields (let's call them "a" and "b"), a line
could look like `1|a_field|b_field`. The correct corresponding RecordSpec is

```python
from s1.records import RecordSpec

Record1 = RecordSpec(record_id="1", static_fields=["a", "b"])
```

Rather than have to keep track of all these record spec instances, there's a simple registry
system, used as such:

```python
from s1.records import register_record_spec, spec_from_record_id

register_record_spec(Record1)


# later, potentially in another file

spec = spec_from_record_id("1")
# this RecordSpec can be used to parse a line w/ that record id
```
