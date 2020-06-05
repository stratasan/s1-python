import pytest

from s1.records import RecordSpec, register_record_spec, spec_from_record_id


def test_default_registry():
    """ By instantiating a RecordBase and registering, we should be able
    to read that spec out """

    spec = RecordSpec("something_wild", ["a", "b", "c"])
    register_record_spec(spec)

    assert spec_from_record_id("something_wild") == spec
