import pytest

from s1.parsing import parse_line_with_spec
from s1.records.base import InvalidFieldLength


def test_parsing_invalid_length(basic_spec):
    line = "1|foo"
    with pytest.raises(InvalidFieldLength):
        parse_line_with_spec(line, basic_spec)


# def test_basic_parse(basic_spec):
#     line = "1|foo|bar|bat"
#     parsed = parse_line_with_spec(line, basic_spec)
#     assert parsed == {"a": "foo", "b": "bar", "c": "bat"}
