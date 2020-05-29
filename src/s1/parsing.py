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
    fields = splat(line)
    spec.validate_number_of_fields(len(fields))

    return {}
