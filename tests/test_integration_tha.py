from s1.parsers import S1Parser


def test_integration_tha(tha_lines, tha_encounter):
    parser = S1Parser()
    for line in tha_lines:
        parser.feed(line)

    parser.finish()
    records = parser.flush()
    assert len(records) == 1
    assert records[0].as_dict() == tha_encounter
