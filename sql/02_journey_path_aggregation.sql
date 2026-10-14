-- =============================================================================
-- Grito Labs Multi-Channel Marketing Analytics & Attribution Framework
-- Script 02: Customer Journey Sessionization & Conversion Path Stitching
-- Dialect: ANSI SQL / PostgreSQL / DuckDB / SQLite Compatible
-- =============================================================================

-- CTE 1: Filter touchpoints within a 30-day lookback window prior to conversion
WITH touchpoint_history AS (
    SELECT 
        tp.user_id,
        tp.touchpoint_id,
        tp.timestamp AS touch_time,
        tp.channel,
        tp.campaign_id,
        tp.campaign_name,
        tp.device_category,
        tp.landing_page,
        c.conversion_timestamp,
        c.order_id,
        c.net_revenue_usd,
        CASE WHEN c.order_id IS NOT NULL THEN 1 ELSE 0 END AS is_converted,
        -- Sequence number within user journey
        ROW_NUMBER() OVER (
            PARTITION BY tp.user_id 
            ORDER BY tp.timestamp ASC
        ) AS touch_seq,
        -- Total touches per user
        COUNT(*) OVER (
            PARTITION BY tp.user_id
        ) AS total_touches
    FROM web_touchpoints tp
    LEFT JOIN conversions_and_orders c 
        ON tp.user_id = c.user_id
        AND tp.timestamp <= c.conversion_timestamp
),

-- CTE 2: User Path Summary & Duration to Convert (in Days)
user_journey_summary AS (
    SELECT 
        user_id,
        is_converted,
        order_id,
        net_revenue_usd,
        total_touches,
        MIN(touch_time) AS first_touch_time,
        MAX(touch_time) AS last_touch_time,
        -- Julian day / day difference between first and last touch
        ROUND(
            (JULIANDAY(MAX(touch_time)) - JULIANDAY(MIN(touch_time))), 
            1
        ) AS journey_span_days
    FROM touchpoint_history
    GROUP BY user_id, is_converted, order_id, net_revenue_usd, total_touches
),

-- CTE 3: Path Length Distribution & Conversion Velocity
path_length_metrics AS (
    SELECT 
        total_touches AS touchpoints_count,
        COUNT(user_id) AS total_users,
        SUM(is_converted) AS converted_students,
        ROUND(SUM(is_converted) * 100.0 / COUNT(user_id), 2) AS conversion_rate_pct,
        ROUND(AVG(CASE WHEN is_converted = 1 THEN journey_span_days ELSE NULL END), 1) AS avg_days_to_convert,
        ROUND(SUM(CASE WHEN is_converted = 1 THEN net_revenue_usd ELSE 0 END), 2) AS total_revenue_usd
    FROM user_journey_summary
    GROUP BY total_touches
)

-- Query Result 1: Journey Length Conversion Funnel
SELECT 
    touchpoints_count,
    total_users,
    converted_students,
    conversion_rate_pct,
    avg_days_to_convert,
    total_revenue_usd,
    ROUND(total_revenue_usd / NULLIF(converted_students, 0), 2) AS avg_order_value_usd
FROM path_length_metrics
ORDER BY touchpoints_count ASC;
