import pytest

from s1.parsing import parse_line_with_spec
from s1.records.base import InvalidFieldLength


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
