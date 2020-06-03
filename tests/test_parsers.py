import pytest


def test_parser_normal_feed_flush(parser, good_lines, parser_specs):
    for line in good_lines:
        parser.feed(line)

    parser.finish()
    assert parser.buffer_size == 1
    flushed = parser.flush()
    assert len(flushed) == 1
    encounter = flushed[0]
    assert len(encounter.records) == 2


def test_parser_raises_batch_size_exceeded(parser, good_lines, parser_specs):
    """ Given a small batch size, we should check the parser raises """
    # when we set the batch size small
    parser.batch_size = 1

    # and feed a full encounter
    for line in good_lines:
        parser.feed(line)

    # We should raise after submitting a new record that denotes a new encounter
    with pytest.raises(parser.BatchSizeExceeded):
        parser.feed("1|1|1")
