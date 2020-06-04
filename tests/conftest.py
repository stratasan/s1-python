from typing import List

from dataclasses import dataclass, field

from s1.parsers import S1Parser
from s1.records import RecordSpec, RepeatedBlock, register_record_spec

from pytest import fixture


@fixture
def basic_spec():
    spec = RecordSpec(record_id="1", static_fields=["a", "b", "c"])
    register_record_spec(spec)
    return spec


@fixture
def correct_basic_line():
    """ Matching the spec above """
    return "1|foo|bar|bat"


@fixture
def repeat_spec():
    block = RepeatedBlock(key_name="repeats", fields=["d", "e"])
    spec = RecordSpec(
        record_id="2", static_fields=["a", "b", "c"], repeated_block=block
    )
    register_record_spec(spec)
    return spec


@fixture
def correct_repeat_line():
    """ Matches repeat spec above """
    return "2|1|2|3|4|5|6|7"


@fixture
def parser_specs():
    register_record_spec(
        RecordSpec(
            record_id="1", denotes_new_set=True, static_fields=["a", "b"]
        )
    )
    register_record_spec(RecordSpec(record_id="2", static_fields=["c", "d"]))
    return None


@fixture
def good_lines():
    return ["1|1|1", "2|2|2"]


@fixture
def parser():
    return S1Parser()


@fixture
def tha_lines():
    return [
        "100|123456|PCN|0111|MRN|TAXID|1234567891|01012020|01012020|01012020|01012020|34|37027|0000|M|4|2|3|2|01|1200|1200",
        "200|123456|PCN|CODE1|20200101|1234567890|CODE2|20200101|1234567890|CODE3|01012020|1234567890|CODE4|01012020|1234567890",
        "300|123456|PCN|0|ADMITCODE|PRINCODE|Y|ECODE1|Y|ECODE2|Y|ECODE3|Y|ECODE4|Y|ECODE5|Y|ECODE6|Y|ECODE7|Y|ECODE8|Y|ECODE9|Y|ECODE10|Y|ECODE11|Y|RCODE1|RCODE2|RCODE3|OTHERCODE1|Y|OTHERCODE2|Y|OTHERCODE3|Y|OTHERCODE4|Y|OTHERCODE5|Y",
        "400|123456|PCN|0123|1.0|UN|1|01012020|1.0|0.0|HCPCS|HCPCSMOD1|HCPCSMOD2|HCPCSMOD3|HCPCSMOD4|0124|2.0|UN|1|01012020|2.0|0.0|HCPCS|HCPCSMOD1|HCPCSMOD2|HCPCSMOD3|HCPCSMOD4|0001|3.0|UN|1|01012020|3.0|0.0|HCPCS3|HCPCSMOD1|HCPCSMOD2|HCPCSMOD3|HCPCSMOD4",
        "500|123456|PCN|primary|CIGNA|CI|18",
        "600|123456|PCN|John|M|Doe|123 Main Street|Address 2|City|ST|US|COUNTY|01011990|999999999",
        "700|123456|PCN|ATT|1234567890|STATE_ID|Jane|M|Doe",
        "800|123456|PCN|COND|COND|COND|COND|COND|COND|COND|COND|COND|COND|COND|COND|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCC|01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|OCCSPAN|01012020-01012020|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1|VAL|1",
    ]


