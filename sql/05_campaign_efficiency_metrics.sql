-- =============================================================================
-- Grito Labs Multi-Channel Marketing Analytics & Attribution Framework
-- Script 05: Campaign Efficiency KPIs & Saturation Analysis
-- Dialect: ANSI SQL / PostgreSQL / DuckDB / SQLite Compatible
-- =============================================================================

WITH campaign_spend_summary AS (
    SELECT 
        campaign_id,
        campaign_name,
        channel,
        SUM(spend_usd) AS total_spend_usd,
        SUM(impressions) AS total_impressions,
        SUM(clicks) AS total_clicks,
        ROUND(AVG(cpc_usd), 2) AS avg_cpc_usd,
        ROUND(SUM(clicks) * 100.0 / NULLIF(SUM(impressions), 0), 2) AS avg_ctr_pct
    FROM ad_spend_daily
    GROUP BY campaign_id, campaign_name, channel
),

touchpoint_linear_credit AS (
    SELECT 
        tp.campaign_id,
        COUNT(DISTINCT tp.user_id) AS engaged_prospects,
        -- Linear conversion credit
        ROUND(SUM(CASE WHEN c.order_id IS NOT NULL THEN (1.0 / c.journey_length_touches) ELSE 0 END), 2) AS linear_conversions,
        ROUND(SUM(CASE WHEN c.order_id IS NOT NULL THEN (c.net_revenue_usd * 1.0 / c.journey_length_touches) ELSE 0 END), 2) AS linear_revenue_usd,
        -- Last touch conversion credit
        ROUND(SUM(CASE WHEN c.order_id IS NOT NULL AND tp.interaction_seq = c.journey_length_touches THEN 1.0 ELSE 0 END), 2) AS last_touch_conversions,
        ROUND(SUM(CASE WHEN c.order_id IS NOT NULL AND tp.interaction_seq = c.journey_length_touches THEN c.net_revenue_usd ELSE 0 END), 2) AS last_touch_revenue_usd
    FROM web_touchpoints tp
    LEFT JOIN conversions_and_orders c ON tp.user_id = c.user_id
    GROUP BY tp.campaign_id
)

SELECT 
    s.campaign_id,
    s.campaign_name,
    s.channel,
    s.total_spend_usd,
    s.total_impressions,
    s.total_clicks,
    s.avg_ctr_pct,
    s.avg_cpc_usd,
    t.linear_conversions,
    t.linear_revenue_usd,
    t.last_touch_conversions,
    t.last_touch_revenue_usd,
    
    -- Linear CAC & ROAS
    CASE 
        WHEN s.total_spend_usd = 0 THEN 0.0
        WHEN t.linear_conversions > 0 THEN ROUND(s.total_spend_usd / t.linear_conversions, 2)
        ELSE 999.0 
    END AS linear_cac_usd,

    CASE 
        WHEN s.total_spend_usd = 0 THEN 999.0
        ELSE ROUND(t.linear_revenue_usd / s.total_spend_usd, 2)
    END AS linear_roas,

    -- LTA to Linear Distortion Ratio (> 1.2 indicates heavy Last-Click bias / cannibalization)
    ROUND(t.last_touch_conversions / NULLIF(t.linear_conversions, 0), 2) AS lta_to_linear_ratio,

    -- Strategic Evaluation Flag
    CASE 
        WHEN s.total_spend_usd = 0 THEN 'ORGANIC_PILLAR'
        WHEN t.linear_revenue_usd / s.total_spend_usd >= 4.0 THEN 'SCALE_AGGRESSIVE'
        WHEN t.linear_revenue_usd / s.total_spend_usd >= 2.5 THEN 'MAINTAIN_AND_OPTIMIZE'
        ELSE 'REDUCE_BUDGET_DRAIN'
    END AS strategic_recommendation

FROM campaign_spend_summary s
LEFT JOIN touchpoint_linear_credit t ON s.campaign_id = t.campaign_id
ORDER BY s.total_spend_usd DESC;
