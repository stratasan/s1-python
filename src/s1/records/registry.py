import collections
from logging import getLogger
from typing import Dict

from s1.records import RecordSpec

logger = getLogger(__name__)


class RecordRegistry(dict):
    pass


default_registry: Dict[str, RecordSpec] = RecordRegistry()


def register_record_spec(spec: RecordSpec, registry=default_registry):
    logger.debug(f"registering spec at id:{spec.record_id}")
    registry[spec.record_id] = spec


def spec_from_record_id(
    record_id: str, registry=default_registry
) -> RecordSpec:
    spec: RecordSpec = registry[record_id]
    return spec
