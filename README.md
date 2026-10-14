# Multi-Channel Marketing Analytics & Attribution Framework
### Executive Analytics, Algorithmic Multi-Touch Attribution, and Capital Optimization
**Organization:** Grito Labs (Industry-Focused EdTech Platform for Data & Business Analytics)  
**Domain:** Marketing Analytics & Business Intelligence  
**Author:** Lead Marketing Analytics & Business Intelligence Specialist  
**Evaluation Scope:** H1 2026 Commercial Audit (180 Days | 9,995 Touchpoints | 1,385 Enrolled Students | \$1.65M Net Revenue)  

---

## 🏆 Project Highlights & Executive Summary

* **The Problem:** Grito Labs invests heavily across Google Search, Meta Ads, YouTube Ads, LinkedIn Ads, and Email Nurture to acquire students for its flagship programs (*Data Analytics Accelerator*, *Business Analytics & RCA Masterclass*, *Enterprise AI Fellowship*). Historically, relying on **Last-Touch Attribution (LTA)** over-credited Google Search and Direct navigation by **+48%** (\$589.7k vs \$395.2k), severely undervaluing top-of-funnel discovery channels like Meta and YouTube Ads.
* **The Solution:** An end-to-end multi-channel attribution and capital optimization framework evaluating **6 attribution models**:
  1. First-Touch Attribution (FTA)
  2. Last-Touch Attribution (LTA)
  3. Linear Attribution
  4. Time-Decay Attribution (7-Day Exponential Half-Life)
  5. Position-Based / U-Shaped (40-20-40)
  6. **Data-Driven Algorithmic Attribution (Markov Chains & Removal Effects)**
* **The Business Impact:**
  * Identified a **\$47.5k capital drain** on LinkedIn Ads generating an unsustainable CAC of **\$547.62** (ROAS: 2.16x).
  * Discovered **Email Marketing** as Grito Labs' highest ROI engine (**47.98x ROAS**, **\$24.61 CAC**, Removal Effect: 0.2765).
  * Designed a mathematical **Hill-Markov Capital Reallocation Strategy** shifting \$19.0k from LinkedIn Ads into Email automation, YouTube Ads, and Google Search, unlocking:
    * **+\$74,941.99 in Incremental Net Tuition Revenue**
    * **+63.5 Additional Enrolled Students (+5.88% Enrollment Uplift)**
    * **\$0 Additional Media Budget Required**

---

## 📁 Repository Directory Structure

```
grito labs/
├── README.md                                  # Master repository documentation & quick-start guide
├── PS_Grito_labs.pdf                          # Official Problem Statement specification
├── grito_ss.png                               # Project context screenshot
├── data/
│   ├── grito_marketing_analytics.db           # Relational SQLite database with all tables, views & indexes
│   ├── Grito_Labs_Marketing_Attribution_Model.xlsx # 6-Tab Boardroom-ready Financial Model with formulas
│   ├── raw/
│   │   ├── ad_spend_daily.csv                 # 2,715 daily campaign records (spend, impressions, clicks, CPC)
│   │   ├── web_touchpoints.csv                # 9,995 granular customer session logs (channel, campaign, page)
│   │   ├── conversions_and_orders.csv         # 1,385 student enrollment transactions (AOV, discount, tuition)
│   │   └── customer_retention_cohorts.csv     # 1,385 student retention, capstone completion & 12M LTV records
│   └── processed/
│       ├── customer_journey_paths.csv         # Aggregated multi-touch paths, touchpoint counts & CVR
│       ├── attribution_model_comparison.csv   # Cross-channel credit across all 6 attribution models
│       ├── campaign_roi_deepdive.csv          # Granular audit of all 15 marketing campaigns
│       └── budget_reallocation_strategy.csv   # Quantitative marginal optimization outcomes
├── sql/
│   ├── 01_schema_ddl.sql                      # DDL schema with primary/foreign keys & index strategy
│   ├── 02_journey_path_aggregation.sql        # Window CTEs, sessionization & path stitching
│   ├── 03_rule_based_attribution.sql          # First-Touch, Last-Touch, Linear, Time-Decay & U-Shaped in SQL
│   ├── 04_cohort_retention_ltv.sql            # Capstone completion, NPS, referrals & 12M LTV by channel
│   └── 05_campaign_efficiency_metrics.sql     # Blended vs Paid CAC, ROAS, CPC, CTR & saturation flags
├── notebooks/
│   └── 01_multi_channel_marketing_attribution.ipynb # End-to-end reproducible Jupyter Notebook
├── dashboard/
│   ├── index.html                             # Standalone interactive executive BI dashboard
│   ├── app.js                                 # Client-side analytical engine & simulator logic
│   └── style.css                              # Tailwind and custom UI styling
├── presentation/
│   ├── Grito_Labs_Marketing_Attribution_Deck.pptx # 14-Slide Boardroom Executive Presentation
│   └── deck_presentation.html                 # Interactive browser slide deck with keyboard controls
├── scripts/
│   ├── generate_synthetic_data.py             # High-fidelity data generator tailored to Grito Labs
│   ├── run_attribution_pipeline.py            # Executes 6 attribution models & updates SQLite DB
│   ├── budget_optimizer.py                    # Hill-Markov marginal response capital reallocation
│   ├── generate_excel_workbook.py             # Compiles formatted Excel financial model (.xlsx)
│   ├── generate_presentation_deck.py          # Builds custom 14-slide executive presentation (.pptx)
│   └── build_notebook.py                      # Assembles clean, validated Jupyter Notebook
└── docs/
    ├── EXECUTIVE_SUMMARY_REPORT.md            # Exhaustive 12-section strategic report for Grito Labs leadership
    ├── METHODOLOGY.md                         # Mathematical derivations, Markov removal effects & caveats
    └── DATA_DICTIONARY.md                     # Complete relational schema & marketing KPI metric catalog
```

