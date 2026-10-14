-- =============================================================================
-- Grito Labs Multi-Channel Marketing Analytics & Attribution Framework
-- Script 03: Multi-Touch Attribution Models in Pure SQL
-- Dialect: ANSI SQL / PostgreSQL / DuckDB / SQLite Compatible
-- Models Implemented:
--   1. First-Touch Attribution (FTA): 100% to initial discovery touchpoint
--   2. Last-Touch Attribution (LTA): 100% to conversion-triggering touchpoint
--   3. Linear Attribution: Equal weight (1 / N) across all path touchpoints
--   4. Time-Decay Attribution: Exponential half-life decay (lambda = 7 days)
--   5. Position-Based / U-Shaped (40-20-40): 40% first, 40% last, 20% middle
-- =============================================================================

WITH converting_touchpoints AS (
    SELECT 
        tp.touchpoint_id,
        tp.user_id,
        tp.channel,
        tp.campaign_id,
        tp.timestamp AS touch_time,
        c.conversion_timestamp,
        c.net_revenue_usd,
        -- Sequence position within journey
        ROW_NUMBER() OVER (
            PARTITION BY tp.user_id 
            ORDER BY tp.timestamp ASC
        ) AS touch_seq,
        -- Total touches in journey
        COUNT(*) OVER (
            PARTITION BY tp.user_id
        ) AS total_touches,
        -- Time difference in days between touchpoint and conversion
        (JULIANDAY(c.conversion_timestamp) - JULIANDAY(tp.timestamp)) AS days_prior_to_conv
    FROM web_touchpoints tp
    INNER JOIN conversions_and_orders c 
        ON tp.user_id = c.user_id
        AND tp.timestamp <= c.conversion_timestamp
),

-- Weight assignment CTE for each touchpoint under each model
attributed_weights AS (
    SELECT 
        touchpoint_id,
        user_id,
        channel,
        campaign_id,
        touch_time,
        conversion_timestamp,
        net_revenue_usd,
        touch_seq,
        total_touches,
        
        -- Model 1: First-Touch Attribution Weight
        CASE 
            WHEN touch_seq = 1 THEN 1.0 
            ELSE 0.0 
        END AS weight_first_touch,

        -- Model 2: Last-Touch Attribution Weight
        CASE 
            WHEN touch_seq = total_touches THEN 1.0 
            ELSE 0.0 
        END AS weight_last_touch,

        -- Model 3: Linear Attribution Weight
        (1.0 / total_touches) AS weight_linear,

        -- Model 4: Raw Time-Decay Weight using 7-day half-life: 2^(-delta_t / 7.0)
        -- In SQLite: POWER(2.0, -days_prior_to_conv / 7.0)
        POWER(2.0, -CAST(days_prior_to_conv AS REAL) / 7.0) AS raw_time_decay_weight,

        -- Model 5: Position-Based / U-Shaped Weight
        CASE 
            WHEN total_touches = 1 THEN 1.0
            WHEN total_touches = 2 THEN 0.50
            WHEN touch_seq = 1 THEN 0.40
            WHEN touch_seq = total_touches THEN 0.40
            ELSE (0.20 / (total_touches - 2))
        END AS weight_u_shaped
    FROM converting_touchpoints
),

-- Normalize Time-Decay weights so that sum of weights per user equals exactly 1.0
normalized_attribution AS (
    SELECT 
        touchpoint_id,
        user_id,
        channel,
        campaign_id,
        net_revenue_usd,
        weight_first_touch,
        weight_last_touch,
        weight_linear,
        weight_u_shaped,
        -- Normalized Time-Decay Weight
        raw_time_decay_weight / SUM(raw_time_decay_weight) OVER (PARTITION BY user_id) AS weight_time_decay
    FROM attributed_weights
)

-- Final Aggregation: Channel-Level Model Comparison
SELECT 
    channel,
    -- First Touch
    ROUND(SUM(weight_first_touch), 2) AS conv_first_touch,
    ROUND(SUM(weight_first_touch * net_revenue_usd), 2) AS rev_first_touch,

    -- Last Touch
    ROUND(SUM(weight_last_touch), 2) AS conv_last_touch,
    ROUND(SUM(weight_last_touch * net_revenue_usd), 2) AS rev_last_touch,

    -- Linear
    ROUND(SUM(weight_linear), 2) AS conv_linear,
    ROUND(SUM(weight_linear * net_revenue_usd), 2) AS rev_linear,

    -- Time-Decay
    ROUND(SUM(weight_time_decay), 2) AS conv_time_decay,
    ROUND(SUM(weight_time_decay * net_revenue_usd), 2) AS rev_time_decay,

    -- U-Shaped (Position-Based)
    ROUND(SUM(weight_u_shaped), 2) AS conv_u_shaped,
    ROUND(SUM(weight_u_shaped * net_revenue_usd), 2) AS rev_u_shaped

FROM normalized_attribution
GROUP BY channel
ORDER BY rev_linear DESC;
