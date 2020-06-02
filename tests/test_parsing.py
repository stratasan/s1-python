import pytest

from s1.parsing import parse_line_with_spec, build_repeated_objects
from s1.records.base import InvalidFieldLength, RepeatedBlock


@pytest.mark.parametrize("bad_line", ["1|foo", "1|foo|bar|bat|zoo"])
def test_parsing_invalid_length_no_repeat(bad_line, basic_spec):
    with pytest.raises(InvalidFieldLength):
        parse_line_with_spec(bad_line, basic_spec)


@pytest.mark.parametrize(
    "bad_line", ["1|foo", "1|foo|bar|bat|zoo", "1|foo|bar|bat|zoo|zod|zep"]
)
def test_parsing_invalid_length_repeat_spec(bad_line, repeat_spec):
    with pytest.raises(InvalidFieldLength):
        parse_line_with_spec(bad_line, repeat_spec)


def test_basic_parse(correct_basic_line, basic_spec):
    parsed = parse_line_with_spec(correct_basic_line, basic_spec)
    assert parsed == {"record_id": "1", "a": "foo", "b": "bar", "c": "bat"}


def test_parse_repeat(correct_repeat_line, repeat_spec):
    parsed = parse_line_with_spec(correct_repeat_line, repeat_spec)
    assert parsed == {
        "record_id": "1",
        "a": "1",
        "b": "2",
        "c": "3",
        "repeats": [{"d": "4", "e": "5"}, {"d": "6", "e": "7"}],
    }


def test_incorrect_record_ids(basic_spec):
    """ Should raise when a record_id doesn't match the spec.record_id """
    bad_line = "2|a|b|c"
    assert basic_spec.record_id == "1"
    with pytest.raises(ValueError):
        parse_line_with_spec(bad_line, basic_spec)


def test_build_repeated_objects_basic():
    iterator = ["1", "2", "3", "4"]
    # define a RepeatedBlock of two fields
    block = RepeatedBlock(key_name="something", fields=["a", "b"])
    repeated_objects = build_repeated_objects(iterator, block)
    assert len(repeated_objects) == 2
    assert repeated_objects[0] == {"a": "1", "b": "2"}
    assert repeated_objects[1] == {"a": "3", "b": "4"}


def test_build_repeated_objects_empty_data():
    iterator = []
    # define a RepeatedBlock of two fields
    block = RepeatedBlock(key_name="something", fields=["a", "b"])
    repeated_objects = build_repeated_objects(iterator, block)
    assert len(repeated_objects) == 0