---

## 🚀 Quick-Start Guide: How to Run & Explore

### 1. Interactive Executive BI Dashboard
Open the standalone dashboard directly in any web browser (no local web server required):
```powershell
# Open via default browser in Windows
Start-Process "dashboard\index.html"
```
* **Features:**
  * Real-time model switcher (Markov Chain, Last-Touch, First-Touch, Linear, Time-Decay, U-Shaped)
  * Visual Markov Removal Effects bar chart
  * Top converting customer journey paths
  * **Interactive What-If Budget Simulator:** Drag sliders across channels to see projected enrollments and revenue update in real-time using calibrated marginal response curves!
  * Campaign efficiency audit table with status flags

### 2. Executive Boardroom Presentation Deck
* **PowerPoint File:** [`presentation/Grito_Labs_Marketing_Attribution_Deck.pptx`](presentation/Grito_Labs_Marketing_Attribution_Deck.pptx) — 14 professionally designed slides with custom metrics, comparison tables, and roadmap.
* **Interactive Browser Slides:** Open [`presentation/deck_presentation.html`](presentation/deck_presentation.html) in any browser (navigate using `←` and `→` arrow keys).

### 3. Financial & Attribution Excel Model
Open [`data/Grito_Labs_Marketing_Attribution_Model.xlsx`](data/Grito_Labs_Marketing_Attribution_Model.xlsx) in Microsoft Excel. Includes 5 formatted tabs:
1. `Executive Overview`: Portfolio KPIs, Blended ROAS, CAC, and strategic findings.
2. `Attribution Models`: 6-model cross-channel comparison with totals and formulas.
3. `Budget Optimization`: Current vs Recommended spend, dollar shifts, and projected ROI.
4. `Campaign Deep-Dive`: Granular audit of all 15 campaigns with efficiency statuses.
5. `Customer Journey Paths`: Top 25 converting multi-touch paths ranked by volume.

### 4. Executing the SQL Workflows
All SQL scripts are ANSI SQL compliant and run directly on the SQLite database (`data/grito_marketing_analytics.db`) or can be executed in PostgreSQL / BigQuery / Snowflake:
```powershell
# Run the complete attribution comparison script in Python
python -c "import sqlite3; conn = sqlite3.connect('data/grito_marketing_analytics.db'); print(conn.cursor().execute(open('sql/03_rule_based_attribution.sql').read()).fetchall())"
```

### 5. Running the Jupyter Notebook
```powershell
jupyter lab notebooks/01_multi_channel_marketing_attribution.ipynb
```

---

## 📊 Attribution Model Comparison Summary

