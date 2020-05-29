from typing import List

from dataclasses import dataclass, field

from s1.records.base import BaseRecordSpec, RepeatedBlock

from pytest import fixture


@fixture
def basic_spec():
    return BaseRecordSpec(record_id="1", static_fields=["a", "b", "c"])


@fixture
def repeat_spec():
    block = RepeatedBlock(key_name="stuff", fields=["d", "e"])
    return BaseRecordSpec(
        record_id="1", static_fields=["a", "b", "c"], repeated_block=block
    )
