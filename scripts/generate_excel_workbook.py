"""
================================================================================
Grito Labs - Multi-Channel Marketing Attribution Financial Model
Generates Boardroom-Ready Excel Workbook (.xlsx) with xlsxwriter
================================================================================
"""

import os
import csv
import sqlite3
import xlsxwriter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
DB_PATH = os.path.join(BASE_DIR, "data", "grito_marketing_analytics.db")
OUTPUT_XLSX = os.path.join(BASE_DIR, "data", "Grito_Labs_Marketing_Attribution_Model.xlsx")

def create_workbook():
    print(f"Generating Executive Financial Model: {OUTPUT_XLSX} ...")
    wb = xlsxwriter.Workbook(OUTPUT_XLSX)

    # Professional Palettes: Deep Navy (#1E293B), Electric Indigo (#4F46E5), Slate Gray (#64748B), Soft Gray (#F8FAFC)
    fmt_title = wb.add_format({'bold': True, 'font_size': 16, 'font_color': '#1E293B'})
    fmt_subtitle = wb.add_format({'italic': True, 'font_size': 10, 'font_color': '#64748B'})
    fmt_kpi_card_title = wb.add_format({'font_size': 9, 'bold': True, 'font_color': '#64748B', 'bg_color': '#F1F5F9', 'border': 1, 'border_color': '#CBD5E1', 'align': 'center'})
    fmt_kpi_card_val = wb.add_format({'font_size': 14, 'bold': True, 'font_color': '#0F172A', 'bg_color': '#F8FAFC', 'border': 1, 'border_color': '#CBD5E1', 'align': 'center'})

    fmt_header = wb.add_format({
        'bold': True, 'font_size': 10, 'font_color': '#FFFFFF', 
        'bg_color': '#1E293B', 'border': 1, 'border_color': '#334155', 
        'align': 'center', 'valign': 'vcenter', 'text_wrap': True
    })
    fmt_header_accent = wb.add_format({
        'bold': True, 'font_size': 10, 'font_color': '#FFFFFF', 
        'bg_color': '#4F46E5', 'border': 1, 'border_color': '#4338CA', 
        'align': 'center', 'valign': 'vcenter', 'text_wrap': True
    })

    fmt_text = wb.add_format({'font_size': 10, 'font_color': '#334155', 'border': 1, 'border_color': '#E2E8F0'})
    fmt_text_bold = wb.add_format({'bold': True, 'font_size': 10, 'font_color': '#0F172A', 'border': 1, 'border_color': '#CBD5E1', 'bg_color': '#F8FAFC'})
    fmt_num = wb.add_format({'font_size': 10, 'font_color': '#334155', 'border': 1, 'border_color': '#E2E8F0', 'num_format': '#,##0'})
    fmt_currency = wb.add_format({'font_size': 10, 'font_color': '#334155', 'border': 1, 'border_color': '#E2E8F0', 'num_format': '$#,##0.00'})
    fmt_currency_bold = wb.add_format({'bold': True, 'font_size': 10, 'font_color': '#0F172A', 'border': 1, 'border_color': '#CBD5E1', 'bg_color': '#F8FAFC', 'num_format': '$#,##0.00'})
    fmt_percent = wb.add_format({'font_size': 10, 'font_color': '#334155', 'border': 1, 'border_color': '#E2E8F0', 'num_format': '0.0%'})
    fmt_decimal = wb.add_format({'font_size': 10, 'font_color': '#334155', 'border': 1, 'border_color': '#E2E8F0', 'num_format': '0.00'})
    fmt_decimal_bold = wb.add_format({'bold': True, 'font_size': 10, 'font_color': '#0F172A', 'border': 1, 'border_color': '#CBD5E1', 'bg_color': '#F8FAFC', 'num_format': '0.00'})

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # --------------------------------------------------------------------------
    # Tab 1: Executive Summary
    # --------------------------------------------------------------------------
    ws1 = wb.add_worksheet("Executive Overview")
    ws1.set_column('A:A', 4)
    ws1.set_column('B:G', 22)

    ws1.write('B2', "GRITO LABS | MULTI-CHANNEL ATTRIBUTION & ROI DASHBOARD", fmt_title)
    ws1.write('B3', "Marketing Capital Allocation & Attribution Performance Audit (H1 2026)", fmt_subtitle)

    # Fetch high-level KPIs
    cur.execute("SELECT SUM(spend_usd) as spend, SUM(clicks) as clicks, SUM(impressions) as impr FROM ad_spend_daily")
    spend_row = cur.fetchone()
    total_spend = spend_row['spend']

    cur.execute("SELECT COUNT(*) as conv, SUM(net_revenue_usd) as rev, AVG(net_revenue_usd) as aov, AVG(journey_length_touches) as avg_touches FROM conversions_and_orders")
    conv_row = cur.fetchone()
    total_conv = conv_row['conv']
    total_rev = conv_row['rev']
    blended_roas = total_rev / total_spend
    blended_cac = total_spend / total_conv

    # KPI Summary Cards
    cards = [
        ("TOTAL MEDIA SPEND", f"${total_spend:,.2f}"),
        ("GROSS REVENUE", f"${total_rev:,.2f}"),
        ("BLENDED ROAS", f"{blended_roas:.2f}x"),
        ("TOTAL ENROLLMENTS", f"{total_conv:,}"),
        ("BLENDED CAC", f"${blended_cac:.2f}"),
        ("AVG TOUCHES / STUDENT", f"{conv_row['avg_touches']:.2f}")
    ]

    col_idx = 1
    for title, val in cards:
        ws1.write(4, col_idx, title, fmt_kpi_card_title)
        ws1.write(5, col_idx, val, fmt_kpi_card_val)
        col_idx += 1

    ws1.write('B8', "Key Executive Findings & Attribution Distortion Summary:", wb.add_format({'bold': True, 'font_size': 12, 'font_color': '#1E293B'}))
    bullets = [
        "1. Extreme Last-Touch Bias: Google Search is over-credited by +48% in Last-Touch ($589.7k vs $395.2k in Markov), masking Meta & YouTube top-of-funnel discovery.",
        "2. The Hidden Hero: Email Marketing drives $250.4k in algorithmic value with only $5.2k spend (ROAS: 48.0x) due to its high conversion assistance removal effect (0.2765).",
        "3. Capital Drain Identified: LinkedIn Ads generates an unsustainable CAC of $547.62 (ROAS: 2.16x) due to steep $7.40 CPCs. Reallocating $19k from LinkedIn unlocks +$74.9k incremental revenue.",
        "4. Organic Pillar: Organic Search & Alumni Referrals drive 305+ organic student enrollments ($360.4k net tuition) at $0 paid acquisition cost.",
        "5. Conversion Velocity: Average student consideration journey takes 3.4 touchpoints over 14.8 days between initial discovery and tuition payment."
    ]
    for i, b in enumerate(bullets):
        ws1.write(8 + i, 1, b, wb.add_format({'font_size': 10, 'font_color': '#334155'}))

    # --------------------------------------------------------------------------
    # Tab 2: Attribution Model Comparison
    # --------------------------------------------------------------------------
    ws2 = wb.add_worksheet("Attribution Models")
    ws2.set_column('A:A', 4)
    ws2.set_column('B:B', 22)
    ws2.set_column('C:E', 15)
    ws2.set_column('F:Q', 14)

    ws2.write('B2', "MULTI-TOUCH ATTRIBUTION MODEL COMPARISON MATRIX", fmt_title)
    ws2.write('B3', "Evaluating Conversions, Revenue, ROAS, and CAC Across 6 Methodologies", fmt_subtitle)

    headers = [
        "Channel", "Media Spend ($)", "Markov Removal Effect",
        "Conv (First-Touch)", "Conv (Last-Touch)", "Conv (Linear)", "Conv (Time-Decay)", "Conv (U-Shaped)", "Conv (Markov)",
        "Rev (First-Touch)", "Rev (Last-Touch)", "Rev (Linear)", "Rev (Time-Decay)", "Rev (U-Shaped)", "Rev (Markov)",
        "Markov ROAS", "Markov CAC ($)"
    ]
    for col, h in enumerate(headers):
        f = fmt_header_accent if "Markov" in h else fmt_header
        ws2.write(4, col + 1, h, f)

    cur.execute("SELECT * FROM attribution_model_comparison ORDER BY total_spend_usd DESC")
    rows = cur.fetchall()
    r_idx = 5
    for r in rows:
        ws2.write(r_idx, 1, r['channel'], fmt_text_bold)
        ws2.write(r_idx, 2, r['total_spend_usd'], fmt_currency)
        ws2.write(r_idx, 3, r['markov_removal_effect'], fmt_decimal)
        ws2.write(r_idx, 4, r['conv_first_touch'], fmt_decimal)
        ws2.write(r_idx, 5, r['conv_last_touch'], fmt_decimal)
        ws2.write(r_idx, 6, r['conv_linear'], fmt_decimal)
        ws2.write(r_idx, 7, r['conv_time_decay'], fmt_decimal)
        ws2.write(r_idx, 8, r['conv_u_shaped'], fmt_decimal)
        ws2.write(r_idx, 9, r['conv_markov_chain'], fmt_decimal_bold)
        ws2.write(r_idx, 10, r['rev_first_touch'], fmt_currency)
        ws2.write(r_idx, 11, r['rev_last_touch'], fmt_currency)
        ws2.write(r_idx, 12, r['rev_linear'], fmt_currency)
        ws2.write(r_idx, 13, r['rev_time_decay'], fmt_currency)
        ws2.write(r_idx, 14, r['rev_u_shaped'], fmt_currency)
        ws2.write(r_idx, 15, r['rev_markov_chain'], fmt_currency_bold)
        ws2.write(r_idx, 16, r['markov_roas'], fmt_decimal_bold)
        ws2.write(r_idx, 17, r['markov_cac'], fmt_currency_bold)
        r_idx += 1

    # Total Row
    ws2.write(r_idx, 1, "TOTAL / BLENDED", fmt_text_bold)
    ws2.write(r_idx, 2, f"=SUM(C6:C{r_idx})", fmt_currency_bold)
    ws2.write(r_idx, 3, "-", fmt_text_bold)
    for c_i in range(4, 10):
        col_letter = chr(ord('A') + c_i)
        ws2.write(r_idx, c_i, f"=SUM({col_letter}6:{col_letter}{r_idx})", fmt_decimal_bold)
    for c_i in range(10, 16):
        col_letter = chr(ord('A') + c_i)
        ws2.write(r_idx, c_i, f"=SUM({col_letter}6:{col_letter}{r_idx})", fmt_currency_bold)
    ws2.write(r_idx, 16, f"=P{r_idx+1}/C{r_idx+1}", fmt_decimal_bold)
    ws2.write(r_idx, 17, f"=C{r_idx+1}/J{r_idx+1}", fmt_currency_bold)

    # --------------------------------------------------------------------------
    # Tab 3: Budget Reallocation Strategy
    # --------------------------------------------------------------------------
    ws3 = wb.add_worksheet("Budget Optimization")
    ws3.set_column('A:A', 4)
    ws3.set_column('B:B', 20)
    ws3.set_column('C:E', 16)
    ws3.set_column('F:I', 15)
    ws3.set_column('J:J', 48)

    ws3.write('B2', "MATHEMATICAL BUDGET REALLOCATION (HILL-MARKOV MODEL)", fmt_title)
    ws3.write('B3', "Projected +$74.9k Revenue Uplift (+5.9% Conversions) with Zero Increase in Media Budget", fmt_subtitle)

    headers3 = [
        "Channel", "Current Spend ($)", "Optimized Spend ($)", "Budget Shift ($)", "Shift (%)",
        "Current Markov Conv", "Projected Conv", "Current Revenue ($)", "Projected Revenue ($)", "Projected ROAS", "Strategic Rationale"
    ]
    for col, h in enumerate(headers3):
        ws3.write(4, col + 1, h, fmt_header_accent if "Optimized" in h or "Projected" in h else fmt_header)

    strat_file = os.path.join(DATA_PROC_DIR, "budget_reallocation_strategy.csv")
    r_idx = 5
    with open(strat_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            ws3.write(r_idx, 1, r['channel'], fmt_text_bold)
            ws3.write(r_idx, 2, float(r['current_spend_usd']), fmt_currency)
            ws3.write(r_idx, 3, float(r['optimized_spend_usd']), fmt_currency_bold)
            ws3.write(r_idx, 4, float(r['budget_shift_usd']), fmt_currency)
            ws3.write(r_idx, 5, float(r['budget_shift_pct']) / 100.0, fmt_percent)
            ws3.write(r_idx, 6, float(r['current_markov_conv']), fmt_decimal)
            ws3.write(r_idx, 7, float(r['projected_conv']), fmt_decimal_bold)
            ws3.write(r_idx, 8, float(r['current_markov_rev']), fmt_currency)
            ws3.write(r_idx, 9, float(r['projected_rev']), fmt_currency_bold)
            ws3.write(r_idx, 10, float(r['projected_roas']), fmt_decimal_bold)
            ws3.write(r_idx, 11, r['strategic_rationale'], fmt_text)
            r_idx += 1

    # --------------------------------------------------------------------------
    # Tab 4: Campaign Deep-Dive
    # --------------------------------------------------------------------------
    ws4 = wb.add_worksheet("Campaign Deep-Dive")
    ws4.set_column('A:A', 4)
    ws4.set_column('B:C', 26)
    ws4.set_column('D:D', 18)
    ws4.set_column('E:G', 14)
    ws4.set_column('H:K', 14)
    ws4.set_column('L:M', 18)
    ws4.set_column('N:N', 42)

    ws4.write('B2', "GRANULAR CAMPAIGN PERFORMANCE AUDIT", fmt_title)
    ws4.write('B3', "Linear vs Last-Touch Return on Ad Spend, Cost Per Acquisition, and Strategic Health", fmt_subtitle)

    headers4 = [
        "Campaign ID", "Campaign Name", "Channel", "Spend ($)", "Impressions", "Clicks",
        "CTR (%)", "CPC ($)", "Linear Conv", "Linear Rev ($)", "Linear ROAS", "Linear CAC ($)", "Status", "Recommendation"
    ]
    for col, h in enumerate(headers4):
        ws4.write(4, col + 1, h, fmt_header)

    cur.execute("SELECT * FROM campaign_roi_deepdive ORDER BY spend_usd DESC")
    rows4 = cur.fetchall()
    r_idx = 5
    for r in rows4:
        ws4.write(r_idx, 1, r['campaign_id'], fmt_text)
        ws4.write(r_idx, 2, r['campaign_name'], fmt_text_bold)
        ws4.write(r_idx, 3, r['channel'], fmt_text)
        ws4.write(r_idx, 4, r['spend_usd'], fmt_currency)
        ws4.write(r_idx, 5, r['impressions'], fmt_num)
        ws4.write(r_idx, 6, r['clicks'], fmt_num)
        ws4.write(r_idx, 7, r['ctr_pct'] / 100.0, fmt_percent)
        ws4.write(r_idx, 8, r['cpc_usd'], fmt_currency)
        ws4.write(r_idx, 9, r['conversions_linear'], fmt_decimal)
        ws4.write(r_idx, 10, r['revenue_linear'], fmt_currency)
        ws4.write(r_idx, 11, r['roas_linear'], fmt_decimal_bold)
        ws4.write(r_idx, 12, r['cac_linear_usd'], fmt_currency)
        ws4.write(r_idx, 13, r['efficiency_status'], fmt_text_bold)
        ws4.write(r_idx, 14, r['strategic_recommendation'], fmt_text)
        r_idx += 1

    # --------------------------------------------------------------------------
    # Tab 5: Journey Path Analysis
    # --------------------------------------------------------------------------
    ws5 = wb.add_worksheet("Customer Journey Paths")
    ws5.set_column('A:A', 4)
    ws5.set_column('B:B', 50)
    ws5.set_column('C:G', 18)

    ws5.write('B2', "HIGH-IMPACT CUSTOMER CONVERSION JOURNEYS", fmt_title)
    ws5.write('B3', "Multi-Touch Transition Paths, Touchpoint Count, and Path Conversion Rates", fmt_subtitle)

    headers5 = ["Journey Path", "Touchpoint Count", "Total Prospects", "Conversions", "CVR (%)", "Total Net Revenue ($)"]
    for col, h in enumerate(headers5):
        ws5.write(4, col + 1, h, fmt_header)

    paths_file = os.path.join(DATA_PROC_DIR, "customer_journey_paths.csv")
    r_idx = 5
    with open(paths_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for r in reader:
            if count >= 25: break
            ws5.write(r_idx, 1, r['journey_path'], fmt_text)
            ws5.write(r_idx, 2, int(r['touchpoints_count']), fmt_num)
            ws5.write(r_idx, 3, int(r['total_prospects']), fmt_num)
            ws5.write(r_idx, 4, int(r['total_conversions']), fmt_num)
            ws5.write(r_idx, 5, float(r['conversion_rate_pct']) / 100.0, fmt_percent)
            ws5.write(r_idx, 6, float(r['total_net_revenue_usd']), fmt_currency)
            r_idx += 1
            count += 1

    conn.close()
    wb.close()
    print("Excel financial model generated successfully!")

if __name__ == "__main__":
    create_workbook()
