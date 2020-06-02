from itertools import islice, zip_longest
from typing import Dict, Iterator, List, Union

from s1.records import RecordSpec, RepeatedBlock, RecordType

SEP = "|"


def splat(line: str) -> List[str]:
    """ Single source to split by our separator """
    return line.split(SEP)


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks

    https://docs.python.org/3.8/library/itertools.html
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def build_repeated_objects(
    repeated_fields: Iterator[str], block: RepeatedBlock
) -> List[Dict[str, str]]:
    repeated_objects = []
    for grouped in grouper(repeated_fields, block.num_fields):
        new_object: Dict[str, str] = dict(
            (field, value) for field, value in zip(block.fields, grouped)
        )
        repeated_objects.append(new_object)
    return repeated_objects


def parse_line_with_spec(line: str, spec: RecordSpec) -> RecordType:
    """ Convert a pipe-separated line into a dictionary

    The basic idea of the S1 format is that it contains pipe-separated lines containing
    fields. The first field, a record id, encodes what we expect the rest of the line
    to look like.

    """
    data_fields = splat(line)
    spec.validate_number_of_fields(len(data_fields))
    if data_fields[0] != spec.record_id:
        raise ValueError()
    record: RecordType = {}
    static_field_names = ["record_id"] + spec.static_fields
    for field_name, value in zip(static_field_names, data_fields):
        record[field_name] = value
    if spec.repeated_block:
        # Take the rest of the repeated fields, which we know cleanly
        # fall into the number of fields in the repeated block
        repeated_fields = islice(data_fields, spec.num_static_fields, None)
        record[spec.repeated_block.key_name] = build_repeated_objects(
            repeated_fields, spec.repeated_block
        )

    return record
