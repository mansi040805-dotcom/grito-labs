"""
================================================================================
Grito Labs - Multi-Channel Marketing Analytics & Attribution Engine
================================================================================
Executes 6 multi-touch attribution models:
1. First-Touch Attribution (FTA)
2. Last-Touch Attribution (LTA)
3. Linear Attribution (Uniform)
4. Time-Decay Attribution (7-day half-life)
5. Position-Based / U-Shaped Attribution (40-20-40)
6. Markov Chain Algorithmic Attribution (Transition Matrix & Removal Effect)

Calculates marketing KPIs: ROAS, CAC, CTR, CPC, LTV:CAC, Payback Period.
Outputs processed datasets and updates SQLite analytics database.
"""

import os
import csv
import math
import sqlite3
from datetime import datetime
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
DB_PATH = os.path.join(BASE_DIR, "data", "grito_marketing_analytics.db")

HALF_LIFE_DAYS = 7.0

def load_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Load spend by channel
    cur.execute("""
        SELECT channel, 
               SUM(spend_usd) as total_spend,
               SUM(impressions) as total_impressions,
               SUM(clicks) as total_clicks
        FROM ad_spend_daily
        GROUP BY channel
    """)
    channel_spend = {row["channel"]: dict(row) for row in cur.fetchall()}

    # Load campaign spend
    cur.execute("""
        SELECT campaign_id, campaign_name, channel,
               SUM(spend_usd) as total_spend,
               SUM(impressions) as total_impressions,
               SUM(clicks) as total_clicks
        FROM ad_spend_daily
        GROUP BY campaign_id, campaign_name, channel
    """)
    campaign_spend = {row["campaign_id"]: dict(row) for row in cur.fetchall()}

    # Load user touchpoints ordered by timestamp
    cur.execute("""
        SELECT touchpoint_id, user_id, session_id, timestamp, channel, campaign_id, interaction_seq
        FROM web_touchpoints
        ORDER BY user_id, timestamp ASC
    """)
    touchpoints = cur.fetchall()

    # Load conversions
    cur.execute("""
        SELECT order_id, user_id, conversion_timestamp, program_code, program_name,
               gross_revenue_usd, discount_usd, net_revenue_usd
        FROM conversions_and_orders
    """)
    conversions = {row["user_id"]: dict(row) for row in cur.fetchall()}

    # Load customer retention / LTV
    cur.execute("""
        SELECT user_id, total_customer_ltv_usd, referrals_generated
        FROM customer_retention_cohorts
    """)
    retention = {row["user_id"]: dict(row) for row in cur.fetchall()}

    conn.close()
    return channel_spend, campaign_spend, touchpoints, conversions, retention

