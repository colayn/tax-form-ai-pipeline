{{ config(materialized='table') }}

SELECT
    employee_first_name AS customer_first_name,
    employee_last_name AS customer_last_name,
    employee_ssn AS customer_identification_number,
    employee_street AS customer_street_address,
    employee_city AS customer_city_address,
    employee_state AS customer_state_address,
    extraction_ts AS data_extraction_timestamp -- Aliased for clarity
FROM {{ ref('silver_clean_tax_forms') }}
WHERE review_required = FALSE 
  AND employee_ssn IS NOT NULL 
  AND employee_last_name IS NOT NULL
  AND employee_street IS NOT NULL