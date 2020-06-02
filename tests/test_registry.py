from s1.records import RecordSpec
from s1.records.registry import spec_from_record_id


def test_default_registry():
    """ By instantiating a RecordBase, we should be able
    to read that spec out """

    spec = RecordSpec("something_wild", ["a", "b", "c"])

    assert spec_from_record_id("something_wild") == spec
