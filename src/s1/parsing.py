from typing import List

from s1.records import RecordSpec

SEP = "|"


def splat(line: str) -> List[str]:
    """ Single source to split by our separator """
    return line.split(SEP)


def parse_line_with_spec(line: str, spec: RecordSpec) -> dict:
    """ Convert a pipe-separated line into a dictionary

    The basic idea of the S1 format is that it contains pipe-separated lines containing
    fields. The first field, a record id, encodes what we expect the rest of the line
    to look like.

    """
    data_fields = splat(line)
    spec.validate_number_of_fields(len(data_fields))
    record = {}
    static_field_names = ["record_id"] + spec.static_fields
    for field_name, value in zip(static_field_names, data_fields):
        record[field_name] = value

    return record
