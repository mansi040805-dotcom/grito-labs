# Grito Labs Marketing Analytics Data Dictionary & Metric Catalog

**System:** Multi-Channel Marketing Analytics & Attribution Framework  
**Database Engine:** ANSI SQL / SQLite / PostgreSQL Compatible (`data/grito_marketing_analytics.db`)  
**Data Scope:** H1 2026 (180 Days, Jan 1 – Jun 30, 2026)  
**Author:** Lead Marketing Analytics & Business Intelligence Specialist  

---

## 1. Entity-Relationship Overview

```
                      +-----------------------------+
                      |       ad_spend_daily        |
                      +-----------------------------+
                      | spend_date (PK)             |
                      | campaign_id (PK)            |
                      | channel                     |
                      | spend_usd                   |
                      | impressions, clicks         |
                      +-----------------------------+
                                     |
                                     | (channel, campaign_id)
                                     v
+-----------------------------+             +-------------------------------+
|       web_touchpoints       |             |     conversions_and_orders    |
+-----------------------------+             +-------------------------------+
| touchpoint_id (PK)          |             | order_id (PK)                 |
| user_id (FK)  ------------->|<----------  | user_id (FK, Unique)          |
| session_id                  |             | conversion_timestamp          |
| timestamp                   |             | program_code                  |
| channel, campaign_id        |             | net_revenue_usd               |
| interaction_seq             |             | journey_length_touches        |
| device_category             |             | first_touch_channel           |
| landing_page                |             | last_touch_channel            |
+-----------------------------+             +-------------------------------+
                                                            |
                                                            | (user_id)
                                                            v
                                            +-------------------------------+
                                            |   customer_retention_cohorts  |
                                            +-------------------------------+
                                            | user_id (PK, FK)              |
                                            | enrollment_cohort_month       |
                                            | completed_capstone            |
                                            | nps_rating                    |
                                            | upsell_revenue_usd            |
                                            | referrals_generated           |
                                            | total_customer_ltv_usd        |
                                            +-------------------------------+
```

---

## 2. Granular Table Schemas

### 2.1 Table: `ad_spend_daily`
Captures daily media expenditure, exposure, and traffic engagement across all acquisition channels and marketing campaigns.

| Column Name | Data Type | Nullable | Primary Key | Description & Business Rules |
| :--- | :--- | :--- | :--- | :--- |
| `spend_date` | `DATE` | No | Composite PK | Date of ad delivery (YYYY-MM-DD). |
| `channel` | `VARCHAR(64)` | No | No | Marketing channel (`Google Search`, `Meta Ads`, `YouTube Ads`, `LinkedIn Ads`, `Email Marketing`, `Organic Search`, `Referral & Direct`). |
| `campaign_id` | `VARCHAR(64)` | No | Composite PK | Unique campaign identifier (e.g., `GS_Intent_Bootcamp`, `Meta_Feed_CareerTransition`). |
| `campaign_name` | `VARCHAR(128)`| No | No | Human-readable campaign naming convention. |
| `impressions` | `INTEGER` | No | No | Count of times ad creative was displayed to users ($\ge 0$). |
| `clicks` | `INTEGER` | No | No | Count of user clicks recorded on the ad creative ($\ge 0$). |
| `spend_usd` | `NUMERIC(12,2)` | No | No | Media spend in US Dollars ($\ge 0$). $0 for organic/referral. |
| `cpc_usd` | `NUMERIC(8,2)` | Yes | No | Cost per Click: $\frac{\text{spend\_usd}}{\text{clicks}}$. |
| `ctr_pct` | `NUMERIC(6,2)` | Yes | No | Click-Through Rate: $\frac{\text{clicks}}{\text{impressions}} \times 100$. |

---

### 2.2 Table: `web_touchpoints`
Captures clickstream interactions across prospective student journeys. Enables multi-touch sessionization and path stitching.

