# importing these
from s1.records import register_record_spec

from .tha import all_specs as all_tha_specs

for spec in all_tha_specs:
    register_record_spec(spec)
