"""
================================================================================
Grito Labs - Multi-Channel Marketing Analytics & Attribution Framework
Synthetic Data Generator
================================================================================
Generates high-fidelity, production-grade marketing datasets for Grito Labs:
1. ad_spend_daily.csv: Daily campaign impressions, clicks, spend across 180 days.
2. web_touchpoints.csv: Granular user interaction logs (channel, campaign, device, page).
3. conversions_and_orders.csv: Order details (program, gross & net revenue, coupon).
4. customer_retention_cohorts.csv: 12-month post-enrollment engagement and LTV.
"""

import os
import csv
import math
import random
import sqlite3
from datetime import datetime, timedelta

# Fix seed for reproducibility
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
DB_PATH = os.path.join(BASE_DIR, "data", "grito_marketing_analytics.db")

os.makedirs(DATA_RAW_DIR, exist_ok=True)
os.makedirs(DATA_PROC_DIR, exist_ok=True)

START_DATE = datetime(2026, 1, 1)
DAYS_COUNT = 181  # 6 months (Jan 1 to Jun 30, 2026)

# Channel & Campaign Definitions
CAMPAIGNS = [
    # Google Search
    {"channel": "Google Search", "campaign_id": "GS_Intent_Bootcamp", "campaign_name": "Google Ads - High Intent Bootcamps", "daily_spend_base": 240, "base_cpc": 3.80, "ctr_base": 0.042},
    {"channel": "Google Search", "campaign_id": "GS_Brand_Defense", "campaign_name": "Google Ads - Grito Labs Brand Search", "daily_spend_base": 75, "base_cpc": 1.25, "ctr_base": 0.125},
    {"channel": "Google Search", "campaign_id": "GS_Competitor_Conquest", "campaign_name": "Google Ads - Alternative Conquesting", "daily_spend_base": 110, "base_cpc": 4.10, "ctr_base": 0.028},
    
    # Meta Ads
    {"channel": "Meta Ads", "campaign_id": "Meta_Feed_CareerTransition", "campaign_name": "Meta - Career Switcher Video Stories", "daily_spend_base": 210, "base_cpc": 1.45, "ctr_base": 0.019},
    {"channel": "Meta Ads", "campaign_id": "Meta_Reels_ProjectShowcase", "campaign_name": "Meta - Reels RCA Capstone Demos", "daily_spend_base": 140, "base_cpc": 1.15, "ctr_base": 0.024},
    {"channel": "Meta Ads", "campaign_id": "Meta_Retargeting_LAL", "campaign_name": "Meta - Warm Audience & Lookalike 2%", "daily_spend_base": 95, "base_cpc": 2.10, "ctr_base": 0.038},

    # LinkedIn Ads
    {"channel": "LinkedIn Ads", "campaign_id": "LI_Sponsored_DataCareer", "campaign_name": "LinkedIn - Working Pro Upskilling", "daily_spend_base": 160, "base_cpc": 7.50, "ctr_base": 0.012},
    {"channel": "LinkedIn Ads", "campaign_id": "LI_ThoughtLeadership_RCA", "campaign_name": "LinkedIn - Root Cause Analysis Exec Guides", "daily_spend_base": 85, "base_cpc": 6.80, "ctr_base": 0.015},

    # YouTube Ads
    {"channel": "YouTube Ads", "campaign_id": "YT_Tutorial_SQLCrash", "campaign_name": "YouTube - Free SQL Masterclass Promo", "daily_spend_base": 130, "base_cpc": 0.95, "ctr_base": 0.021},
    {"channel": "YouTube Ads", "campaign_id": "YT_Alumni_Interviews", "campaign_name": "YouTube - Student Career Transformation", "daily_spend_base": 90, "base_cpc": 1.10, "ctr_base": 0.018},

    # Organic & Owned (Non-paid ad spend = 0, but operational effort tracking)
    {"channel": "Email Marketing", "campaign_id": "Email_Nurture_Drip", "campaign_name": "Email - 7-Day Curriculum Deep Dive", "daily_spend_base": 12, "base_cpc": 0.10, "ctr_base": 0.075},
    {"channel": "Email Marketing", "campaign_id": "Email_Webinar_Masterclass", "campaign_name": "Email - Live Weekend Workshop Invite", "daily_spend_base": 15, "base_cpc": 0.12, "ctr_base": 0.092},
    {"channel": "Organic Search", "campaign_id": "SEO_Technical_Guides", "campaign_name": "Organic - Technical Analytics Tutorials", "daily_spend_base": 0, "base_cpc": 0.0, "ctr_base": 0.045},
    {"channel": "Organic Search", "campaign_id": "SEO_Career_Roadmaps", "campaign_name": "Organic - 2026 Data Analyst Roadmap", "daily_spend_base": 0, "base_cpc": 0.0, "ctr_base": 0.052},
    {"channel": "Referral & Direct", "campaign_id": "Direct_Alumni_Network", "campaign_name": "Direct - Alumni & Referral Program", "daily_spend_base": 0, "base_cpc": 0.0, "ctr_base": 0.110}
]

