{% macro generate_schema_name(custom_schema_name, node) -%}

    {# 
        If a custom schema (dataset) is defined in dbt_project.yml or a config block, 
        use ONLY that name. If not, fall back to the default target dataset 
        defined in profiles.yml.
    #}

    {%- if custom_schema_name is none -%}

        {{ target.schema }}

    {%- else -%}

        {{ custom_schema_name | trim }}

    {%- endif -%}

{%- endmacro %}
