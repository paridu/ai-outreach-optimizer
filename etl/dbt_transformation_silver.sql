-- dbt Model: Silver Layer - Unified Customer Interactions
-- Purpose: Deduplication, PII masking, and enrichment for AI Decisioning Engine

{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='event_id',
    cluster_by=['customer_id', 'event_time']
) }}

WITH raw_events AS (
    SELECT *
    FROM {{ source('bronze', 'customer_interactions') }}
    {% if is_incremental() %}
    WHERE ingestion_at > (SELECT max(ingestion_at) FROM {{ this }})
    {% endif %}
),

cleaned_events AS (
    SELECT
        event_id,
        customer_id,
        UPPER(event_type) AS interaction_type,
        event_time,
        platform,
        COALESCE(product_id, 'N/A') AS product_id,
        COALESCE(action_value, 0.0) AS interaction_score,
        -- Hash PII if necessary for GDPR/Compliance
        sha2(customer_id, 256) AS hashed_customer_id,
        ingestion_at
    FROM raw_events
    WHERE customer_id IS NOT NULL
)

SELECT 
    *,
    -- Flag for High-Value actions to trigger real-time AI agents
    CASE 
        WHEN interaction_type IN ('PURCHASE', 'ADD_TO_CART') THEN TRUE 
        ELSE FALSE 
    END AS is_priority_event
FROM cleaned_events