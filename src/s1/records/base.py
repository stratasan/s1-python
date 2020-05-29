from typing import List, Optional
from dataclasses import dataclass, field

from .registry import register_record_spec


class InvalidFieldLength(ValueError):
    pass


@dataclass
class RepeatedBlock:
    key_name: str
    fields: List[str]


@dataclass
class RecordSpec:
    record_id: str
    static_fields: List[str]
    repeated_block: Optional[RepeatedBlock] = None
    num_static_fields: int = field(init=False)
    num_repeat_fields: int = field(init=False)

    def __post_init__(self):
        self.num_static_fields = len(self.static_fields)
        self.num_repeat_fields = (
            len(self.repeated_block.fields) if self.repeated_block else 0
        )
        register_record_spec(self)

    def validate_number_of_fields(self, n_fields: int) -> None:
        """ The number of fields expected in a line is the length of static
        fields + some multiple of the length of the repeated block.

        There are a couple of bad things to catch:
        * With no repeat block, n_fields is < expected
        * With no repeat block, n_fields is > expected
        * With repeat block, remaining fields don't perfectly fit """
        # we add one to this to account for the record_id
        size_repeated_fields = n_fields - (self.num_static_fields + 1)
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
