""" Record specifications for Texas Hospital Association


See https://docs.google.com/document/d/1mp1lG1nkHwiMVZt3ZaClzzKc-bJ0dSNuhi2m04EljP8/ """


from s1.records import RecordSpec, RepeatedBlock, register_record_spec

PROVIDER_ID = "provider_id"
PCN = "patient_control_number"

Header100 = RecordSpec(
    record_id="100",
    static_fields=[
        PROVIDER_ID,
        PCN,
        "type_of_bill",
        "mrn",
        "provider_tax_id",
        "provider_npi",
        "statement_from_date",
        "statement_through_date",
        "date_of_admission",
        "date_of_discharge",
        "patient_age",
        "patient_zip",
        "patient_zip_ext",
        "patient_sex",
        "patient_race",
        "patient_ethnicity",
        "admission_type",
        "admission_source",
        "patient_discharge_status",
        "hour_of_admission",
        "hour_of_discharge",
    ],
    denotes_new_set=True,
)

Procedures200 = RecordSpec(
    record_id="200",
    static_fields=[
        PROVIDER_ID,
        PCN,
        "principal_procedure_code",
        "principal_procedure_date",
        "principal_procedure_physician_npi",
    ],
    repeated_block=RepeatedBlock(
        key_name="other_procedures",
        fields=["procedure_code", "procedure_date", "procedure_physician_npi"],
    ),
)

Diagnoses300 = RecordSpec(
    record_id="300",
    static_fields=[
        PROVIDER_ID,
        PCN,
        "diagnosis_version_qualifier",
        "admitting_diagnosis_code",
        "principal_diagnosis_code",
        "principal_diagnosis_code_poa",
        "principal_external_code",
        "principal_external_code_poa",
        "external_code_2",
        "external_code_2_poa",
        "external_code_3",
        "external_code_3_poa",
        "external_code_4",
        "external_code_4_poa",
        "external_code_5",
        "external_code_5_poa",
        "external_code_6",
        "external_code_6_poa",
        "external_code_7",
        "external_code_7_poa",
        "external_code_8",
        "external_code_8_poa",
        "external_code_9",
        "external_code_9_poa",
        "external_code_10",
        "external_code_10_poa",
        "external_code_11",
        "external_code_11_poa",
        "reason_for_visit_1",
        "reason_for_visit_2",
        "reason_for_visit_3",
    ],
    repeated_block=RepeatedBlock(
        key_name="other_diagnoses", fields=["code", "poa"]
    ),
)

RevenueCodes400 = RecordSpec(
    record_id="400",
    static_fields=[PROVIDER_ID, PCN],
    repeated_block=RepeatedBlock(
        key_name="revenue_codes",
        fields=[
            "revenue_code",
            "rate",
            "unit_measurement_code",
            "units",
            "date_of_service",
            "charges",
            "noncovered_charges",
            "hcpcs_code",
            "hcpcs_modifier_1",
            "hcpcs_modifier_2",
            "hcpcs_modifier_3",
            "hcpcs_modifier_4",
        ],
    ),
)

RevenueCodes500 = RecordSpec(
    record_id="500",
    static_fields=[PROVIDER_ID, PCN],
    repeated_block=RepeatedBlock(
        key_name="payers",
        fields=["designation", "name", "id", "patient_relationship_to_insured"],
    ),
)

Supplemental600 = RecordSpec(
    record_id="600",
    static_fields=[
        PROVIDER_ID,
        PCN,
        "patient_first_name",
        "patient_middle_initial",
        "patient_last_name",
        "patient_address_1",
        "patient_address_2",
        "patient_city",
        "patient_state_abbreviation",
        "patient_country_code",
        "patient_county_name",
        "patient_date_of_birth",
        "patient_ssn",
    ],
)

Physician700 = RecordSpec(
    record_id="700",
    static_fields=[PROVIDER_ID, PCN],
    repeated_block=RepeatedBlock(
        key_name="physicians",
        fields=[
            "role",
            "npi",
            "state_id",
            "first_name",
            "middle_initial",
            "last_name",
        ],
    ),
)

