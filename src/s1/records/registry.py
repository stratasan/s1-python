import collections
from logging import getLogger

logger = getLogger(__name__)


class RecordRegistry(dict):
    pass


default_registry = RecordRegistry()


def register_record_spec(spec, registry=default_registry):
    logger.debug(f"registering spec at id:{spec.record_id}")
    registry[spec.record_id] = spec


def spec_from_record_id(record_id, registry=default_registry):
    return registry[record_id]