# ------------------------------------------------------------------------------
# 1. Rule-Based Multi-Touch Attribution Modeling
# ------------------------------------------------------------------------------
def compute_rule_based_attribution(touchpoints, conversions):
    user_touches = defaultdict(list)
    for tp in touchpoints:
        user_touches[tp["user_id"]].append(dict(tp))

    channels = sorted(list(set(tp["channel"] for tp in touchpoints)))

    # Track conversions and revenue credited per channel per model
    # models: first_touch, last_touch, linear, time_decay, u_shaped
    models = ["first_touch", "last_touch", "linear", "time_decay", "u_shaped"]
    attr_conv = {m: defaultdict(float) for m in models}
    attr_rev = {m: defaultdict(float) for m in models}

    # Also track at campaign level
    camp_attr_conv = {m: defaultdict(float) for m in models}
    camp_attr_rev = {m: defaultdict(float) for m in models}

    journey_paths_summary = defaultdict(lambda: {"count": 0, "conversions": 0, "revenue": 0.0})

    for user_id, touches in user_touches.items():
        # Sort touches chronologically
        touches = sorted(touches, key=lambda x: x["timestamp"])
        path_str = " > ".join(t["channel"] for t in touches)
        is_conv = user_id in conversions

        journey_paths_summary[path_str]["count"] += 1

        if not is_conv:
            continue

        conv_info = conversions[user_id]
        rev = conv_info["net_revenue_usd"]
        journey_paths_summary[path_str]["conversions"] += 1
        journey_paths_summary[path_str]["revenue"] += rev

        n = len(touches)
        conv_dt = datetime.strptime(conv_info["conversion_timestamp"], "%Y-%m-%d %H:%M:%S")

        # 1. First-Touch
        ft_ch = touches[0]["channel"]
        ft_cp = touches[0]["campaign_id"]
        attr_conv["first_touch"][ft_ch] += 1.0
        attr_rev["first_touch"][ft_ch] += rev
        camp_attr_conv["first_touch"][ft_cp] += 1.0
        camp_attr_rev["first_touch"][ft_cp] += rev

        # 2. Last-Touch
        lt_ch = touches[-1]["channel"]
        lt_cp = touches[-1]["campaign_id"]
        attr_conv["last_touch"][lt_ch] += 1.0
        attr_rev["last_touch"][lt_ch] += rev
        camp_attr_conv["last_touch"][lt_cp] += 1.0
        camp_attr_rev["last_touch"][lt_cp] += rev

        # 3. Linear
        linear_w = 1.0 / n
        for t in touches:
            ch = t["channel"]
            cp = t["campaign_id"]
            attr_conv["linear"][ch] += linear_w
            attr_rev["linear"][ch] += rev * linear_w
            camp_attr_conv["linear"][cp] += linear_w
            camp_attr_rev["linear"][cp] += rev * linear_w

        # 4. Time-Decay (half-life = 7 days)
        raw_decay_weights = []
        for t in touches:
            t_dt = datetime.strptime(t["timestamp"], "%Y-%m-%d %H:%M:%S")
            days_diff = max(0.0, (conv_dt - t_dt).total_seconds() / 86400.0)
            weight = math.pow(2.0, -days_diff / HALF_LIFE_DAYS)
            raw_decay_weights.append(weight)
        sum_decay = sum(raw_decay_weights)
        norm_decay = [w / sum_decay for w in raw_decay_weights]

        for i, t in enumerate(touches):
            w = norm_decay[i]
            ch = t["channel"]
            cp = t["campaign_id"]
            attr_conv["time_decay"][ch] += w
            attr_rev["time_decay"][ch] += rev * w
            camp_attr_conv["time_decay"][cp] += w
            camp_attr_rev["time_decay"][cp] += rev * w

        # 5. Position-Based / U-Shaped (40-20-40)
        if n == 1:
            u_weights = [1.0]
        elif n == 2:
            u_weights = [0.5, 0.5]
        else:
            mid_weight = 0.20 / (n - 2)
            u_weights = [0.40] + [mid_weight] * (n - 2) + [0.40]

        for i, t in enumerate(touches):
            w = u_weights[i]
            ch = t["channel"]
            cp = t["campaign_id"]
            attr_conv["u_shaped"][ch] += w
            attr_rev["u_shaped"][ch] += rev * w
            camp_attr_conv["u_shaped"][cp] += w
            camp_attr_rev["u_shaped"][cp] += rev * w

    return attr_conv, attr_rev, camp_attr_conv, camp_attr_rev, journey_paths_summary, user_touches

