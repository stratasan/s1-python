from typing import List, Tuple

from s1.exceptions import UnknownRecordType
from s1.parsing import parse_line_with_spec, record_id_from_line
from s1.records import RecordSet, RecordSpec, RecordType
from s1.records.registry import spec_from_record_id


class S1Parser:
    class BatchSizeExceeded(Exception):
        pass

    def __init__(self, batch_size=1000):
        self.batch_size = batch_size
        self.buffer: List[RecordSet] = []
        self.current_encounter: RecordSet = RecordSet()
        self._buffer_size: int = 0
        self._total_lines: int = 0
        self._total_sets: int = 0

    @property
    def buffer_size(self) -> int:
        return self._buffer_size

    @buffer_size.setter
    def buffer_size(self, size: int) -> None:
        self._buffer_size = size

    @property
    def total_lines(self):
        return self._total_lines

    @total_lines.setter
    def total_lines(self, total: int) -> None:
        self._total_lines = total

    @property
    def total_sets(self) -> int:
        return self._total_sets

    @total_sets.setter
    def total_sets(self, total: int) -> None:
        self._total_sets = total

    def handle_new_line(self, line: str) -> Tuple[RecordSpec, RecordType]:
        record_id = record_id_from_line(line)
        try:
            spec = spec_from_record_id(record_id)
        except KeyError:
            raise UnknownRecordType()
        record = parse_line_with_spec(line, spec)
        self.total_lines += 1
        return spec, record

    def finish_current_encounter(self) -> None:
        # Catch an edge on the first feed or right after a flush
        if self.current_encounter.is_empty:
            return

        self.buffer.append(self.current_encounter)
        self.buffer_size += 1
        self.total_sets += 1
        self.current_encounter = RecordSet()

    def attach_record(self, record: RecordType) -> None:
        self.current_encounter.add_record(record)

    def feed(self, line: str) -> None:
        spec, record = self.handle_new_line(line)
        if spec.denotes_new_set:
            self.finish_current_encounter()
        self.attach_record(record)
        self.check_batch_size()

    def check_batch_size(self) -> None:
        if self.buffer_size >= self.batch_size:
            raise self.BatchSizeExceeded()

    def finish(self) -> None:
        self.finish_current_encounter()

    def flush(self) -> List[RecordSet]:
        flushed = self.buffer.copy()
        self.buffer.clear()
        self.buffer_size = 0
        return flushed
