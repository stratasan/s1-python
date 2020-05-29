from typing import List, Optional
from dataclasses import dataclass

from .registry import register_record_spec_class
from ..parsing import parse_line_with_spec


class InvalidFieldLength(ValueError):
    pass


@dataclass
class RepeatedBlock:
    key_name: str
    fields: List[str]


@dataclass
class BaseRecordSpec:
    record_id: str
    static_fields: List[str]
    repeated_block: Optional[RepeatedBlock] = None

    def __init_subclass__(cls, **kwargs) -> None:
        """ Register subclasses to our record registry

        New to py3.6, this is invoked only in subclasses before __init__ """
        super().__init_subclass__(**kwargs)
        # register_record_spec_class(cls)

    @property
    def size_of_static_fields(self) -> 0:
        """ Number of non-repeating fields """
        return len(self.static_fields)

    @property
    def size_of_repeated_block(self) -> 0:
        """ Number of fields to expect in a single repeated block """
        return len(self.repeated_block.fields) if self.repeated_block else 0

    def validate_number_of_fields(self, n_fields: int) -> None:
        """ The number of fields expected in a line is the length of static
        fields + some multiple of the length of the repeated block.

        There are a couple of bad things to catch:
        * With no repeat block, n_fields is < expected
        * With no repeat block, n_fields is > expected
        * With repeat block, remaining fields don't perfectly fit """
        # we add one to this to account for the record_id
        size_repeated_fields = n_fields - (self.size_of_static_fields + 1)
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

        if (size_repeated_fields % self.size_of_repeated_block) != 0:
            raise InvalidFieldLength(
                "This record contains more repeated fields than cleanly fit into a repeated block"
            )
        #
        return