| Column Name | Data Type | Nullable | Primary Key | Description & Business Rules |
| :--- | :--- | :--- | :--- | :--- |
| `touchpoint_id` | `VARCHAR(32)` | No | PK | Unique identifier for the individual session touchpoint. |
| `user_id` | `VARCHAR(32)` | No | FK | Unique identifier for prospective student (e.g., `USR_00142`). |
| `session_id` | `VARCHAR(32)` | No | No | Unique browsing session identifier (e.g., `SES_00142_1`). |
| `timestamp` | `TIMESTAMP` | No | No | Precise UTC timestamp of user interaction (YYYY-MM-DD HH:MM:SS). |
| `touch_date` | `DATE` | No | No | Calendar date of touchpoint. |
| `channel` | `VARCHAR(64)` | No | No | Traffic acquisition channel for the touchpoint. |
| `campaign_id` | `VARCHAR(64)` | No | No | Marketing campaign originating the session. |
| `campaign_name` | `VARCHAR(128)`| Yes | No | Name of marketing campaign. |
| `interaction_seq`| `INTEGER` | No | No | Chronological order of touchpoint in user's journey ($1, 2, 3, \dots$). |
| `device_category`| `VARCHAR(32)` | Yes | No | Device classification: `Desktop` (52%), `Mobile` (43%), `Tablet` (5%). |
| `landing_page` | `VARCHAR(128)`| Yes | No | Entry URI path (e.g., `/curriculum/data-analytics`, `/free-masterclass-signup`). |
| `session_duration_sec`| `INTEGER` | Yes | No | Dwell time in seconds spent during the session ($\ge 0$). |
| `pages_viewed` | `INTEGER` | Yes | No | Depth of session browsing ($\ge 1$). |
| `has_form_submit`| `INTEGER` | No | No | Boolean flag ($1$ if user submitted syllabus or webinar lead form, $0$ otherwise). |

---

### 2.3 Table: `conversions_and_orders`
Captures commercial transactions for students admitted into Grito Labs programs.

| Column Name | Data Type | Nullable | Primary Key | Description & Business Rules |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | `VARCHAR(32)` | No | PK | Unique enrollment invoice identifier (e.g., `ORD_1042`). |
| `user_id` | `VARCHAR(32)` | No | Unique FK | Student user identifier. |
| `conversion_timestamp` | `TIMESTAMP` | No | No | Timestamp when tuition payment succeeded. |
| `conversion_date` | `DATE` | No | No | Calendar date of enrollment transaction. |
| `program_code` | `VARCHAR(32)` | No | No | Program code (`DA_ACCEL`, `BA_MASTER`, `AI_FELLOW`). |
| `program_name` | `VARCHAR(128)`| No | No | Program title (e.g., Data Analytics Accelerator 12-Wk). |
| `gross_revenue_usd`| `NUMERIC(10,2)`| No | No | Listed catalog tuition fee before scholarships ($950, $1,250, $1,850). |
| `discount_usd` | `NUMERIC(10,2)`| No | No | Scholarship / early-bird discount applied ($\ge 0$). |
| `net_revenue_usd` | `NUMERIC(10,2)`| No | No | Final realized tuition collected: $\text{gross} - \text{discount}$. |
| `payment_mode` | `VARCHAR(64)` | Yes | No | Financial settlement channel (`Credit Card / Debit`, `EMI / Installments`, `UPI`, `Corporate`). |
| `journey_length_touches`| `INTEGER` | No | No | Count of interactions prior to payment ($1 \le N \le 7$). |
| `first_touch_channel` | `VARCHAR(64)` | No | No | Channel that originated the prospective student's first visit. |
| `last_touch_channel` | `VARCHAR(64)` | No | No | Channel that triggered the final conversion session. |
| `journey_path` | `TEXT` | No | No | Full chronological channel sequence (e.g., `Meta Ads > Email Marketing > Google Search`). |

---

### 2.4 Table: `customer_retention_cohorts`
Captures 12-month post-enrollment engagement, academic completion, satisfaction, upsells, and advocacy.