# ------------------------------------------------------------------------------
# 2. Markov Chain Algorithmic Attribution (Transition Matrix & Removal Effects)
# ------------------------------------------------------------------------------
def compute_markov_chain_attribution(user_touches, conversions):
    """
    Constructs state transitions:
    Start -> Channel 1 -> Channel 2 -> ... -> (Conversion / Drop)
    Computes Baseline Conversion Probability via Markov simulation / absorbing chain,
    Then calculates the Removal Effect for each channel.
    """
    transitions = defaultdict(lambda: defaultdict(int))
    channels = set()

    for user_id, touches in user_touches.items():
        touches = sorted(touches, key=lambda x: x["timestamp"])
        path = [t["channel"] for t in touches]
        for ch in path:
            channels.add(ch)

        # Start transition
        transitions["(Start)"][path[0]] += 1

        # Intermediate transitions
        for i in range(len(path) - 1):
            transitions[path[i]][path[i + 1]] += 1

        # Final transition
        if user_id in conversions:
            transitions[path[-1]]["(Conversion)"] += 1
        else:
            transitions[path[-1]]["(Null_Drop)"] += 1

    channels = sorted(list(channels))

    # Calculate Transition Probability Matrix
    prob_matrix = defaultdict(dict)
    for state_from, to_dict in transitions.items():
        total_out = sum(to_dict.values())
        for state_to, count in to_dict.items():
            prob_matrix[state_from][state_to] = count / total_out if total_out > 0 else 0.0

    # Function to calculate conversion probability through graph traversal
    # Using recursive path probability calculation with depth cutoff
    def get_conversion_probability(blocked_channel=None):
        memo = {}
        def path_prob(current_state, depth):
            if depth > 10:
                return 0.0
            if current_state == "(Conversion)":
                return 1.0
            if current_state == "(Null_Drop)":
                return 0.0
            if blocked_channel and current_state == blocked_channel:
                return 0.0

            key = (current_state, depth)
            if key in memo:
                return memo[key]

            total_p = 0.0
            for next_state, p in prob_matrix[current_state].items():
                if next_state != current_state:  # prevent self-loop infinite recursion
                    total_p += p * path_prob(next_state, depth + 1)
                else:
                    pass
            memo[key] = total_p
            return total_p

        return path_prob("(Start)", 0)

    base_conv_prob = get_conversion_probability()
    if base_conv_prob == 0:
        base_conv_prob = 1e-6

    # Calculate Removal Effects
    removal_effects = {}
    for ch in channels:
        p_blocked = get_conversion_probability(blocked_channel=ch)
        removal_effect = max(0.0, (base_conv_prob - p_blocked) / base_conv_prob)
        removal_effects[ch] = removal_effect

    total_removal = sum(removal_effects.values())
    if total_removal == 0:
        total_removal = 1e-6

    # Normalized weights
    markov_weights = {ch: removal_effects[ch] / total_removal for ch in channels}

    # Attribute actual total conversions and revenue
    total_conversions = len(conversions)
    total_net_rev = sum(c["net_revenue_usd"] for c in conversions.values())

    markov_conv = {ch: round(markov_weights[ch] * total_conversions, 2) for ch in channels}
    markov_rev = {ch: round(markov_weights[ch] * total_net_rev, 2) for ch in channels}

    return markov_conv, markov_rev, removal_effects, prob_matrix, channels

