from typing import List

from dataclasses import dataclass, field

from s1.parsers import S1Parser
from s1.records import RecordSpec, RepeatedBlock, register_record_spec

from pytest import fixture


@fixture
def basic_spec():
    spec = RecordSpec(record_id="1", static_fields=["a", "b", "c"])
    register_record_spec(spec)
    return spec


@fixture
def correct_basic_line():
    """ Matching the spec above """
    return "1|foo|bar|bat"


@fixture
def repeat_spec():
    block = RepeatedBlock(key_name="repeats", fields=["d", "e"])
    spec = RecordSpec(
        record_id="2", static_fields=["a", "b", "c"], repeated_block=block
    )
    register_record_spec(spec)
    return spec


@fixture
def correct_repeat_line():
    """ Matches repeat spec above """
    return "2|1|2|3|4|5|6|7"


@fixture
def parser_specs():
    register_record_spec(
        RecordSpec(
            record_id="1", denotes_new_set=True, static_fields=["a", "b"]
        )
    )
    register_record_spec(RecordSpec(record_id="2", static_fields=["c", "d"]))
    return None


@fixture
def good_lines():
    return ["1|1|1", "2|2|2"]


@fixture
def parser():
    return S1Parser()