| Column Name | Data Type | Nullable | Primary Key | Description & Business Rules |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | `VARCHAR(32)` | No | PK, FK | Foreign key matching `conversions_and_orders.user_id`. |
| `order_id` | `VARCHAR(32)` | No | Unique FK | Foreign key matching original tuition invoice. |
| `enrollment_cohort_month`| `VARCHAR(16)`| No | No | Admission cohort month (`2026-01` through `2026-06`). |
| `completed_capstone` | `INTEGER` | No | No | 1 if student successfully submitted RCA industry capstone, 0 otherwise. |
| `nps_rating` | `INTEGER` | No | No | Net Promoter Score rating on 0–10 scale. |
| `upsell_program_enrolled`| `VARCHAR(64)`| Yes | No | Follow-up advanced module purchased (e.g., `Advanced RCA Case Lab`). |
| `upsell_revenue_usd`| `NUMERIC(10,2)`| No | No | Secondary tuition revenue from upsells ($0 or $450). |
| `referrals_generated` | `INTEGER` | No | No | Number of peer students referred by this user. |
| `referral_incentive_usd`| `NUMERIC(10,2)`| No | No | Referral scholarships disbursed to student ($75 per student). |
| `total_customer_ltv_usd`| `NUMERIC(12,2)`| No | No | 12-month total gross contribution: $\text{initial\_net\_tuition} + \text{upsell\_revenue}$. |
| `is_active_alumni_network`| `INTEGER` | No | No | 1 if active on Grito Labs alumni Slack & mentorship platform. |

---

## 3. Marketing & Financial KPI Mathematical Definitions

### 3.1 Return on Ad Spend (ROAS)
Measures gross tuition revenue generated per dollar of paid media expenditure.
$$\text{ROAS} = \frac{\text{Attributed Net Revenue (\USD)}}{\text{Media Spend (\USD)}}$$

### 3.2 Customer Acquisition Cost (CAC)
Measures the direct media cost required to enroll one paying student.
$$\text{CAC}_{\text{channel}} = \frac{\text{Channel Media Spend (\USD)}}{\text{Attributed Channel Conversions}}$$
$$\text{Blended CAC} = \frac{\text{Total Portfolio Paid Media Spend (\USD)}}{\text{Total Enrolled Students (Paid + Organic)}}$$
* In H1 2026: Blended CAC = $\frac{\$262,896.68}{1,385} = \$189.82$

### 3.3 Average Order Value (AOV)
$$\text{AOV} = \frac{\text{Total Net Tuition Revenue}}{\text{Total Enrolled Students}} = \frac{\$1,646,260.00}{1,385} = \$1,188.63$$

### 3.4 Customer Lifetime Value (12-Month Empirical LTV)
$$\text{LTV} = \text{Net Initial Tuition} + \text{Upsell Program Revenue}$$
* Empirical Average across Grito Labs Cohorts = **$1,304.50**

### 3.5 LTV-to-CAC Ratio
Indicates unit economic sustainability. A ratio $> 3.0\times$ represents healthy unit economics.
$$\text{LTV:CAC} = \frac{\text{Average 12-Month LTV}}{\text{CAC}_{\text{channel}}}$$
* Google Search: $\frac{\$1,269.78}{\$245.03} = 5.18\times$ (Healthy)
* Meta Ads: $\frac{\$1,257.13}{\$291.76} = 4.31\times$ (Healthy)
* LinkedIn Ads: $\frac{\$1,285.00}{\$547.62} = 2.35\times$ (Underperforming / Borderline)

### 3.6 Payback Period (Months)
Number of months required to recoup the upfront customer acquisition investment based on net contribution margin per student (~$400/month).
$$\text{Payback Period} = \frac{\text{CAC}}{\text{Monthly Net Contribution Margin}}$$

---

## 4. Attribution Model Metrics Reference

| Model Key | Mathematical Weight Formula | Core Philosophy |
| :--- | :--- | :--- |
| `first_touch` | $w_i = 1.0$ if $i = 1$, else $0$ | 100% Discovery Credit |
| `last_touch` | $w_i = 1.0$ if $i = N$, else $0$ | 100% Demand Capture Credit |
| `linear` | $w_i = \frac{1}{N}$ | Equal Democratic Distribution |
| `time_decay` | $w_i = \frac{2^{-\Delta t_i / \lambda}}{\sum_j 2^{-\Delta t_j / \lambda}}$, $\lambda = 7$ days | Exponential Half-life Recency |
| `u_shaped` | $w_1 = 0.40, w_N = 0.40, w_{2 \dots N-1} = \frac{0.20}{N-2}$ | Position-Based Funnel Milestone |
| `markov_chain` | $W(c) = \frac{RE(c)}{\sum_k RE(k)}$, $RE(c) = \frac{P(\text{Conv}) - P(\text{Conv}\setminus\{c\})}{P(\text{Conv})}$ | Algorithmic Graph Removal Effect |