@fixture
def tha_encounter():
    return {
        "100": {
            "record_id": "100",
            "provider_id": "123456",
            "patient_control_number": "PCN",
            "type_of_bill": "0111",
            "mrn": "MRN",
            "provider_tax_id": "TAXID",
            "provider_npi": "1234567891",
            "statement_from_date": "01012020",
            "statement_through_date": "01012020",
            "date_of_admission": "01012020",
            "date_of_discharge": "01012020",
            "patient_age": "34",
            "patient_zip": "37027",
            "patient_zip_ext": "0000",
            "patient_sex": "M",
            "patient_race": "4",
            "patient_ethnicity": "2",
            "admission_type": "3",
            "admission_source": "2",
            "patient_discharge_status": "01",
            "hour_of_admission": "1200",
            "hour_of_discharge": "1200",
        },
        "200": {
            "record_id": "200",
            "provider_id": "123456",
            "patient_control_number": "PCN",
            "principal_procedure_code": "CODE1",
            "principal_procedure_date": "20200101",
            "principal_procedure_physician_npi": "1234567890",
            "other_procedures": [
                {
                    "procedure_code": "CODE2",
                    "procedure_date": "20200101",
                    "procedure_physician_npi": "1234567890",
                },
                {
                    "procedure_code": "CODE3",
                    "procedure_date": "01012020",
                    "procedure_physician_npi": "1234567890",
                },
                {
                    "procedure_code": "CODE4",
                    "procedure_date": "01012020",
                    "procedure_physician_npi": "1234567890",
                },
            ],
        },
        "300": {
            "record_id": "300",
            "provider_id": "123456",
            "patient_control_number": "PCN",
            "diagnosis_version_qualifier": "0",
            "admitting_diagnosis_code": "ADMITCODE",
            "principal_diagnosis_code": "PRINCODE",
            "principal_diagnosis_code_poa": "Y",
            "principal_external_code": "ECODE1",
            "principal_external_code_poa": "Y",
            "external_code_2": "ECODE2",
            "external_code_2_poa": "Y",
            "external_code_3": "ECODE3",
            "external_code_3_poa": "Y",
            "external_code_4": "ECODE4",
            "external_code_4_poa": "Y",
            "external_code_5": "ECODE5",
            "external_code_5_poa": "Y",
            "external_code_6": "ECODE6",
            "external_code_6_poa": "Y",
            "external_code_7": "ECODE7",
            "external_code_7_poa": "Y",
            "external_code_8": "ECODE8",
            "external_code_8_poa": "Y",
            "external_code_9": "ECODE9",
            "external_code_9_poa": "Y",
            "external_code_10": "ECODE10",
            "external_code_10_poa": "Y",
            "external_code_11": "ECODE11",
            "external_code_11_poa": "Y",
            "reason_for_visit_1": "RCODE1",
            "reason_for_visit_2": "RCODE2",
            "reason_for_visit_3": "RCODE3",
            "other_diagnoses": [
                {"code": "OTHERCODE1", "poa": "Y"},
                {"code": "OTHERCODE2", "poa": "Y"},
                {"code": "OTHERCODE3", "poa": "Y"},
                {"code": "OTHERCODE4", "poa": "Y"},
                {"code": "OTHERCODE5", "poa": "Y"},
            ],
        },
        "400": {
            "record_id": "400",
            "provider_id": "123456",
            "patient_control_number": "PCN",
            "revenue_codes": [
                {
                    "revenue_code": "0123",
                    "rate": "1.0",
                    "unit_measurement_code": "UN",
                    "units": "1",
                    "date_of_service": "01012020",
                    "charges": "1.0",
                    "noncovered_charges": "0.0",
                    "hcpcs_code": "HCPCS",
                    "hcpcs_modifier_1": "HCPCSMOD1",
                    "hcpcs_modifier_2": "HCPCSMOD2",
                    "hcpcs_modifier_3": "HCPCSMOD3",
                    "hcpcs_modifier_4": "HCPCSMOD4",
                },
                {
                    "revenue_code": "0124",
                    "rate": "2.0",
                    "unit_measurement_code": "UN",
                    "units": "1",
                    "date_of_service": "01012020",
                    "charges": "2.0",
                    "noncovered_charges": "0.0",
                    "hcpcs_code": "HCPCS",
                    "hcpcs_modifier_1": "HCPCSMOD1",
                    "hcpcs_modifier_2": "HCPCSMOD2",
                    "hcpcs_modifier_3": "HCPCSMOD3",
                    "hcpcs_modifier_4": "HCPCSMOD4",
                },
                {
                    "revenue_code": "0001",
                    "rate": "3.0",
                    "unit_measurement_code": "UN",
                    "units": "1",
                    "date_of_service": "01012020",
                    "charges": "3.0",
                    "noncovered_charges": "0.0",
                    "hcpcs_code": "HCPCS3",
                    "hcpcs_modifier_1": "HCPCSMOD1",
                    "hcpcs_modifier_2": "HCPCSMOD2",
                    "hcpcs_modifier_3": "HCPCSMOD3",
                    "hcpcs_modifier_4": "HCPCSMOD4",
                },
            ],
        },
        "500": {
            "record_id": "500",
            "provider_id": "123456",
            "patient_control_number": "PCN",
            "payers": [
                {
                    "designation": "primary",
                    "name": "CIGNA",
                    "id": "CI",
                    "patient_relationship_to_insured": "18",
                }
            ],
        },
        "600": {
            "record_id": "600",
            "provider_id": "123456",
            "patient_control_number": "PCN",
            "patient_first_name": "John",
            "patient_middle_initial": "M",
            "patient_last_name": "Doe",
            "patient_address_1": "123 Main Street",
            "patient_address_2": "Address 2",
            "patient_city": "City",
            "patient_state_abbreviation": "ST",
            "patient_country_code": "US",
            "patient_county_name": "COUNTY",
            "patient_date_of_birth": "01011990",
            "patient_ssn": "999999999",
        },
        "700": {
            "record_id": "700",
            "provider_id": "123456",
            "patient_control_number": "PCN",
            "physicians": [
                {
                    "role": "ATT",
                    "npi": "1234567890",
                    "state_id": "STATE_ID",
                    "first_name": "Jane",
                    "middle_initial": "M",
                    "last_name": "Doe",
                }
            ],
        },
        "800": {
            "record_id": "800",
            "provider_id": "123456",
            "patient_control_number": "PCN",
            "condition_code_1": "COND",
            "condition_code_2": "COND",
            "condition_code_3": "COND",
            "condition_code_4": "COND",
            "condition_code_5": "COND",
            "condition_code_6": "COND",
            "condition_code_7": "COND",
            "condition_code_8": "COND",
            "condition_code_9": "COND",
            "condition_code_10": "COND",
            "condition_code_11": "COND",
            "condition_code_12": "COND",
            "occurrence_code_1": "OCC",
            "occurrence_code_date_1": "01012020",
            "occurrence_code_2": "OCC",
            "occurrence_code_date_2": "01012020",
            "occurrence_code_3": "OCC",
            "occurrence_code_date_3": "01012020",
            "occurrence_code_4": "OCC",
            "occurrence_code_date_4": "01012020",
            "occurrence_code_5": "OCC",
            "occurrence_code_date_5": "01012020",
            "occurrence_code_6": "OCC",
            "occurrence_code_date_6": "01012020",
            "occurrence_code_7": "OCC",
            "occurrence_code_date_7": "01012020",
            "occurrence_code_8": "OCC",
            "occurrence_code_date_8": "01012020",
            "occurrence_code_9": "OCC",
            "occurrence_code_date_9": "01012020",
            "occurrence_code_10": "OCC",
            "occurrence_code_date_10": "01012020",
            "occurrence_code_11": "OCC",
            "occurrence_code_date_11": "01012020",
            "occurrence_code_12": "OCC",
            "occurrence_code_date_12": "01012020",
            "occurrence_code_13": "OCC",
            "occurrence_code_date_13": "01012020",
            "occurrence_code_14": "OCC",
            "occurrence_code_date_14": "01012020",
            "occurrence_code_15": "OCC",
            "occurrence_code_date_15": "01012020",
            "occurrence_code_16": "OCC",
            "occurrence_code_date_16": "01012020",
            "occurrence_code_17": "OCC",
            "occurrence_code_date_17": "01012020",
            "occurrence_code_18": "OCC",
            "occurrence_code_date_18": "01012020",
            "occurrence_code_19": "OCC",
            "occurrence_code_date_19": "01012020",
            "occurrence_code_20": "OCC",
            "occurrence_code_date_20": "01012020",
            "occurrence_code_21": "OCC",
            "occurrence_code_date_21": "01012020",
            "occurrence_code_22": "OCC",
            "occurrence_code_date_22": "01012020",
            "occurrence_code_23": "OCC",
            "occurrence_code_date_23": "01012020",
            "occurrence_code_24": "OCC",
            "occurrence_code_date_24": "01012020",
            "occurrence_span_code_1": "OCCSPAN",
            "occurrence_span_code_date_range_1": "01012020-01012020",
            "occurrence_span_code_2": "OCCSPAN",
            "occurrence_span_code_date_range_2": "01012020-01012020",
            "occurrence_span_code_3": "OCCSPAN",
            "occurrence_span_code_date_range_3": "01012020-01012020",
            "occurrence_span_code_4": "OCCSPAN",
            "occurrence_span_code_date_range_4": "01012020-01012020",
            "occurrence_span_code_5": "OCCSPAN",
            "occurrence_span_code_date_range_5": "01012020-01012020",
            "occurrence_span_code_6": "OCCSPAN",
            "occurrence_span_code_date_range_6": "01012020-01012020",
            "occurrence_span_code_7": "OCCSPAN",
            "occurrence_span_code_date_range_7": "01012020-01012020",
            "occurrence_span_code_8": "OCCSPAN",
            "occurrence_span_code_date_range_8": "01012020-01012020",
            "occurrence_span_code_9": "OCCSPAN",
            "occurrence_span_code_date_range_9": "01012020-01012020",
            "occurrence_span_code_10": "OCCSPAN",
            "occurrence_span_code_date_range_10": "01012020-01012020",
            "occurrence_span_code_11": "OCCSPAN",
            "occurrence_span_code_date_range_11": "01012020-01012020",
            "occurrence_span_code_12": "OCCSPAN",
            "occurrence_span_code_date_range_12": "01012020-01012020",
            "occurrence_span_code_13": "OCCSPAN",
            "occurrence_span_code_date_range_13": "01012020-01012020",
            "occurrence_span_code_14": "OCCSPAN",
            "occurrence_span_code_date_range_14": "01012020-01012020",
            "occurrence_span_code_15": "OCCSPAN",
            "occurrence_span_code_date_range_15": "01012020-01012020",
            "occurrence_span_code_16": "OCCSPAN",
            "occurrence_span_code_date_range_16": "01012020-01012020",
            "occurrence_span_code_17": "OCCSPAN",
            "occurrence_span_code_date_range_17": "01012020-01012020",
            "occurrence_span_code_18": "OCCSPAN",
            "occurrence_span_code_date_range_18": "01012020-01012020",
            "occurrence_span_code_19": "OCCSPAN",
            "occurrence_span_code_date_range_19": "01012020-01012020",
            "occurrence_span_code_20": "OCCSPAN",
            "occurrence_span_code_date_range_20": "01012020-01012020",
            "occurrence_span_code_21": "OCCSPAN",
            "occurrence_span_code_date_range_21": "01012020-01012020",
            "occurrence_span_code_22": "OCCSPAN",
            "occurrence_span_code_date_range_22": "01012020-01012020",
            "occurrence_span_code_23": "OCCSPAN",
            "occurrence_span_code_date_range_23": "01012020-01012020",
            "occurrence_span_code_24": "OCCSPAN",
            "occurrence_span_code_date_range_24": "01012020-01012020",
            "value_code_1": "VAL",
            "value_code_amount_1": "1",
            "value_code_2": "VAL",
            "value_code_amount_2": "1",
            "value_code_3": "VAL",
            "value_code_amount_3": "1",
            "value_code_4": "VAL",
            "value_code_amount_4": "1",
            "value_code_5": "VAL",
            "value_code_amount_5": "1",
            "value_code_6": "VAL",
            "value_code_amount_6": "1",
            "value_code_7": "VAL",
            "value_code_amount_7": "1",
            "value_code_8": "VAL",
            "value_code_amount_8": "1",
            "value_code_9": "VAL",
            "value_code_amount_9": "1",
            "value_code_10": "VAL",
            "value_code_amount_10": "1",
            "value_code_11": "VAL",
            "value_code_amount_11": "1",
            "value_code_12": "VAL",
            "value_code_amount_12": "1",
            "value_code_13": "VAL",
            "value_code_amount_13": "1",
            "value_code_14": "VAL",
            "value_code_amount_14": "1",
            "value_code_15": "VAL",
            "value_code_amount_15": "1",
            "value_code_16": "VAL",
            "value_code_amount_16": "1",
            "value_code_17": "VAL",
            "value_code_amount_17": "1",
            "value_code_18": "VAL",
            "value_code_amount_18": "1",
            "value_code_19": "VAL",
            "value_code_amount_19": "1",
            "value_code_20": "VAL",
            "value_code_amount_20": "1",
            "value_code_21": "VAL",
            "value_code_amount_21": "1",
            "value_code_22": "VAL",
            "value_code_amount_22": "1",
            "value_code_23": "VAL",
            "value_code_amount_23": "1",
            "value_code_24": "VAL",
            "value_code_amount_24": "1",
        },
    }