OccurrencesAndValues800 = RecordSpec(
    record_id="800",
    static_fields=[
        PROVIDER_ID,
        PCN,
        "condition_code_1",
        "condition_code_2",
        "condition_code_3",
        "condition_code_4",
        "condition_code_5",
        "condition_code_6",
        "condition_code_7",
        "condition_code_8",
        "condition_code_9",
        "condition_code_10",
        "condition_code_11",
        "condition_code_12",
        "occurrence_code_1",
        "occurrence_code_date_1",
        "occurrence_code_2",
        "occurrence_code_date_2",
        "occurrence_code_3",
        "occurrence_code_date_3",
        "occurrence_code_4",
        "occurrence_code_date_4",
        "occurrence_code_5",
        "occurrence_code_date_5",
        "occurrence_code_6",
        "occurrence_code_date_6",
        "occurrence_code_7",
        "occurrence_code_date_7",
        "occurrence_code_8",
        "occurrence_code_date_8",
        "occurrence_code_9",
        "occurrence_code_date_9",
        "occurrence_code_10",
        "occurrence_code_date_10",
        "occurrence_code_11",
        "occurrence_code_date_11",
        "occurrence_code_12",
        "occurrence_code_date_12",
        "occurrence_code_13",
        "occurrence_code_date_13",
        "occurrence_code_14",
        "occurrence_code_date_14",
        "occurrence_code_15",
        "occurrence_code_date_15",
        "occurrence_code_16",
        "occurrence_code_date_16",
        "occurrence_code_17",
        "occurrence_code_date_17",
        "occurrence_code_18",
        "occurrence_code_date_18",
        "occurrence_code_19",
        "occurrence_code_date_19",
        "occurrence_code_20",
        "occurrence_code_date_20",
        "occurrence_code_21",
        "occurrence_code_date_21",
        "occurrence_code_22",
        "occurrence_code_date_22",
        "occurrence_code_23",
        "occurrence_code_date_23",
        "occurrence_code_24",
        "occurrence_code_date_24",
        "occurrence_span_code_1",
        "occurrence_span_code_date_range_1",
        "occurrence_span_code_2",
        "occurrence_span_code_date_range_2",
        "occurrence_span_code_3",
        "occurrence_span_code_date_range_3",
        "occurrence_span_code_4",
        "occurrence_span_code_date_range_4",
        "occurrence_span_code_5",
        "occurrence_span_code_date_range_5",
        "occurrence_span_code_6",
        "occurrence_span_code_date_range_6",
        "occurrence_span_code_7",
        "occurrence_span_code_date_range_7",
        "occurrence_span_code_8",
        "occurrence_span_code_date_range_8",
        "occurrence_span_code_9",
        "occurrence_span_code_date_range_9",
        "occurrence_span_code_10",
        "occurrence_span_code_date_range_10",
        "occurrence_span_code_11",
        "occurrence_span_code_date_range_11",
        "occurrence_span_code_12",
        "occurrence_span_code_date_range_12",
        "occurrence_span_code_13",
        "occurrence_span_code_date_range_13",
        "occurrence_span_code_14",
        "occurrence_span_code_date_range_14",
        "occurrence_span_code_15",
        "occurrence_span_code_date_range_15",
        "occurrence_span_code_16",
        "occurrence_span_code_date_range_16",
        "occurrence_span_code_17",
        "occurrence_span_code_date_range_17",
        "occurrence_span_code_18",
        "occurrence_span_code_date_range_18",
        "occurrence_span_code_19",
        "occurrence_span_code_date_range_19",
        "occurrence_span_code_20",
        "occurrence_span_code_date_range_20",
        "occurrence_span_code_21",
        "occurrence_span_code_date_range_21",
        "occurrence_span_code_22",
        "occurrence_span_code_date_range_22",
        "occurrence_span_code_23",
        "occurrence_span_code_date_range_23",
        "occurrence_span_code_24",
        "occurrence_span_code_date_range_24",
        "value_code_1",
        "value_code_amount_1",
        "value_code_2",
        "value_code_amount_2",
        "value_code_3",
        "value_code_amount_3",
        "value_code_4",
        "value_code_amount_4",
        "value_code_5",
        "value_code_amount_5",
        "value_code_6",
        "value_code_amount_6",
        "value_code_7",
        "value_code_amount_7",
        "value_code_8",
        "value_code_amount_8",
        "value_code_9",
        "value_code_amount_9",
        "value_code_10",
        "value_code_amount_10",
        "value_code_11",
        "value_code_amount_11",
        "value_code_12",
        "value_code_amount_12",
        "value_code_13",
        "value_code_amount_13",
        "value_code_14",
        "value_code_amount_14",
        "value_code_15",
        "value_code_amount_15",
        "value_code_16",
        "value_code_amount_16",
        "value_code_17",
        "value_code_amount_17",
        "value_code_18",
        "value_code_amount_18",
        "value_code_19",
        "value_code_amount_19",
        "value_code_20",
        "value_code_amount_20",
        "value_code_21",
        "value_code_amount_21",
        "value_code_22",
        "value_code_amount_22",
        "value_code_23",
        "value_code_amount_23",
        "value_code_24",
        "value_code_amount_24",
    ],
)


# These will get registered in the specifications module
all_specs = [
    Header100,
    Procedures200,
    Diagnoses300,
    RevenueCodes400,
    RevenueCodes500,
    Supplemental600,
    Physician700,
    OccurrencesAndValues800,
]