# ------------------------------------------------------------------------------
# 3. Main Analytics Aggregation & File Export
# ------------------------------------------------------------------------------
def main():
    print("Executing Grito Labs Multi-Touch Attribution Engine...")
    channel_spend, campaign_spend, touchpoints, conversions, retention = load_data()

    # Run rule-based models
    attr_conv, attr_rev, camp_attr_conv, camp_attr_rev, paths_summary, user_touches = compute_rule_based_attribution(touchpoints, conversions)

    # Run Markov Chain model
    markov_conv, markov_rev, removal_effects, prob_matrix, channels = compute_markov_chain_attribution(user_touches, conversions)

    attr_conv["markov_chain"] = markov_conv
    attr_rev["markov_chain"] = markov_rev

    # 1. Output Journey Paths Summary
    sorted_paths = sorted(paths_summary.items(), key=lambda x: x[1]["conversions"], reverse=True)
    paths_file = os.path.join(DATA_PROC_DIR, "customer_journey_paths.csv")
    with open(paths_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["journey_path", "touchpoints_count", "total_prospects", "total_conversions", "conversion_rate_pct", "total_net_revenue_usd"])
        for path_str, stats in sorted_paths:
            path_len = len(path_str.split(" > "))
            cvr = round((stats["conversions"] / stats["count"]) * 100, 2) if stats["count"] > 0 else 0.0
            writer.writerow([path_str, path_len, stats["count"], stats["conversions"], cvr, round(stats["revenue"], 2)])
    print(f" -> Exported top conversion journeys -> {paths_file}")

    # 2. Output Attribution Comparison Table
    attr_file = os.path.join(DATA_PROC_DIR, "attribution_model_comparison.csv")
    attr_rows = []
    for ch in channels:
        spend = channel_spend.get(ch, {}).get("total_spend", 0.0)
        row = {
            "channel": ch,
            "total_spend_usd": round(spend, 2),
            "impressions": channel_spend.get(ch, {}).get("total_impressions", 0),
            "clicks": channel_spend.get(ch, {}).get("total_clicks", 0),
            "markov_removal_effect": round(removal_effects.get(ch, 0.0), 4),
            
            # Conversions
            "conv_first_touch": round(attr_conv["first_touch"][ch], 2),
            "conv_last_touch": round(attr_conv["last_touch"][ch], 2),
            "conv_linear": round(attr_conv["linear"][ch], 2),
            "conv_time_decay": round(attr_conv["time_decay"][ch], 2),
            "conv_u_shaped": round(attr_conv["u_shaped"][ch], 2),
            "conv_markov_chain": round(attr_conv["markov_chain"][ch], 2),

            # Revenue
            "rev_first_touch": round(attr_rev["first_touch"][ch], 2),
            "rev_last_touch": round(attr_rev["last_touch"][ch], 2),
            "rev_linear": round(attr_rev["linear"][ch], 2),
            "rev_time_decay": round(attr_rev["time_decay"][ch], 2),
            "rev_u_shaped": round(attr_rev["u_shaped"][ch], 2),
            "rev_markov_chain": round(attr_rev["markov_chain"][ch], 2),

            # Markov ROAS & CAC (Primary Truth Model)
            "markov_roas": round(attr_rev["markov_chain"][ch] / spend, 2) if spend > 0 else 999.0,
            "markov_cac": round(spend / attr_conv["markov_chain"][ch], 2) if attr_conv["markov_chain"][ch] > 0 and spend > 0 else 0.0
        }
        attr_rows.append(row)

    with open(attr_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(attr_rows[0].keys()))
        writer.writeheader()
        writer.writerows(attr_rows)
    print(f" -> Exported attribution model comparison -> {attr_file}")

    # 3. Output Campaign Deep Dive
    camp_file = os.path.join(DATA_PROC_DIR, "campaign_roi_deepdive.csv")
    camp_rows = []
    
    # Calculate avg LTV across users
    all_ltvs = [r["total_customer_ltv_usd"] for r in retention.values()]
    avg_customer_ltv = sum(all_ltvs) / len(all_ltvs) if all_ltvs else 1350.0

    for camp_id, info in campaign_spend.items():
        spend = info["total_spend"]
        impr = info["total_impressions"]
        clicks = info["total_clicks"]
        cpc = round(spend / clicks, 2) if clicks > 0 else 0.0
        ctr = round((clicks / impr) * 100, 2) if impr > 0 else 0.0
        
        lt_conv = round(camp_attr_conv["last_touch"][camp_id], 2)
        lt_rev = round(camp_attr_rev["last_touch"][camp_id], 2)
        lin_conv = round(camp_attr_conv["linear"][camp_id], 2)
        lin_rev = round(camp_attr_rev["linear"][camp_id], 2)

        roas_linear = round(lin_rev / spend, 2) if spend > 0 else 999.0
        cac_linear = round(spend / lin_conv, 2) if lin_conv > 0 and spend > 0 else 0.0
        ltv_to_cac = round(avg_customer_ltv / cac_linear, 2) if cac_linear > 0 else 999.0

        # Payback period in months = CAC / (Monthly Net Margin per Student ~$400)
        payback_months = round(cac_linear / 400.0, 1) if cac_linear > 0 else 0.0

        # Actionable Recommendation based on ROAS & LTV:CAC
        if spend == 0:
            status = "ORGANIC_EXPAND"
            action = "Scale content production; primary zero-CAC acquisition pillar."
        elif roas_linear >= 3.8 and ltv_to_cac >= 7.0:
            status = "STRONG_SCALE"
            action = "Increase budget by +30% to +40%; high marginal efficiency."
        elif roas_linear >= 2.5:
            status = "OPTIMIZE_AND_MAINTAIN"
            action = "Maintain budget; optimize ad creatives & landing page CVR."
        else:
            status = "UNDERPERFORMING_REDUCE"
            action = "Cut spend by -25% to -40%; reallocate capital to top channels."

        camp_rows.append({
            "campaign_id": camp_id,
            "campaign_name": info["campaign_name"],
            "channel": info["channel"],
            "spend_usd": round(spend, 2),
            "impressions": impr,
            "clicks": clicks,
            "ctr_pct": ctr,
            "cpc_usd": cpc,
            "conversions_last_touch": lt_conv,
            "revenue_last_touch": lt_rev,
            "conversions_linear": lin_conv,
            "revenue_linear": lin_rev,
            "roas_linear": roas_linear,
            "cac_linear_usd": cac_linear,
            "ltv_to_cac_ratio": ltv_to_cac,
            "payback_months": payback_months,
            "efficiency_status": status,
            "strategic_recommendation": action
        })

    camp_rows.sort(key=lambda x: x["spend_usd"], reverse=True)
    with open(camp_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(camp_rows[0].keys()))
        writer.writeheader()
        writer.writerows(camp_rows)
    print(f" -> Exported campaign deep-dive analysis -> {camp_file}")

    # 4. Save to Database as SQL Views / Tables
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS attribution_model_comparison;")
    cur.execute("""
    CREATE TABLE attribution_model_comparison (
        channel VARCHAR(64) PRIMARY KEY,
        total_spend_usd REAL,
        impressions INTEGER,
        clicks INTEGER,
        markov_removal_effect REAL,
        conv_first_touch REAL,
        conv_last_touch REAL,
        conv_linear REAL,
        conv_time_decay REAL,
        conv_u_shaped REAL,
        conv_markov_chain REAL,
        rev_first_touch REAL,
        rev_last_touch REAL,
        rev_linear REAL,
        rev_time_decay REAL,
        rev_u_shaped REAL,
        rev_markov_chain REAL,
        markov_roas REAL,
        markov_cac REAL
    );
    """)
    cur.executemany("""
        INSERT INTO attribution_model_comparison VALUES (
            :channel, :total_spend_usd, :impressions, :clicks, :markov_removal_effect,
            :conv_first_touch, :conv_last_touch, :conv_linear, :conv_time_decay, :conv_u_shaped, :conv_markov_chain,
            :rev_first_touch, :rev_last_touch, :rev_linear, :rev_time_decay, :rev_u_shaped, :rev_markov_chain,
            :markov_roas, :markov_cac
        );
    """, attr_rows)

    cur.execute("DROP TABLE IF EXISTS campaign_roi_deepdive;")
    cur.execute("""
    CREATE TABLE campaign_roi_deepdive (
        campaign_id VARCHAR(64) PRIMARY KEY,
        campaign_name VARCHAR(128),
        channel VARCHAR(64),
        spend_usd REAL,
        impressions INTEGER,
        clicks INTEGER,
        ctr_pct REAL,
        cpc_usd REAL,
        conversions_last_touch REAL,
        revenue_last_touch REAL,
        conversions_linear REAL,
        revenue_linear REAL,
        roas_linear REAL,
        cac_linear_usd REAL,
        ltv_to_cac_ratio REAL,
        payback_months REAL,
        efficiency_status VARCHAR(64),
        strategic_recommendation TEXT
    );
    """)
    cur.executemany("""
        INSERT INTO campaign_roi_deepdive VALUES (
            :campaign_id, :campaign_name, :channel, :spend_usd, :impressions, :clicks, :ctr_pct, :cpc_usd,
            :conversions_last_touch, :revenue_last_touch, :conversions_linear, :revenue_linear,
            :roas_linear, :cac_linear_usd, :ltv_to_cac_ratio, :payback_months,
            :efficiency_status, :strategic_recommendation
        );
    """, camp_rows)

    conn.commit()
    conn.close()
    print("Multi-touch attribution pipeline finished with high precision.")

if __name__ == "__main__":
    main()
