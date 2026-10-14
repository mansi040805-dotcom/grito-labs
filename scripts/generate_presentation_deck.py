"""
================================================================================
Grito Labs - Multi-Channel Marketing Attribution & ROI Analytics
Boardroom-Ready Executive Presentation Deck Generator (.pptx)
================================================================================
Generates 14 custom-formatted executive slides using python-pptx:
1. Title & Executive Overview
2. Strategic Context & Business Problem
3. Multi-Touch Student Journey Architecture
4. Heuristic Models vs. Algorithmic Markov Chains
5. Markov Removal Effect Derivation
6. 6-Model Attribution Comparison Matrix
7. ROAS, CAC, and Blended Unit Economics
8. Campaign-Level Efficiency & Cannibalization
9. Top Multi-Touch Conversion Paths
10. Cohort Retention & 12-Month LTV Analysis
11. Mathematical Budget Reallocation (+74.9k Uplift)
12. Sensitivity Analysis (iOS 14.5 ATT & Cookie Deprecation)
13. 90-Day Implementation & Experimentation Roadmap
14. Executive Recommendations & Decision Checklist
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PPTX = os.path.join(BASE_DIR, "presentation", "Grito_Labs_Marketing_Attribution_Deck.pptx")

# Executive Palette
C_NAVY_DARK = RGBColor(15, 23, 42)      # #0F172A
C_NAVY_SLATE = RGBColor(30, 41, 59)     # #1E293B
C_BLUE_ACCENT = RGBColor(59, 130, 246)  # #3B82F6
C_BLUE_LIGHT = RGBColor(239, 246, 255)  # #EFF6FF
C_TEXT_LIGHT = RGBColor(248, 250, 252)  # #F8FAFC
C_TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8
C_TEXT_DARK = RGBColor(15, 23, 42)
C_CARD_BG = RGBColor(241, 245, 249)     # #F1F5F9
C_GREEN = RGBColor(16, 185, 129)        # #10B981
C_RED = RGBColor(244, 63, 94)           # #F43F5E
C_BORDER = RGBColor(203, 213, 225)      # #CBD5E1

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 Widescreen
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title, category="GRITO LABS | MARKETING ANALYTICS & ATTRIBUTION"):
        # Category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_c = tf_cat.paragraphs[0]
        p_c.text = category.upper()
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = C_BLUE_ACCENT

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.5), Inches(0.6))
        tf = t_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_DARK

    def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
        return shape

    # ==========================================================================
    # Slide 1: Title Slide (Dark Boardroom Aesthetic)
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY_DARK
    bg1.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(3.5))
    tf = tb.text_frame
    
    p0 = tf.paragraphs[0]
    p0.text = "MARKETING ANALYTICS & ATTRIBUTION FRAMEWORK"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = C_BLUE_ACCENT
    p0.space_after = Pt(12)

    p1 = tf.add_paragraph()
    p1.text = "Multi-Channel Marketing Attribution\n& ROI Optimization Framework"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT_LIGHT
    p1.space_after = Pt(16)

    p2 = tf.add_paragraph()
    p2.text = "Evaluating Cross-Channel Customer Journeys, Algorithmic Markov Attribution, and Capital Reallocation Strategy"
    p2.font.size = Pt(15)
    p2.font.color.rgb = C_TEXT_MUTED
    p2.space_after = Pt(28)

    p3 = tf.add_paragraph()
    p3.text = "Prepared for Grito Labs Executive Leadership | H1 2026 Analytical Review"
    p3.font.size = Pt(12)
    p3.font.color.rgb = RGBColor(203, 213, 225)

    # ==========================================================================
    # Slide 2: Executive Summary & Core Verdict
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Summary: The Last-Touch Fallacy & Capital Opportunity")

    # 4 Top KPI Cards
    kpi_defs = [
        ("TOTAL MEDIA SPEND", "$262,896.68", "Across 6 Months (15 Campaigns)", C_NAVY_SLATE),
        ("NET TUITION REVENUE", "$1,646,260.00", "1,385 Enrolled Students", C_BLUE_ACCENT),
        ("BLENDED ROAS", "6.26x", "Total Net Tuition / Media Spend", C_GREEN),
        ("PROJECTED UPLIFT", "+$74,941.99", "With $0 Extra Media Investment", C_GREEN)
    ]
    for i, (title, val, sub, col) in enumerate(kpi_defs):
        left = Inches(0.8 + i * 2.95)
        add_card(s2, left, Inches(1.4), Inches(2.8), Inches(1.4))
        tb = s2.shapes.add_textbox(left + Inches(0.1), Inches(1.5), Inches(2.6), Inches(1.2))
        tf = tb.text_frame
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(9)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TEXT_MUTED
        
        p_v = tf.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(20)
        p_v.font.bold = True
        p_v.font.color.rgb = col

        p_s = tf.add_paragraph()
        p_s.text = sub
        p_s.font.size = Pt(8.5)
        p_s.font.color.rgb = C_NAVY_SLATE

    # 3 Strategic Takeaway Cards Below
    takes = [
        ("1. Severe Last-Touch Attribution Bias", 
         "Standard Last-Touch Attribution (LTA) over-allocates +48% of commercial credit ($589.7k vs $395.2k) to Google Search and Direct. This misleads leadership into believing discovery channels (Meta, YouTube) are unviable, when in fact they originate 64% of all converting paths."),
        ("2. Email Marketing is the Primary ROI Driver",
         "Email nurture sequences contribute $250.4k in algorithmic revenue at a marginal media spend of just $5.2k (ROAS: 47.98x). Email holds a critical 0.2765 Markov Removal Effect, acting as the indispensable mid-funnel converter of warm leads."),
        ("3. High-Cost Capital Drain on LinkedIn Ads",
         "LinkedIn Ads absorbs $47.5k in spend but yields only 86.6 Markov conversions ($547.62 CAC vs $245.03 on Google Search). Shifting $19.0k away from LinkedIn into Email, YouTube, and Google Search unlocks +63.5 incremental students and +$74.9k revenue.")
    ]
    for i, (head, body) in enumerate(takes):
        top = Inches(3.1 + i * 1.35)
        add_card(s2, Inches(0.8), top, Inches(11.7), Inches(1.2))
        tb = s2.shapes.add_textbox(Inches(1.0), top + Inches(0.1), Inches(11.3), Inches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = C_NAVY_DARK
        
        p_b = tf.add_paragraph()
        p_b.text = body
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = C_NAVY_SLATE

    # ==========================================================================
    # Slide 3: Grito Labs Product & Student Journey Architecture
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Business Context: Grito Labs Portfolio & Decision Funnel")

    # 3 Product Columns
    prods = [
        ("Data Analytics Accelerator", "12 Weeks | SQL, Python, Power BI, RCA", "$1,250 Base Fee", "45% of Enrollments",
         "Target: Early-career freshers & career switchers seeking job-ready technical agility.\n• High discovery via Meta Reels & YouTube Crash Courses.\n• Requires hands-on curriculum proof and alumni outcome transparency."),
        ("Business Analytics & RCA Masterclass", "8 Weeks | Root Cause Analysis & Tableau", "$950 Base Fee", "35% of Enrollments",
         "Target: Working associates and business operators aiming for senior BI roles.\n• Decision cycle: 12-18 days with 3+ touchpoints.\n• High conversion via Sunday Masterclass email webinars."),
        ("Enterprise AI & BI Fellowship", "16 Weeks | Advanced GenAI & MLOps", "$1,850 Base Fee", "20% of Enrollments",
         "Target: Senior technical professionals & enterprise sponsored candidates.\n• Highest AOV product ($1,620 net tuition).\n• Highest reliance on brand credibility and peer referrals.")
    ]
    for i, (p_title, p_sub, p_price, p_share, p_desc) in enumerate(prods):
        left = Inches(0.8 + i * 3.95)
        add_card(s3, left, Inches(1.4), Inches(3.8), Inches(5.5))
        tb = s3.shapes.add_textbox(left + Inches(0.2), Inches(1.6), Inches(3.4), Inches(5.1))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = p_title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY_DARK

        p2 = tf.add_paragraph()
        p2.text = p_sub
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_TEXT_MUTED
        p2.space_after = Pt(10)

        p3 = tf.add_paragraph()
        p3.text = f"{p_price} | {p_share}"
        p3.font.size = Pt(11)
        p3.font.bold = True
        p3.font.color.rgb = C_BLUE_ACCENT
        p3.space_after = Pt(14)

        p4 = tf.add_paragraph()
        p4.text = p_desc
        p4.font.size = Pt(10)
        p4.font.color.rgb = C_NAVY_SLATE

    # ==========================================================================
    # Slide 4: The Core Problem: Why Last-Touch Attribution Fails
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "The Flaw of Heuristics: Single-Touch vs Multi-Touch Reality")

    # Left Box: Single-Touch Bias
    add_card(s4, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.5), bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    tb_l = s4.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.3), Inches(5.1))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    pl1 = tf_l.paragraphs[0]
    pl1.text = "THE DANGERS OF LAST-TOUCH ATTRIBUTION (LTA)"
    pl1.font.size = Pt(13)
    pl1.font.bold = True
    pl1.font.color.rgb = C_RED
    pl1.space_after = Pt(10)

    pl_body = [
        "• 100% Conversion Credit to Closing Click: Allocates all value to Google Search or Direct navigation, treating them as sole conversion drivers.",
        "• Systematic Defunding of Discovery Channels: Top-of-funnel channels (YouTube Ads, Meta Ads) look unprofitable (ROAS < 1.0x under LTA), leading CMOs to slash awareness budgets.",
        "• Catastrophic Delayed Pipeline Collapse: When awareness spend is cut, prospective student discovery dries up; total conversions collapse 4-6 weeks later.",
        "• Zero Credit to Mid-Funnel Nurture: Email Marketing receives 0 credit in First-Touch and gets discounted in single-touch models despite nurturing leads for weeks."
    ]
    for b in pl_body:
        p = tf_l.add_paragraph()
        p.text = b
        p.font.size = Pt(10)
        p.font.color.rgb = C_NAVY_DARK
        p.space_after = Pt(8)

    # Right Box: Multi-Touch & Algorithmic Solution
    add_card(s4, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5), bg_color=C_BLUE_LIGHT, border_color=RGBColor(191, 219, 254))
    tb_r = s4.shapes.add_textbox(Inches(7.0), Inches(1.6), Inches(5.3), Inches(5.1))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    pr1 = tf_r.paragraphs[0]
    pr1.text = "THE MULTI-TOUCH ATTRIBUTION (MTA) SOLUTION"
    pr1.font.size = Pt(13)
    pr1.font.bold = True
    pr1.font.color.rgb = C_BLUE_ACCENT
    pr1.space_after = Pt(10)

    pr_body = [
        "• Holistic Full-Funnel Valuation: Accounts for discovery (First-Touch), evaluation (Linear / Time-Decay), and transaction (Last-Touch).",
        "• Data-Driven Markov Chains: Calculates empirical removal effects by evaluating customer journey paths that convert vs those that drop out.",
        "• Objective Incrementality: Isolates true incremental contribution rather than arbitrary percentage rules (like 40-20-40).",
        "• Actionable Capital Reallocation: Directs marketing capital to channels with the highest marginal response rather than highest vanity clicks."
    ]
    for b in pr_body:
        p = tf_r.add_paragraph()
        p.text = b
        p.font.size = Pt(10)
        p.font.color.rgb = C_NAVY_DARK
        p.space_after = Pt(8)

    # ==========================================================================
    # Slide 5: Attribution Methodology Spectrum
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Methodology Spectrum: 6 Attribution Models Evaluated")

    models_info = [
        ("First-Touch (FTA)", "Rule-Based", "100% to initial touchpoint", "Rewards discovery; ignores nurture & closing.", "Awareness benchmarking"),
        ("Last-Touch (LTA)", "Rule-Based", "100% to final touchpoint", "Biased toward brand search & direct; penalizes TOFU.", "Legacy paid search"),
        ("Linear Model", "Rule-Based", "Equal credit (1 / N) to all touches", "Democratic; fails to reflect true touchpoint leverage.", "Multi-touch baseline"),
        ("Time-Decay (7d)", "Rule-Based", "Exponential half-life: 2^(-dt / 7)", "Favors recent touches; slightly discounts early ads.", "Shorter consideration cycles"),
        ("U-Shaped (40-20-40)", "Position-Based", "40% First, 40% Last, 20% Middle", "Balances discovery & closing; penalizes middle touches.", "General B2C e-commerce"),
        ("Markov Chain", "Algorithmic", "Removal Effect derived from state transitions", "Statistically rigorous; evaluates converting & drop paths.", "Boardroom Capital Allocation")
    ]

    # Create comparison table
    rows_cnt = len(models_info) + 1
    cols_cnt = 5
    table_shape = s5.shapes.add_table(rows_cnt, cols_cnt, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(1.5)
    table.columns[2].width = Inches(2.6)
    table.columns[3].width = Inches(3.2)
    table.columns[4].width = Inches(2.2)

    headers = ["Model", "Type", "Weighting Logic", "Core Weakness / Bias", "Primary Use Case"]
    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_LIGHT

    for r_idx, row in enumerate(models_info):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_BLUE_LIGHT if r_idx == 5 else (RGBColor(255, 255, 255) if r_idx % 2 == 0 else C_CARD_BG)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.bold = (r_idx == 5 and c_idx == 0)
            p.font.color.rgb = C_BLUE_ACCENT if (r_idx == 5 and c_idx == 0) else C_NAVY_DARK

    # ==========================================================================
    # Slide 6: Markov Chain Transition Matrix & Removal Effect
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Algorithmic Rigor: Markov Removal Effects Explained")

    # Left: Mathematical Formulation
    add_card(s6, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.5))
    tb_m = s6.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.3), Inches(5.1))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True

    p = tf_m.paragraphs[0]
    p.text = "MATHEMATICAL FOUNDATION"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(12)

    math_points = [
        "1. State Representation:\nEvery marketing channel represents a node in a stochastic Markov graph. Absorbing states are (Conversion) and (Drop-out).",
        "2. Transition Probability Matrix P:\nP(i, j) = C(i, j) / Σ_k C(i, k), where C(i, j) represents total student transitions from channel i to channel j.",
        "3. Baseline Conversion Probability:\nP(Conv) calculates total probability of transitioning from (Start) to (Conversion) across all existing paths.",
        "4. Removal Effect Formula:\nRE(c) = [P(Conv) - P(Conv \\ {c})] / P(Conv)\nMeasures the percentage drop in total conversions when channel c is removed from the ecosystem.",
        "5. Normalized Attribution Weight:\nW_Markov(c) = RE(c) / Σ_k RE(k)"
    ]
    for pt in math_points:
        p = tf_m.add_paragraph()
        p.text = pt
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_NAVY_SLATE
        p.space_after = Pt(8)

    # Right: Calculated Removal Effects Table
    add_card(s6, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5))
    tb_re = s6.shapes.add_textbox(Inches(7.0), Inches(1.6), Inches(5.3), Inches(5.1))
    tf_re = tb_re.text_frame
    tf_re.word_wrap = True

    p = tf_re.paragraphs[0]
    p.text = "EMPIRICAL REMOVAL EFFECTS FOR GRITO LABS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_ACCENT
    p.space_after = Pt(12)

    re_table = [
        ("Google Search", "0.4363", "43.6% conversions lost if removed", C_GREEN),
        ("Meta Ads", "0.3832", "38.3% conversions lost if removed", C_GREEN),
        ("Email Marketing", "0.2765", "27.6% conversions lost if removed", C_GREEN),
        ("Organic Search", "0.2314", "23.1% conversions lost if removed", C_BLUE_ACCENT),
        ("YouTube Ads", "0.1988", "19.9% conversions lost if removed", C_BLUE_ACCENT),
        ("Referral & Direct", "0.1665", "16.7% conversions lost if removed", C_BLUE_ACCENT),
        ("LinkedIn Ads", "0.1130", "11.3% conversions lost (Lowest leverage)", C_RED)
    ]
    for ch, val, note, col in re_table:
        p = tf_re.add_paragraph()
        p.text = f"• {ch}: {val}  —  {note}"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(6)

    # ==========================================================================
    # Slide 7: 6-Model Attribution Comparison Matrix
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Model Comparison: Conversions & Revenue by Channel")

    # Table comparing the 6 models
    attr_data = [
        ("Google Search", "$82.0k", "182.0", "496.0", "308.0", "329.9", "325.5", "334.7", "$395.2k", "4.82x"),
        ("Meta Ads", "$85.8k", "449.0", "219.0", "341.1", "322.9", "336.4", "294.0", "$347.1k", "4.05x"),
        ("YouTube Ads", "$42.5k", "317.0", "40.0", "163.7", "144.4", "172.1", "152.5", "$180.0k", "4.24x"),
        ("Email Marketing", "$5.2k", "0.0", "302.0", "235.7", "256.4", "188.7", "212.0", "$250.4k", "47.98x"),
        ("LinkedIn Ads", "$47.5k", "135.0", "17.0", "94.7", "84.9", "84.5", "86.7", "$102.3k", "2.16x"),
        ("Organic Search", "$0.0k", "246.0", "127.0", "161.5", "153.2", "175.3", "177.5", "$209.6k", "N/A"),
        ("Referral & Direct", "$0.0k", "56.0", "184.0", "80.4", "93.3", "102.5", "127.7", "$150.8k", "N/A")
    ]
    t_shape = s7.shapes.add_table(8, 10, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.4))
    tbl = t_shape.table
    widths = [Inches(1.8), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.1), Inches(1.4), Inches(1.4)]
    for idx, w in enumerate(widths):
        tbl.columns[idx].width = w

    t_heads = ["Channel", "Spend", "First", "Last", "Linear", "Decay", "U-Shape", "Markov", "Markov Rev", "Markov ROAS"]
    for c_i, h in enumerate(t_heads):
        cell = tbl.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_LIGHT

    for r_i, r in enumerate(attr_data):
        for c_i, v in enumerate(r):
            cell = tbl.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_BLUE_LIGHT if c_i in [7, 8, 9] else (RGBColor(255, 255, 255) if r_i % 2 == 0 else C_CARD_BG)
            p = cell.text_frame.paragraphs[0]
            p.text = v
            p.font.size = Pt(9)
            p.font.bold = (c_i in [0, 7, 8, 9])
            p.font.color.rgb = C_NAVY_DARK

    # ==========================================================================
    # Slide 8: Channel ROI & CAC Deep-Dive
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Channel Efficiency: Markov CAC vs ROAS Matrix")

    # 4 Quadrant / Segment Cards
    segments = [
        ("SCALE ENGINES (High ROAS, Low/Moderate CAC)", C_GREEN,
         "• Email Marketing: ROAS 47.98x | CAC $24.61\n  High conversion velocity, nurtures warm webinar and syllabus leads.\n• Google Search: ROAS 4.82x | CAC $245.03\n  Core high-intent demand harvesting pillar; captures active bootcamp searchers."),
        ("DISCOVERY DRIVERS (Moderate ROAS, High Pipeline Value)", C_BLUE_ACCENT,
         "• YouTube Ads: ROAS 4.24x | CAC $278.49\n  Originates 317 prospective student journeys; tutorial lead magnets.\n• Meta Ads: ROAS 4.05x | CAC $291.76\n  Massive reach (2.6M impressions); salary jump student testimonials."),
        ("CAPITAL BLEEDER (High CAC, Marginal ROAS)", C_RED,
         "• LinkedIn Ads: ROAS 2.16x | CAC $547.62\n  Excessive CPC ($7.40) creates steep unit economics; 40% of spend generates only 86 enrollments. Must be restructured or pruned."),
        ("ORGANIC FOUNDATION (Zero Paid CAC)", C_NAVY_SLATE,
         "• Organic Search & SEO: 177.5 Markov Conversions ($209.6k revenue)\n  RCA case studies and SQL interview prep content drive organic authority.\n• Alumni Referrals: 127.7 Markov Conversions ($150.8k revenue)\n  Strong student satisfaction (NPS 9.1) delivers zero-acquisition-cost enrollments.")
    ]
    for i, (title, color, text) in enumerate(segments):
        col_x = Inches(0.8 + (i % 2) * 5.95)
        row_y = Inches(1.4 + (i // 2) * 2.85)
        add_card(s8, col_x, row_y, Inches(5.75), Inches(2.65))
        tb = s8.shapes.add_textbox(col_x + Inches(0.2), row_y + Inches(0.15), Inches(5.35), Inches(2.35))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = color
        p1.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = text
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_NAVY_SLATE

    # ==========================================================================
    # Slide 9: Top Customer Journey Paths & Funnel Velocity
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Customer Journey Pathology: High-Impact Conversion Paths")

    paths_data = [
        ("Meta Ads > Email Marketing > Google Search", 3, 412, 148, "35.9%", "$175.2k", "Highest volume converting path (Classic discovery > nurture > closing)"),
        ("YouTube Ads > Meta Ads > Email Marketing > Google Search", 4, 328, 122, "37.2%", "$144.5k", "Comprehensive 4-touch journey; highest revenue velocity"),
        ("Organic Search > Email Marketing > Google Search", 3, 295, 105, "35.6%", "$124.8k", "High-efficiency hybrid organic-paid sequence"),
        ("YouTube Ads > Email Marketing > Referral & Direct", 3, 210, 78, "37.1%", "$92.4k", "Bootcamp lead magnet to alumni advocacy path"),
        ("Google Search (Single Touch / High Intent)", 1, 380, 68, "17.9%", "$80.5k", "Direct intent; lower conversion rate due to sticker shock without nurture"),
        ("LinkedIn Ads > Google Search", 2, 240, 32, "13.3%", "$38.0k", "Underperforming 2-touch enterprise journey")
    ]

    t_s9 = s9.shapes.add_table(7, 7, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.4))
    t_tbl = t_s9.table
    w_s9 = [Inches(3.8), Inches(0.8), Inches(1.1), Inches(1.1), Inches(1.0), Inches(1.2), Inches(2.7)]
    for idx, w in enumerate(w_s9):
        t_tbl.columns[idx].width = w

    h_s9 = ["Journey Path", "Touches", "Prospects", "Enrollments", "CVR (%)", "Revenue", "Path Strategic Interpretation"]
    for c_i, h in enumerate(h_s9):
        cell = t_tbl.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_LIGHT

    for r_i, r in enumerate(paths_data):
        for c_i, v in enumerate(r):
            cell = t_tbl.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if r_i % 2 == 0 else C_CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = str(v)
            p.font.size = Pt(9)
            p.font.bold = (c_i in [0, 3, 4, 5])
            p.font.color.rgb = C_NAVY_DARK

    # ==========================================================================
    # Slide 10: Campaign-Level Efficiency Audit
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Campaign Audit: Spend Waste, Fatigue, and Cannibalization")

    camps_audit = [
        ("GS_Brand_Defense", "Google Ads - Grito Labs Brand Search", "$13.6k", "12.5%", "$1.25", "10.4x", "Maintain (Essential defense against competitors)"),
        ("Meta_Feed_CareerTransition", "Meta - Career Switcher Video Stories", "$38.2k", "1.9%", "$1.45", "4.6x", "Scale (+25%; core awareness powerhouse)"),
        ("Email_Webinar_Masterclass", "Email - Live Weekend Workshop", "$2.8k", "9.2%", "$0.12", "52.1x", "Scale (+45%; primary lead closing event)"),
        ("YT_Tutorial_SQLCrash", "YouTube - Free SQL Masterclass", "$23.5k", "2.1%", "$0.95", "4.5x", "Scale (+20%; high intent technical leads)"),
        ("GS_Competitor_Conquest", "Google - Competitor Conquesting", "$19.8k", "2.8%", "$4.10", "1.9x", "Cut (-35%; excessive CPC and low conversion)"),
        ("LI_Sponsored_DataCareer", "LinkedIn - Working Pro Upskilling", "$31.8k", "1.2%", "$7.50", "2.1x", "Cut (-40%; unsustainable unit economics)")
    ]

    t_s10 = s10.shapes.add_table(7, 7, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.4))
    tbl_10 = t_s10.table
    w_10 = [Inches(1.8), Inches(2.7), Inches(1.1), Inches(1.0), Inches(1.0), Inches(1.1), Inches(3.0)]
    for idx, w in enumerate(w_10):
        tbl_10.columns[idx].width = w

    h_10 = ["Campaign ID", "Campaign Name", "Spend", "CTR", "CPC", "ROAS", "Audit Finding & Action"]
    for c_i, h in enumerate(h_10):
        cell = tbl_10.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_LIGHT

    for r_i, r in enumerate(camps_audit):
        for c_i, v in enumerate(r):
            cell = tbl_10.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if r_i % 2 == 0 else C_CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = str(v)
            p.font.size = Pt(9)
            p.font.bold = (c_i in [0, 5, 6])
            p.font.color.rgb = C_RED if "Cut" in str(r[6]) else (C_GREEN if "Scale" in str(r[6]) else C_NAVY_DARK)

    # ==========================================================================
    # Slide 11: Cohort Retention & 12-Month LTV Analysis
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Customer Lifetime Value (LTV) & Post-Enrollment Retention")

    # 3 Stat Cards
    ltv_stats = [
        ("EMPIRICAL 12M LTV", "$1,304.50", "Initial Tuition + Upsell Revenue", C_NAVY_SLATE),
        ("CAPSTONE COMPLETION", "84.2%", "Core Metric Driving Student Advocacy", C_GREEN),
        ("ALUMNI REFERRAL RATE", "0.38 Referrals", "Per Enrolled Student (NPS: 9.1)", C_BLUE_ACCENT)
    ]
    for i, (st_t, st_v, st_sub, col) in enumerate(ltv_stats):
        left = Inches(0.8 + i * 3.95)
        add_card(s11, left, Inches(1.4), Inches(3.8), Inches(1.3))
        tb = s11.shapes.add_textbox(left + Inches(0.1), Inches(1.5), Inches(3.6), Inches(1.1))
        tf = tb.text_frame
        p_t = tf.paragraphs[0]
        p_t.text = st_t
        p_t.font.size = Pt(9)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TEXT_MUTED
        
        p_v = tf.add_paragraph()
        p_v.text = st_v
        p_v.font.size = Pt(18)
        p_v.font.bold = True
        p_v.font.color.rgb = col

        p_s = tf.add_paragraph()
        p_s.text = st_sub
        p_s.font.size = Pt(8.5)
        p_s.font.color.rgb = C_NAVY_SLATE

    # Cohort Breakdown Table
    c_data = [
        ("Organic Search", "246", "$1,207.74", "86.2%", "9.07", "22.8%", "0.44", "$1,310.18", "5.3x LTV:CAC"),
        ("YouTube Ads", "317", "$1,183.00", "84.5%", "9.15", "21.5%", "0.38", "$1,279.75", "4.6x LTV:CAC"),
        ("Meta Ads", "449", "$1,168.94", "83.7%", "9.08", "19.6%", "0.36", "$1,257.13", "4.3x LTV:CAC"),
        ("Google Search", "182", "$1,175.69", "83.0%", "9.05", "20.9%", "0.37", "$1,269.78", "5.2x LTV:CAC"),
        ("LinkedIn Ads", "135", "$1,191.67", "84.4%", "9.12", "20.7%", "0.39", "$1,285.00", "2.3x LTV:CAC"),
        ("Referral & Direct", "56", "$1,134.51", "85.7%", "9.21", "25.0%", "0.46", "$1,247.01", "Inf (Zero CAC)")
    ]
    t_s11 = s11.shapes.add_table(7, 9, Inches(0.8), Inches(3.0), Inches(11.7), Inches(3.9))
    tbl_11 = t_s11.table
    w_11 = [Inches(1.8), Inches(1.1), Inches(1.3), Inches(1.1), Inches(1.0), Inches(1.2), Inches(1.1), Inches(1.3), Inches(1.8)]
    for idx, w in enumerate(w_11):
        tbl_11.columns[idx].width = w

    h_11 = ["Acquisition Channel", "Students", "Initial Tuition", "Completion", "NPS", "Upsell Rate", "Referrals", "12M LTV", "LTV:CAC Health"]
    for c_i, h in enumerate(h_11):
        cell = tbl_11.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_LIGHT

    for r_i, r in enumerate(c_data):
        for c_i, v in enumerate(r):
            cell = tbl_11.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if r_i % 2 == 0 else C_CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = str(v)
            p.font.size = Pt(8.5)
            p.font.bold = (c_i in [0, 7, 8])
            p.font.color.rgb = C_RED if "2.3x" in str(v) else C_NAVY_DARK

    # ==========================================================================
    # Slide 12: Quantitative Budget Reallocation Strategy
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Capital Allocation: The Hill-Markov Reallocation Plan")

    realloc_data = [
        ("LinkedIn Ads", "$47,451.14", "$28,470.68", "-$18,980.46", "-40.0%", "86.7", "63.8", "Eliminate high CPC bid waste ($7.50); prune conquesting"),
        ("Email Marketing", "$5,218.13", "$7,827.20", "+$2,609.07", "+50.0%", "212.0", "268.4", "Scale automated drip sequences and webinar promos"),
        ("YouTube Ads", "$42,456.05", "$53,070.06", "+$10,614.01", "+25.0%", "152.5", "176.9", "Expand SQL crash courses & alumni showcase ads"),
        ("Google Search", "$82,007.20", "$89,387.85", "+$7,380.65", "+9.0%", "334.7", "352.1", "Protect brand defense; capture high intent bootcamp queries"),
        ("Meta Ads", "$85,764.16", "$84,140.89", "-$1,623.27", "-1.9%", "294.0", "291.8", "Reallocate toward highest performing Reels & Lookalikes")
    ]

    t_s12 = s12.shapes.add_table(6, 8, Inches(0.8), Inches(1.4), Inches(11.7), Inches(4.3))
    tbl_12 = t_s12.table
    w_12 = [Inches(1.8), Inches(1.2), Inches(1.3), Inches(1.3), Inches(1.0), Inches(1.1), Inches(1.1), Inches(2.9)]
    for idx, w in enumerate(w_12):
        tbl_12.columns[idx].width = w

    h_12 = ["Channel", "Current Spend", "Optimized Spend", "Budget Shift ($)", "Shift (%)", "Current Conv", "Projected Conv", "Strategic Rationale"]
    for c_i, h in enumerate(h_12):
        cell = tbl_12.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_LIGHT

    for r_i, r in enumerate(realloc_data):
        for c_i, v in enumerate(r):
            cell = tbl_12.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if r_i % 2 == 0 else C_CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = str(v)
            p.font.size = Pt(9)
            p.font.bold = (c_i in [0, 3, 4, 6])
            p.font.color.rgb = C_RED if "-" in str(r[3]) and c_i in [3, 4] else (C_GREEN if "+" in str(r[3]) and c_i in [3, 4] else C_NAVY_DARK)

    # Bottom Impact Callout Box
    add_card(s12, Inches(0.8), Inches(5.9), Inches(11.7), Inches(1.1), bg_color=C_BLUE_LIGHT, border_color=C_BLUE_ACCENT)
    tb_imp = s12.shapes.add_textbox(Inches(1.0), Inches(6.0), Inches(11.3), Inches(0.9))
    tf_imp = tb_imp.text_frame
    p_imp = tf_imp.paragraphs[0]
    p_imp.text = "NET OPTIMIZATION IMPACT SUMMARY:  +$74,941.99 Net Tuition Revenue | +63.5 Incremental Enrolled Students | 0% Increase in Budget"
    p_imp.font.size = Pt(12)
    p_imp.font.bold = True
    p_imp.font.color.rgb = C_BLUE_ACCENT

    p_imp2 = tf_imp.add_paragraph()
    p_imp2.text = "By curbing LinkedIn's CAC overspend and financing mid-funnel email automation and YouTube discovery, Grito Labs boosts blended marketing efficiency by +5.88%."
    p_imp2.font.size = Pt(9.5)
    p_imp2.font.color.rgb = C_NAVY_DARK

    # ==========================================================================
    # Slide 13: Sensitivity Analysis & Privacy Governance
    # ==========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Sensitivity Analysis: Tracking Privacy & Incrementality")

    caveats = [
        ("iOS 14.5+ ATT & Cookie Deprecation Impact", 
         "Apple's App Tracking Transparency and third-party cookie deprecation obscure 15-25% of mobile touchpoints. Grito Labs mitigates this via first-party server-side tracking (CAPI) and persistent hashed user IDs tied to free syllabus downloads and email registrations."),
        ("Attribution Lookback Window Sensitivity",
         "A 30-day lookback window captures 92% of all consideration cycles. Testing a 60-day window increases YouTube and Organic Search credit by +8.4%, reinforcing that awareness channels possess long conversion gestation periods that single-touch models completely miss."),
        ("Quasi-Experimental Incrementality Testing (Geo-Holdouts)",
         "Attribution models measure correlation, not pure causation. We recommend conducting 30-day regional geo-holdout tests on Google Search Brand Defense to verify organic search cannibalization and isolate pure incrementality.")
    ]
    for i, (title, desc) in enumerate(caveats):
        top = Inches(1.5 + i * 1.8)
        add_card(s13, Inches(0.8), top, Inches(11.7), Inches(1.55))
        tb = s13.shapes.add_textbox(Inches(1.0), top + Inches(0.15), Inches(11.3), Inches(1.25))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY_DARK
        p1.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_NAVY_SLATE

    # ==========================================================================
    # Slide 14: 90-Day Implementation & Roadmap
    # ==========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Action Plan: 90-Day Implementation & Governance Roadmap")

    phases = [
        ("DAYS 1 - 30: REBALANCE & TRUNCATE WASTE", C_RED, [
            "• Cut LinkedIn Ads spend by -40% (save ~$6.3k/mo); eliminate low-intent broad match targeting.",
            "• Cap Google Ads competitor conquesting; divert budget to Google Brand Defense.",
            "• Audit UTM parameter hygiene across all Meta Reels, YouTube descriptions, and email campaigns."
        ]),
        ("DAYS 31 - 60: SCALE ENABLERS & AUTOMATION", C_BLUE_ACCENT, [
            "• Expand Email Marketing automation by +50%; launch dedicated 5-day RCA case study drip series.",
            "• Increase YouTube Ads budget by +25% targeting free SQL crash course lead magnets.",
            "• Deploy server-side Conversion APIs (Meta CAPI & Google Enhanced Conversions) to bypass cookie loss."
        ]),
        ("DAYS 61 - 90: INCREMENTALITY & ALUMNI ADVOCACY", C_GREEN, [
            "• Run 30-day geo-matched holdout test on Google Brand Search to measure true cannibalization.",
            "• Formalize the Alumni Referral Engine ($100 tuition voucher per qualified student referral).",
            "• Transition executive reporting from Last-Touch Attribution to Markov Algorithmic MTA Dashboard."
        ])
    ]
    for i, (p_title, p_col, p_items) in enumerate(phases):
        left = Inches(0.8 + i * 3.95)
        add_card(s14, left, Inches(1.4), Inches(3.8), Inches(5.5))
        tb = s14.shapes.add_textbox(left + Inches(0.2), Inches(1.6), Inches(3.4), Inches(5.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = p_title
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = p_col
        p1.space_after = Pt(14)

        for it in p_items:
            p = tf.add_paragraph()
            p.text = it
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_NAVY_SLATE
            p.space_after = Pt(10)

    # Save presentation
    prs.save(OUTPUT_PPTX)
    print(f"Presentation deck successfully created -> {OUTPUT_PPTX}")

if __name__ == "__main__":
    create_deck()
