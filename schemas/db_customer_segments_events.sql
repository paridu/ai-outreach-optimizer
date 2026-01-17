-- DATABASE SCHEMA: CUSTOMER SEGMENTS AND EVENT LOGS
-- AGENT: DB ARCHITECT
-- VERSION: 1.0.0
-- DESCRIPTION: High-performance schema designed for real-time AI personalization and analytical segmentation.

-- 1. EXTENSIONS (For UUID and JSON processing)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. ENUMS
CREATE TYPE event_priority AS ENUM ('low', 'medium', 'high', 'critical');

-- 3. EVENT LOGS TABLE (Optimized for high-volume ingestion)
-- This table stores every interaction point, providing the raw data for AI models.
CREATE TABLE event_logs (
    event_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL, -- e.g., 'page_view', 'add_to_cart', 'search'
    priority event_priority DEFAULT 'medium',
    source_platform VARCHAR(50),      -- e.g., 'ios', 'android', 'web'
    
    -- payload stores flexible event-specific data (e.g., product_id, search_term)
    payload JSONB NOT NULL,
    
    -- context stores environmental data (e.g., location, device_info, session_id)
    context JSONB,
    
    event_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMPTZ -- Timestamp when the AI engine processed this for real-time decisioning
);

CREATE INDEX idx_event_logs_customer_id ON event_logs(customer_id);
CREATE INDEX idx_event_logs_timestamp ON event_logs(event_timestamp DESC);
CREATE INDEX idx_event_logs_type ON event_logs(event_type);

-- 4. SEGMENT DEFINITIONS TABLE
-- Stores the metadata and logic for different customer segments.
CREATE TABLE segment_metadata (
    segment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    segment_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    
    -- rule_logic stores the JSON-defined filters or AI model ID used to generate this segment
    rule_logic JSONB,
    
    is_automated BOOLEAN DEFAULT TRUE, -- TRUE if updated by AI/ETL, FALSE if manual
    refresh_interval_minutes INTEGER DEFAULT 60,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 5. CUSTOMER SEGMENT MAPPING (The "State" Table)
-- Optimized for real-time lookup during the decisioning phase.
CREATE TABLE customer_segment_members (
    customer_id VARCHAR(100) NOT NULL,
    segment_id UUID REFERENCES segment_metadata(segment_id) ON DELETE CASCADE,
    
    -- score represents the AI's confidence or the customer's propensity score within this segment
    affinity_score DECIMAL(5, 4) DEFAULT 1.0000,
    
    joined_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ, -- For temporary/behavioral segments (e.g., 'In-Market for 24h')
    
    PRIMARY KEY (customer_id, segment_id)
);

CREATE INDEX idx_segment_lookup ON customer_segment_members(segment_id, affinity_score DESC);

-- 6. VIEWS FOR ANALYTICS
CREATE VIEW view_customer_behavior_summary AS
SELECT 
    customer_id,
    COUNT(event_id) as total_interactions,
    MAX(event_timestamp) as last_active,
    array_agg(DISTINCT event_type) as event_types_interacted
FROM event_logs
GROUP BY customer_id;

-- 7. TRIGGER FOR UPDATED_AT
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_segment_metadata_modtime
    BEFORE UPDATE ON segment_metadata
    FOR EACH ROW
    EXECUTE PROCEDURE update_modified_column();

COMMENT ON TABLE event_logs IS 'Granular log of all customer interactions for AI training and real-time triggers.';
COMMENT ON TABLE segment_metadata IS 'Definitions of customer cohorts based on behavioral or demographic logic.';
COMMENT ON TABLE customer_segment_members IS 'High-speed mapping of customers to segments with AI-calculated affinity scores.';