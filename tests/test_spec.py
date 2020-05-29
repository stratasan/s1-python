import pytest

from s1.records.base import InvalidFieldLength, RecordSpec


def test_validate_number_of_fields_correct(basic_spec: RecordSpec) -> None:
    """ Our basic_spec contains 3 static fields + 1 record_id, this should not raise"""
    basic_spec.validate_number_of_fields(4)


def test_validate_number_of_fields_short(basic_spec: RecordSpec) -> None:
    """ If our basic_spec has 3 fields, and we validate short, raise """
    with pytest.raises(InvalidFieldLength):
        basic_spec.validate_number_of_fields(2)


def test_validate_number_of_fields_long_no_repeat(
    basic_spec: RecordSpec,
) -> None:
    with pytest.raises(InvalidFieldLength):
        basic_spec.validate_number_of_fields(5)


def test_validate_number_of_fields_repeat_spec_no_actual_repeats(
    repeat_spec: RecordSpec,
) -> None:
    """ The repeat spec is (1) + 3 * 2X """
    repeat_spec.validate_number_of_fields(4)


def test_validate_number_of_fields_repeat_spec_some_repeats(
    repeat_spec: RecordSpec
) -> None:
    """ The repeat spec is (1) + 3 * 2X """
    repeat_spec.validate_number_of_fields(6)


def test_validate_number_of_fields_repeat_spec_wrong_repeats(
    repeat_spec: RecordSpec,
) -> None:
    """ The repeat spec is (1) + 3 * 2X """
    with pytest.raises(InvalidFieldLength):
        repeat_spec.validate_number_of_fields(7)
