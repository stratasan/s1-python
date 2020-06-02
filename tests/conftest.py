from typing import List

from dataclasses import dataclass, field

from s1.records.base import RecordSpec, RepeatedBlock

from pytest import fixture


@fixture
def basic_spec():
    return RecordSpec(record_id="1", static_fields=["a", "b", "c"])


@fixture
def correct_basic_line():
    """ Matching the spec above """
    return "1|foo|bar|bat"


@fixture
def repeat_spec():
    block = RepeatedBlock(key_name="repeats", fields=["d", "e"])
    return RecordSpec(
        record_id="1", static_fields=["a", "b", "c"], repeated_block=block
    )


@fixture
def correct_repeat_line():
    """ Matches repeat spec above """
    return "1|1|2|3|4|5|6|7"