PROGRAMS = {
    "DA_ACCEL": {"name": "Data Analytics Accelerator (12-Wk)", "base_price": 1250, "weight": 0.45},
    "BA_MASTER": {"name": "Business Analytics & RCA Masterclass (8-Wk)", "base_price": 950, "weight": 0.35},
    "AI_FELLOW": {"name": "Enterprise AI & BI Fellowship (16-Wk)", "base_price": 1850, "weight": 0.20}
}

DEVICE_DIST = [("Desktop", 0.52), ("Mobile", 0.43), ("Tablet", 0.05)]
LANDING_PAGES = [
    "/curriculum/data-analytics",
    "/curriculum/business-analytics-rca",
    "/fellowship/enterprise-ai-bi",
    "/free-masterclass-signup",
    "/reviews-and-alumni-outcomes",
    "/apply-now"
]

def choose_device():
    r = random.random()
    cumulative = 0
    for dev, prob in DEVICE_DIST:
        cumulative += prob
        if r <= cumulative:
            return dev
    return "Desktop"

# ------------------------------------------------------------------------------
# 1. Generate Daily Ad Spend Data
# ------------------------------------------------------------------------------
def generate_ad_spend():
    rows = []
    for day_offset in range(DAYS_COUNT):
        current_date = START_DATE + timedelta(days=day_offset)
        date_str = current_date.strftime("%Y-%m-%d")
        is_weekend = current_date.weekday() >= 5
        
        # Monthly marketing push (days 24-30 have higher urgency / spend)
        month_end_mult = 1.25 if current_date.day >= 24 else 1.0
        weekend_mult = 0.85 if is_weekend else 1.05
        
        for camp in CAMPAIGNS:
            spend_base = camp["daily_spend_base"]
            if spend_base == 0:
                # Organic / Referral has 0 media spend
                daily_spend = 0.0
                impressions = int(random.uniform(800, 2400) * weekend_mult)
                clicks = int(impressions * camp["ctr_base"] * random.uniform(0.9, 1.15))
                cpc = 0.0
            else:
                noise = random.uniform(0.88, 1.14)
                daily_spend = round(spend_base * month_end_mult * weekend_mult * noise, 2)
                cpc_noise = random.uniform(0.92, 1.08)
                cpc = round(camp["base_cpc"] * cpc_noise, 2)
                clicks = max(1, int(daily_spend / max(cpc, 0.05)))
                ctr = camp["ctr_base"] * random.uniform(0.92, 1.10)
                impressions = int(clicks / ctr)
            
            rows.append({
                "spend_date": date_str,
                "channel": camp["channel"],
                "campaign_id": camp["campaign_id"],
                "campaign_name": camp["campaign_name"],
                "impressions": impressions,
                "clicks": clicks,
                "spend_usd": daily_spend,
                "cpc_usd": round(daily_spend / clicks, 2) if clicks > 0 else 0.0,
                "ctr_pct": round((clicks / impressions) * 100, 2) if impressions > 0 else 0.0
            })
    return rows

