from itertools import islice, zip_longest
from typing import Dict, Iterator, List, Union

from s1.records import RecordSpec, RepeatedBlock, RecordType

SEP = "|"


def splat(line: str) -> List[str]:
    """ Single source to split by our separator """
    return line.split(SEP)


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks

    See recipes at https://docs.python.org/3.8/library/itertools.html
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def build_repeated_objects(
    repeated_fields: Iterator[str], block: RepeatedBlock
) -> List[Dict[str, str]]:
    """ Build a list of dicts with fields given by the RepeatedBlock

    S1 lines can contain a variable number of fields. If a particular spec
    contains a RepeatedBlock, then that block is assumed to repeat after the
    static fields of the RecordSpec. This function groups these fields
    (of unknown length) into a chunk equal to the number of fields in the repeated block
    and converts them into a dictionary, accumulating those dictionaries """
    repeated_objects = []
    # grouper cuts the incoming iterator of strings into a chunk based
    # on the number of fields in the repeated blockg
    for grouped in grouper(repeated_fields, block.num_fields):
        # the dict function can take 2-tuples, using the first item as the key and second
        # as value, which zip-with-two-arguments perfectly fulfills
        new_object: Dict[str, str] = dict(zip(block.fields, grouped))
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
    record.update(dict(zip(spec.all_static_field_names, data_fields)))
    if spec.repeated_block:
        # Take the rest of the repeated fields, which we know cleanly
        # fall into the number of fields in the repeated block
        repeated_fields = islice(data_fields, spec.num_static_fields, None)
        record[spec.repeated_block.key_name] = build_repeated_objects(
            repeated_fields, spec.repeated_block
        )

    return record