| Acquisition Channel | Paid Media Spend | First-Touch (FTA) | Last-Touch (LTA) | Linear Model | Time-Decay (7d) | U-Shaped (40-20-40) | Markov Chain (Truth) | Markov Rev Credit | Markov ROAS | Markov CAC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Google Search** | \$82,007.20 | 182.0 | **496.0** | 308.0 | 330.0 | 325.5 | **334.7** | \$395,172.44 | **4.82x** | \$245.03 |
| **Meta Ads** | \$85,764.16 | **449.0** | 219.0 | 341.1 | 322.9 | 336.4 | **294.0** | \$347,084.09 | **4.05x** | \$291.76 |
| **YouTube Ads** | \$42,456.05 | **317.0** | 40.0 | 163.7 | 144.4 | 172.1 | **152.5** | \$180,001.53 | **4.24x** | \$278.49 |
| **Email Marketing** | \$5,218.13 | 0.0 | **302.0** | 235.7 | 256.4 | 188.7 | **212.0** | \$250,368.15 | **47.98x** | \$24.61 |
| **LinkedIn Ads** | \$47,451.14 | 135.0 | 17.0 | 94.7 | 84.9 | 84.5 | **86.7** | \$102,308.50 | **2.16x** | \$547.62 |
| **Organic Search** | \$0.00 | 246.0 | 127.0 | 161.5 | 153.2 | 175.3 | **177.5** | \$209,607.34 | **N/A** | \$0.00 |
| **Referral & Direct** | \$0.00 | 56.0 | 184.0 | 80.4 | 93.3 | 102.5 | **127.7** | \$150,815.44 | **N/A** | \$0.00 |
| **Total Portfolio** | **\$262,896.68** | **1,385.0** | **1,385.0** | **1,385.0** | **1,385.0** | **1,385.0** | **1,385.0** | **\$1,646,260.00** | **6.26x** | **\$189.82** |

---

## 📈 Budget Optimization Strategy (Hill-Markov Model)

By shifting \$18,980.46 away from underperforming LinkedIn Ads into high-incrementality channels (Email, YouTube, Google Search), Grito Labs expands tuition revenue without increasing spend:

| Channel | Current Spend | Recommended Spend | Shift ($) | Shift (%) | Current Conv | Projected Conv | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **LinkedIn Ads** | \$47,451.14 | **\$28,470.68** | **-\$18,980.46** | **-40.0%** | 86.7 | 63.8 | Eliminate high CPC bid waste (\$7.50); prune cold ads |
| **Email Marketing** | \$5,218.13 | **\$7,827.20** | **+\$2,609.07** | **+50.0%** | 212.0 | 268.4 | Scale Sunday Masterclass promos & automated drip |
| **YouTube Ads** | \$42,456.05 | **\$53,070.06** | **+\$10,614.01** | **+25.0%** | 152.5 | 176.9 | Scale free SQL workshop lead magnets |
| **Google Search** | \$82,007.20 | **\$89,387.85** | **+\$7,380.65** | **+9.0%** | 334.7 | 352.1 | Protect brand defense; capture growing search volume |
| **Meta Ads** | \$85,764.16 | **\$84,140.89** | **-\$1,623.27** | **-1.9%** | 294.0 | 291.8 | Maintain baseline; focus on top video Reels |
| **Total** | **\$262,896.68** | **\$262,896.68** | **\$0.00** | **0.0%** | **1,079.9** | **1,153.0** | **+63.5 Students (+\$74,941.99 Revenue Uplift)** |

---

## ✅ Problem Statement Submission Checklist

| PS Requirement | Deliverable Location | Status |
| :--- | :--- | :---: |
| Channel-level ROI analysis across acquisition channels | `sql/03_rule_based_attribution.sql`, `data/processed/attribution_model_comparison.csv` | **Complete** |
| Customer journey dataset & high-impact path analysis | `sql/02_journey_path_aggregation.sql`, `data/processed/customer_journey_paths.csv` | **Complete** |
| Multi-touch attribution models (FTA, LTA, Linear, Decay, U-Shaped, Markov) | `scripts/run_attribution_pipeline.py`, `sql/03_rule_based_attribution.sql` | **Complete** |
| Key marketing KPIs (Conversion Rate, ROAS, CAC, CTR, CPC, CLV) | `docs/DATA_DICTIONARY.md`, `sql/05_campaign_efficiency_metrics.sql` | **Complete** |
| Identify high-performing & underperforming campaigns | `data/processed/campaign_roi_deepdive.csv`, `docs/EXECUTIVE_SUMMARY_REPORT.md` | **Complete** |
| Quantitative budget reallocation recommendations | `scripts/budget_optimizer.py`, `data/processed/budget_reallocation_strategy.csv` | **Complete** |
| Structured analytical workflows (SQL queries & Notebooks) | `sql/*.sql` (5 scripts), `notebooks/01_multi_channel_marketing_attribution.ipynb` | **Complete** |
| Documented assumptions, methodologies & attribution logic | `docs/METHODOLOGY.md`, `docs/DATA_DICTIONARY.md` | **Complete** |
| Business-facing dashboard or presentation deck | `dashboard/index.html` (Interactive BI), `presentation/Grito_Labs_Marketing_Attribution_Deck.pptx` | **Complete** |

---
*Developed for Grito Labs H1 2026 Commercial Evaluation.*