# ------------------------------------------------------------------------------
# 2. Generate Customer Touchpoints & Conversion Journeys
# ------------------------------------------------------------------------------
def generate_customer_journeys():
    touchpoints = []
    conversions = []
    retention_cohorts = []

    # Channel affinity transition probabilities for realistic journey paths
    # Top of funnel -> Mid funnel -> Conversion
    awareness_channels = ["YouTube Ads", "Meta Ads", "Organic Search"]
    mid_funnel_channels = ["Email Marketing", "Meta Ads", "Google Search", "LinkedIn Ads"]
    closing_channels = ["Google Search", "Email Marketing", "Referral & Direct"]

    total_prospects = 4800
    order_counter = 1001

    for uid_num in range(1, total_prospects + 1):
        user_id = f"USR_{uid_num:05d}"
        
        # Decide if this user will convert
        # Higher probability if multi-touch
        will_convert = random.random() < 0.285  # ~1,368 converted students
        
        # Journey duration
        start_day_offset = random.randint(0, DAYS_COUNT - 35)
        user_start_time = START_DATE + timedelta(days=start_day_offset, hours=random.randint(8, 22), minutes=random.randint(0, 59))
        
        if will_convert:
            num_touches = random.choices([1, 2, 3, 4, 5, 6, 7], weights=[0.12, 0.24, 0.32, 0.18, 0.08, 0.04, 0.02])[0]
        else:
            num_touches = random.choices([1, 2, 3, 4], weights=[0.55, 0.28, 0.12, 0.05])[0]

        curr_time = user_start_time
        user_channels = []

        for seq in range(1, num_touches + 1):
            session_id = f"SES_{uid_num:05d}_{seq}"
            
            # Channel selection based on sequence stage
            if seq == 1:
                channel = random.choices(
                    ["Meta Ads", "YouTube Ads", "Organic Search", "Google Search", "LinkedIn Ads", "Referral & Direct"],
                    weights=[0.32, 0.22, 0.18, 0.14, 0.10, 0.04]
                )[0]
            elif seq == num_touches and will_convert:
                # Last touch prior to enrollment
                channel = random.choices(
                    ["Google Search", "Email Marketing", "Referral & Direct", "Meta Ads", "Organic Search"],
                    weights=[0.38, 0.26, 0.16, 0.12, 0.08]
                )[0]
            else:
                # Mid-journey nurture
                channel = random.choices(
                    ["Email Marketing", "Meta Ads", "Google Search", "LinkedIn Ads", "YouTube Ads", "Organic Search"],
                    weights=[0.34, 0.24, 0.18, 0.10, 0.08, 0.06]
                )[0]

            # Pick matching campaign
            available_camps = [c for c in CAMPAIGNS if c["channel"] == channel]
            chosen_camp = random.choice(available_camps)
            
            landing_page = random.choice(LANDING_PAGES)
            device = choose_device()
            
            touchpoints.append({
                "touchpoint_id": f"TP_{uid_num:05d}_{seq}",
                "user_id": user_id,
                "session_id": session_id,
                "timestamp": curr_time.strftime("%Y-%m-%d %H:%M:%S"),
                "touch_date": curr_time.strftime("%Y-%m-%d"),
                "channel": channel,
                "campaign_id": chosen_camp["campaign_id"],
                "campaign_name": chosen_camp["campaign_name"],
                "interaction_seq": seq,
                "device_category": device,
                "landing_page": landing_page,
                "session_duration_sec": int(random.uniform(45, 780)),
                "pages_viewed": random.randint(1, 8),
                "has_form_submit": 1 if (seq >= 2 and random.random() < 0.45) or (will_convert and seq == num_touches) else 0
            })

            user_channels.append(channel)
            
            # Advance time for next touchpoint (gap between touches: 6 hours to 7 days)
            gap_days = random.choices([0.25, 1, 2, 3, 5, 8], weights=[0.2, 0.25, 0.25, 0.15, 0.10, 0.05])[0]
            curr_time += timedelta(days=gap_days, hours=random.randint(1, 12))

        # Handle Conversion
        if will_convert:
            order_id = f"ORD_{order_counter}"
            order_counter += 1
            
            # Conversion occurs 15 mins to 24 hrs after final touchpoint
            conv_time = curr_time + timedelta(minutes=random.randint(15, 720))
            
            # Select program
            prog_key = random.choices(list(PROGRAMS.keys()), weights=[PROGRAMS[k]["weight"] for k in PROGRAMS])[0]
            prog_info = PROGRAMS[prog_key]
            base_price = prog_info["base_price"]
            
            # Discount code application (Early bird, Referral, Alumni scholarship)
            discount = 0
            has_coupon = random.random() < 0.42
            if has_coupon:
                discount_pct = random.choice([0.10, 0.15, 0.20])
                discount = round(base_price * discount_pct, 2)
            
            net_revenue = round(base_price - discount, 2)
            payment_mode = random.choices(
                ["Credit Card / Debit", "EMI / Installments", "Corporate Sponsorship", "UPI / NetBanking"],
                weights=[0.48, 0.32, 0.06, 0.14]
            )[0]

            conversions.append({
                "order_id": order_id,
                "user_id": user_id,
                "conversion_timestamp": conv_time.strftime("%Y-%m-%d %H:%M:%S"),
                "conversion_date": conv_time.strftime("%Y-%m-%d"),
                "program_code": prog_key,
                "program_name": prog_info["name"],
                "gross_revenue_usd": base_price,
                "discount_usd": discount,
                "net_revenue_usd": net_revenue,
                "payment_mode": payment_mode,
                "journey_length_touches": num_touches,
                "first_touch_channel": user_channels[0],
                "last_touch_channel": user_channels[-1],
                "journey_path": " > ".join(user_channels)
            })

            # Post-purchase engagement & 12-month LTV (Customer Retention Cohort)
            # Some students purchase follow-up masterclasses, interview bootcamps, or refer friends
            completed_capstone = 1 if random.random() < 0.84 else 0
            upsell_converted = 1 if (completed_capstone and random.random() < 0.24) else 0
            upsell_rev = 450.0 if upsell_converted else 0.0
            referrals_made = random.choices([0, 1, 2, 3], weights=[0.72, 0.19, 0.07, 0.02])[0]
            referral_comm_cost = referrals_made * 75.0
            
            total_12m_ltv = net_revenue + upsell_rev

            retention_cohorts.append({
                "user_id": user_id,
                "order_id": order_id,
                "enrollment_cohort_month": conv_time.strftime("%Y-%m"),
                "completed_capstone": completed_capstone,
                "nps_rating": random.choices([10, 9, 8, 7, 6], weights=[0.45, 0.35, 0.12, 0.05, 0.03])[0],
                "upsell_program_enrolled": "Advanced RCA Case Lab" if upsell_converted else "None",
                "upsell_revenue_usd": upsell_rev,
                "referrals_generated": referrals_made,
                "referral_incentive_usd": referral_comm_cost,
                "total_customer_ltv_usd": round(total_12m_ltv, 2),
                "is_active_alumni_network": 1 if completed_capstone and random.random() < 0.78 else 0
            })

    return touchpoints, conversions, retention_cohorts

