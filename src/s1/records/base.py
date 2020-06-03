from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field

from .registry import register_record_spec


class InvalidFieldLength(ValueError):
    pass


@dataclass
class RepeatedBlock:
    key_name: str
    fields: List[str]

    def __post_init__(self):
        self.num_fields = len(self.fields)


# Records are dictionaries, which str keys, that point to str values or in Lists of Dicts
# with str values and str keys
RecordType = Dict[str, Union[str, List[Dict[str, str]]]]


@dataclass
class RecordSpec:
    record_id: str
    static_fields: List[str]
    denotes_new_set: bool = False
    repeated_block: Optional[RepeatedBlock] = None
    num_static_fields: int = field(init=False)
    num_repeat_fields: int = field(init=False)

    def __post_init__(self):
        # static fields are what's defined plus the spot for record_id
        self.num_static_fields = len(self.static_fields) + 1
        self.num_repeat_fields = (
            len(self.repeated_block.fields) if self.repeated_block else 0
        )
        self.all_static_field_names = ["record_id"] + self.static_fields
        register_record_spec(self)

    def validate_number_of_fields(self, n_fields: int) -> None:
        """ The number of fields expected in a line is the length of static
        fields + some multiple of the length of the repeated block.

        There are a couple of bad things to catch:
        * With no repeat block, n_fields is < expected
        * With no repeat block, n_fields is > expected
        * With repeat block, remaining fields don't perfectly fit """
        size_repeated_fields = n_fields - (self.num_static_fields)
        # The number of repeated fields could be less than zero, that's bad
        if size_repeated_fields < 0:
            raise InvalidFieldLength(
                "This record encodes more static fields than given"
            )
        # Perfect fit into static fields, which is fine whether there's a repeat block or not
        if size_repeated_fields == 0 and not self.repeated_block:
            return

        if size_repeated_fields > 0 and not self.repeated_block:
            raise InvalidFieldLength(
                "More fields given than fit into static fields w/o repeated block"
            )

        if (size_repeated_fields % self.num_repeat_fields) != 0:
            raise InvalidFieldLength(
                "This record contains more repeated fields than cleanly fit into a repeated block"
            )

        return


@dataclass
class Encounter:
    """ Encounters capture a contiguous set of records """

    records: List[RecordType] = field(default_factory=list)

    @property
    def is_empty(self):
        return len(self.records) == 0

    def add_record(self, record: RecordType) -> None:
        self.records.append(record)

    def as_dict(self) -> Dict[str, RecordType]:
        serialized = {}
        for record in self.records:
            serialized[record["record_id"]] = record
        return serialized
