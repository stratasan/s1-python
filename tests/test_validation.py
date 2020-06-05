import pytest

from s1.exceptions import InvalidS1Format, UnknownRecordType, InvalidS1Line


def test_validator_throws_invalid_format(validator):
    not_an_s1_line = "some,other,separator"

    with pytest.raises(InvalidS1Format):
        validator.validate(not_an_s1_line)


def test_validator_throws_unknown(validator):
    unknown_line = "nopenopenope|a|b"

    with pytest.raises(UnknownRecordType):
        validator.validate(unknown_line)


def test_validator_throws_invalid_line(validator):
    """ We already have 1-records defined as having three fields """
    invalid_line = "1|a|b|c|d"  # because longer fields

    with pytest.raises(InvalidS1Line):
        validator.validate(invalid_line)