# ------------------------------------------------------------------------------
# 3. Main Generator Execution & Database Persistence
# ------------------------------------------------------------------------------
def main():
    print("Generating Grito Labs Marketing Analytics Datasets...")
    
    # 1. Ad Spend
    ad_spend_rows = generate_ad_spend()
    ad_spend_file = os.path.join(DATA_RAW_DIR, "ad_spend_daily.csv")
    with open(ad_spend_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(ad_spend_rows[0].keys()))
        writer.writeheader()
        writer.writerows(ad_spend_rows)
    print(f" -> Generated {len(ad_spend_rows)} daily ad spend records -> {ad_spend_file}")

    # 2. Customer Journeys & Conversions
    touchpoints, conversions, retention = generate_customer_journeys()
    
    tp_file = os.path.join(DATA_RAW_DIR, "web_touchpoints.csv")
    with open(tp_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(touchpoints[0].keys()))
        writer.writeheader()
        writer.writerows(touchpoints)
    print(f" -> Generated {len(touchpoints)} user touchpoints -> {tp_file}")

    conv_file = os.path.join(DATA_RAW_DIR, "conversions_and_orders.csv")
    with open(conv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(conversions[0].keys()))
        writer.writeheader()
        writer.writerows(conversions)
    print(f" -> Generated {len(conversions)} student enrollments/conversions -> {conv_file}")

    ret_file = os.path.join(DATA_RAW_DIR, "customer_retention_cohorts.csv")
    with open(ret_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(retention[0].keys()))
        writer.writeheader()
        writer.writerows(retention)
    print(f" -> Generated {len(retention)} retention/LTV cohort records -> {ret_file}")

    # 3. Load into SQLite Database for instant SQL query testing
    print(f"Loading data into relational database: {DB_PATH} ...")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # DDL
    cur.execute("""
    CREATE TABLE ad_spend_daily (
        spend_date DATE,
        channel VARCHAR(64),
        campaign_id VARCHAR(64),
        campaign_name VARCHAR(128),
        impressions INTEGER,
        clicks INTEGER,
        spend_usd REAL,
        cpc_usd REAL,
        ctr_pct REAL
    );
    """)

    cur.execute("""
    CREATE TABLE web_touchpoints (
        touchpoint_id VARCHAR(32) PRIMARY KEY,
        user_id VARCHAR(32),
        session_id VARCHAR(32),
        timestamp TIMESTAMP,
        touch_date DATE,
        channel VARCHAR(64),
        campaign_id VARCHAR(64),
        campaign_name VARCHAR(128),
        interaction_seq INTEGER,
        device_category VARCHAR(32),
        landing_page VARCHAR(128),
        session_duration_sec INTEGER,
        pages_viewed INTEGER,
        has_form_submit INTEGER
    );
    """)

    cur.execute("""
    CREATE TABLE conversions_and_orders (
        order_id VARCHAR(32) PRIMARY KEY,
        user_id VARCHAR(32),
        conversion_timestamp TIMESTAMP,
        conversion_date DATE,
        program_code VARCHAR(32),
        program_name VARCHAR(128),
        gross_revenue_usd REAL,
        discount_usd REAL,
        net_revenue_usd REAL,
        payment_mode VARCHAR(64),
        journey_length_touches INTEGER,
        first_touch_channel VARCHAR(64),
        last_touch_channel VARCHAR(64),
        journey_path TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE customer_retention_cohorts (
        user_id VARCHAR(32) PRIMARY KEY,
        order_id VARCHAR(32),
        enrollment_cohort_month VARCHAR(16),
        completed_capstone INTEGER,
        nps_rating INTEGER,
        upsell_program_enrolled VARCHAR(64),
        upsell_revenue_usd REAL,
        referrals_generated INTEGER,
        referral_incentive_usd REAL,
        total_customer_ltv_usd REAL,
        is_active_alumni_network INTEGER
    );
    """)

    # Populate
    cur.executemany("""
        INSERT INTO ad_spend_daily VALUES (:spend_date, :channel, :campaign_id, :campaign_name, :impressions, :clicks, :spend_usd, :cpc_usd, :ctr_pct);
    """, ad_spend_rows)

    cur.executemany("""
        INSERT INTO web_touchpoints VALUES (:touchpoint_id, :user_id, :session_id, :timestamp, :touch_date, :channel, :campaign_id, :campaign_name, :interaction_seq, :device_category, :landing_page, :session_duration_sec, :pages_viewed, :has_form_submit);
    """, touchpoints)

    cur.executemany("""
        INSERT INTO conversions_and_orders VALUES (:order_id, :user_id, :conversion_timestamp, :conversion_date, :program_code, :program_name, :gross_revenue_usd, :discount_usd, :net_revenue_usd, :payment_mode, :journey_length_touches, :first_touch_channel, :last_touch_channel, :journey_path);
    """, conversions)

    cur.executemany("""
        INSERT INTO customer_retention_cohorts VALUES (:user_id, :order_id, :enrollment_cohort_month, :completed_capstone, :nps_rating, :upsell_program_enrolled, :upsell_revenue_usd, :referrals_generated, :referral_incentive_usd, :total_customer_ltv_usd, :is_active_alumni_network);
    """, retention)

    # Create Indexes for fast analytical queries
    cur.execute("CREATE INDEX idx_tp_user ON web_touchpoints (user_id);")
    cur.execute("CREATE INDEX idx_tp_channel ON web_touchpoints (channel);")
    cur.execute("CREATE INDEX idx_tp_date ON web_touchpoints (touch_date);")
    cur.execute("CREATE INDEX idx_conv_user ON conversions_and_orders (user_id);")
    cur.execute("CREATE INDEX idx_spend_channel ON ad_spend_daily (channel);")

    conn.commit()
    conn.close()

    print(f"Data generation and database population completed successfully!")

if __name__ == "__main__":
    main()
