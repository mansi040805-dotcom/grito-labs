-- =============================================================================
-- Grito Labs Multi-Channel Marketing Analytics & Attribution Framework
-- Script 01: Relational Schema DDL & Indexing Strategy
-- Dialect: ANSI SQL / PostgreSQL / DuckDB / SQLite Compatible
-- =============================================================================

-- Table 1: Daily Campaign Marketing Spend
-- Tracks top-of-funnel media investments across all acquisition channels
CREATE TABLE IF NOT EXISTS ad_spend_daily (
    spend_date DATE NOT NULL,
    channel VARCHAR(64) NOT NULL,
    campaign_id VARCHAR(64) NOT NULL,
    campaign_name VARCHAR(128) NOT NULL,
    impressions INTEGER NOT NULL CHECK (impressions >= 0),
    clicks INTEGER NOT NULL CHECK (clicks >= 0),
    spend_usd NUMERIC(12, 2) NOT NULL CHECK (spend_usd >= 0),
    cpc_usd NUMERIC(8, 2),
    ctr_pct NUMERIC(6, 2),
    PRIMARY KEY (spend_date, campaign_id)
);

-- Table 2: Web & Digital Touchpoints
-- Captures granular clickstream interactions across prospective student journeys
CREATE TABLE IF NOT EXISTS web_touchpoints (
    touchpoint_id VARCHAR(32) PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL,
    session_id VARCHAR(32) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    touch_date DATE NOT NULL,
    channel VARCHAR(64) NOT NULL,
    campaign_id VARCHAR(64) NOT NULL,
    campaign_name VARCHAR(128),
    interaction_seq INTEGER NOT NULL CHECK (interaction_seq >= 1),
    device_category VARCHAR(32) CHECK (device_category IN ('Desktop', 'Mobile', 'Tablet')),
    landing_page VARCHAR(128),
    session_duration_sec INTEGER CHECK (session_duration_sec >= 0),
    pages_viewed INTEGER CHECK (pages_viewed >= 1),
    has_form_submit INTEGER DEFAULT 0 CHECK (has_form_submit IN (0, 1))
);

-- Table 3: Conversions & Course Enrollments
-- Captures commercial conversions (student admissions & tuition transactions)
CREATE TABLE IF NOT EXISTS conversions_and_orders (
    order_id VARCHAR(32) PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL UNIQUE,
    conversion_timestamp TIMESTAMP NOT NULL,
    conversion_date DATE NOT NULL,
    program_code VARCHAR(32) NOT NULL,
    program_name VARCHAR(128) NOT NULL,
    gross_revenue_usd NUMERIC(10, 2) NOT NULL CHECK (gross_revenue_usd > 0),
    discount_usd NUMERIC(10, 2) DEFAULT 0 CHECK (discount_usd >= 0),
    net_revenue_usd NUMERIC(10, 2) NOT NULL CHECK (net_revenue_usd > 0),
    payment_mode VARCHAR(64),
    journey_length_touches INTEGER NOT NULL CHECK (journey_length_touches >= 1),
    first_touch_channel VARCHAR(64) NOT NULL,
    last_touch_channel VARCHAR(64) NOT NULL,
    journey_path TEXT NOT NULL
);

-- Table 4: Customer Retention & 12-Month LTV Cohorts
-- Tracks post-enrollment student outcomes, RCA capstone completion, upsells & referrals
CREATE TABLE IF NOT EXISTS customer_retention_cohorts (
    user_id VARCHAR(32) PRIMARY KEY,
    order_id VARCHAR(32) NOT NULL UNIQUE,
    enrollment_cohort_month VARCHAR(16) NOT NULL,
    completed_capstone INTEGER DEFAULT 0 CHECK (completed_capstone IN (0, 1)),
    nps_rating INTEGER CHECK (nps_rating BETWEEN 0 AND 10),
    upsell_program_enrolled VARCHAR(64),
    upsell_revenue_usd NUMERIC(10, 2) DEFAULT 0,
    referrals_generated INTEGER DEFAULT 0 CHECK (referrals_generated >= 0),
    referral_incentive_usd NUMERIC(10, 2) DEFAULT 0,
    total_customer_ltv_usd NUMERIC(12, 2) NOT NULL,
    is_active_alumni_network INTEGER DEFAULT 0 CHECK (is_active_alumni_network IN (0, 1)),
    FOREIGN KEY (user_id) REFERENCES conversions_and_orders (user_id)
);

-- Indexing for High-Performance Attribution & Window Analytical Queries
CREATE INDEX IF NOT EXISTS idx_touchpoints_user_time ON web_touchpoints (user_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_touchpoints_channel ON web_touchpoints (channel);
CREATE INDEX IF NOT EXISTS idx_touchpoints_campaign ON web_touchpoints (campaign_id);
CREATE INDEX IF NOT EXISTS idx_conversions_user ON conversions_and_orders (user_id);
CREATE INDEX IF NOT EXISTS idx_conversions_date ON conversions_and_orders (conversion_date);
CREATE INDEX IF NOT EXISTS idx_spend_channel ON ad_spend_daily (channel, spend_date);
