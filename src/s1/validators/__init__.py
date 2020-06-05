from s1.exceptions import (
    InvalidS1Format,
    UnknownRecordType,
    InvalidFieldLength,
    InvalidS1Line,
)

from s1.records.registry import spec_from_record_id
from s1.parsing import record_id_from_line, parse_line_with_spec


class S1Validator:
    def validate(self, line: str) -> None:
        try:
            record_id = record_id_from_line(line)
        except ValueError:
            raise InvalidS1Format("Does not contain S1 separator")
        try:
            spec = spec_from_record_id(record_id)
        except KeyError:
            raise UnknownRecordType(
                f"Encountered unknown record id of '{record_id}'"
            )
        try:
            # Tossing away this data, but catching field length errors
            parse_line_with_spec(line, spec)
        except InvalidFieldLength:
            raise InvalidS1Line()
