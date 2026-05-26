{{ config(materialized='table') }}

WITH raw_pivoted AS (
    SELECT
        source_file,
        -- 1. Employee Identity & Info
        MAX(CASE WHEN entity_type = 'EmployeeName_FirstName' THEN raw_value END) AS employee_first_name,
        MAX(CASE WHEN entity_type = 'EmployeeName_LastName' THEN raw_value END) AS employee_last_name,
        MAX(CASE WHEN entity_type = 'SSN' THEN raw_value END) AS employee_ssn,
        
        -- 2. Employee Address
        MAX(CASE WHEN entity_type = 'EmployeeAddress_StreetAddressOrPostalBox' THEN raw_value END) AS employee_street,
        MAX(CASE WHEN entity_type = 'EmployeeAddress_City' THEN raw_value END) AS employee_city,
        MAX(CASE WHEN entity_type = 'EmployeeAddress_State' THEN raw_value END) AS employee_state,

        -- 3. Calculate Identity-Specific Confidence Score (with NULL safety)
        (
            (COALESCE(MAX(CASE WHEN entity_type = 'EmployeeName_FirstName' THEN confidence END), 0) +
             COALESCE(MAX(CASE WHEN entity_type = 'EmployeeName_LastName' THEN confidence END), 0) +
             COALESCE(MAX(CASE WHEN entity_type = 'SSN' THEN confidence END), 0) +
             COALESCE(MAX(CASE WHEN entity_type = 'EmployeeAddress_StreetAddressOrPostalBox' THEN confidence END), 0) +
             COALESCE(MAX(CASE WHEN entity_type = 'EmployeeAddress_City' THEN confidence END), 0) +
             COALESCE(MAX(CASE WHEN entity_type = 'EmployeeAddress_State' THEN confidence END), 0)) / 6
        ) AS identity_confidence_score,

        MAX(extraction_timestamp) AS extraction_ts
    FROM {{ source('tax_pipeline_db', 'bronze_tax_data') }}
    GROUP BY 1
)

SELECT
    *,
    -- The "Gatekeeper" Logic
    CASE 
        WHEN employee_ssn IS NULL 
             OR employee_first_name IS NULL 
             OR employee_last_name IS NULL 
             OR employee_street IS NULL 
             OR employee_city IS NULL THEN TRUE 
        WHEN identity_confidence_score < 0.70 THEN TRUE
        ELSE FALSE 
    END AS review_required,

    -- The "Reason" Logic (Keeping your specific flags)
    CASE 
        WHEN employee_ssn IS NULL THEN 'Missing Critical Field: SSN'
        WHEN employee_first_name IS NULL OR employee_last_name IS NULL THEN 'Missing Critical Field: Name'
        WHEN employee_street IS NULL OR employee_city IS NULL THEN 'Missing Critical Field: Address'
        WHEN identity_confidence_score < 0.70 THEN 'Low Confidence Scan'
        ELSE 'Passed'
    END AS review_reason
FROM raw_pivoted