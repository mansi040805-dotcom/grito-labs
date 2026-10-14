-- =============================================================================
-- Grito Labs Multi-Channel Marketing Analytics & Attribution Framework
-- Script 04: Cohort Retention & 12-Month Empirical Customer Lifetime Value (LTV)
-- Dialect: ANSI SQL / PostgreSQL / DuckDB / SQLite Compatible
-- =============================================================================

WITH student_profiles AS (
    SELECT 
        c.user_id,
        c.order_id,
        c.first_touch_channel,
        c.last_touch_channel,
        c.program_name,
        c.net_revenue_usd AS initial_tuition_usd,
        r.enrollment_cohort_month,
        r.completed_capstone,
        r.nps_rating,
        r.upsell_revenue_usd,
        r.referrals_generated,
        r.referral_incentive_usd,
        r.total_customer_ltv_usd,
        r.is_active_alumni_network
    FROM conversions_and_orders c
    INNER JOIN customer_retention_cohorts r 
        ON c.user_id = r.user_id
)

-- Query 1: LTV, Retention, and Advocacy by First-Touch Acquisition Channel
SELECT 
    first_touch_channel,
    COUNT(user_id) AS enrolled_students,
    ROUND(AVG(initial_tuition_usd), 2) AS avg_initial_order_value_usd,
    ROUND(SUM(completed_capstone) * 100.0 / COUNT(user_id), 1) AS capstone_completion_rate_pct,
    ROUND(AVG(nps_rating), 2) AS avg_nps_score,
    ROUND(SUM(CASE WHEN upsell_revenue_usd > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(user_id), 1) AS upsell_conversion_rate_pct,
    ROUND(AVG(upsell_revenue_usd), 2) AS avg_upsell_revenue_usd,
    SUM(referrals_generated) AS total_referrals_generated,
    ROUND(SUM(referrals_generated) * 1.0 / COUNT(user_id), 2) AS referrals_per_student,
    ROUND(AVG(total_customer_ltv_usd), 2) AS avg_12m_customer_ltv_usd,
    ROUND(SUM(total_customer_ltv_usd), 2) AS total_cohort_ltv_usd
FROM student_profiles
GROUP BY first_touch_channel
ORDER BY avg_12m_customer_ltv_usd DESC;
