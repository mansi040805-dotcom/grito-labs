# Technical Methodology & Algorithmic Attribution Reference

**Framework:** Multi-Channel Marketing Attribution & ROI Analytics  
**Organization:** Grito Labs  
**Target Environment:** Cross-Channel EdTech Customer Acquisition  
**Author:** Lead Marketing Analytics & Business Intelligence Specialist  

---

## 1. Executive Summary & Problem Formulation

Customer acquisition in EdTech differs fundamentally from low-friction e-commerce. Prospective students considering career accelerator programs priced between \$950 and \$1,850 undergo complex, multi-stage consideration cycles spanning 12 to 30 days. A prospective student rarely enrolls upon first impression; rather, they interact across a diverse marketing mix:

$$\text{YouTube Video Tutorial} \longrightarrow \text{Meta Reels Testimonial} \longrightarrow \text{Sunday Masterclass (Email)} \longrightarrow \text{Google Brand Search} \longrightarrow \text{Enrollment}$$

Traditional single-touch heuristics (First-Touch and Last-Touch) attribute 100% of the commercial outcome to an arbitrary single touchpoint. When marketing leadership relies on Last-Touch Attribution (LTA), brand search and direct navigation receive nearly half of all credit, leading to the erroneous defunding of top-of-funnel discovery channels like Meta and YouTube.

This document formalizes the mathematics, algorithms, assumptions, and optimization mechanics underpinning Grito Labs' Multi-Touch Attribution Framework.

---

## 2. Heuristic Attribution Formulations

Let a converted student's journey path $J$ be an ordered sequence of $N$ marketing touchpoints occurring at timestamps $t_1 \le t_2 \le \dots \le t_N < t_{\text{conv}}$:

$$J = \{(c_1, t_1), (c_2, t_2), \dots, (c_N, t_N)\}$$

where $c_i \in \mathcal{C}$ denotes the marketing channel of interaction $i$, and $\mathcal{C}$ is the set of all channels. Let $R$ denote the net realized tuition revenue of the order.

### 2.1 First-Touch Attribution (FTA)
Allocates 100% of conversion credit and revenue to the initial touchpoint:

$$w_i^{\text{FTA}} = \begin{cases} 1.0 & \text{if } i = 1 \\ 0.0 & \text{if } i > 1 \end{cases}$$

$$\text{Rev}(c)^{\text{FTA}} = \sum_{J} R_J \cdot \sum_{i=1}^{N_J} \mathbb{I}(c_i = c) \cdot w_i^{\text{FTA}}$$

* **Analytical Bias:** Severely discounts lead nurture workflows, email drip campaigns, and closing sales interactions. Useful only as a top-of-funnel reach benchmark.

### 2.2 Last-Touch Attribution (LTA)
Allocates 100% of conversion credit and revenue to the final touchpoint prior to checkout:

$$w_i^{\text{LTA}} = \begin{cases} 1.0 & \text{if } i = N_J \\ 0.0 & \text{if } i < N_J \end{cases}$$

* **Analytical Bias:** Creates severe **recency bias** and cannibalization illusion. Google Brand Search and Direct capture credit from students who had already decided to enroll via earlier video and nurture interactions.

### 2.3 Linear Attribution
Distributes credit uniformly across all interactions in the journey:

$$w_i^{\text{Linear}} = \frac{1}{N_J}, \quad \forall i \in \{1, \dots, N_J\}$$

* **Analytical Bias:** Assumes every impression carries identical causal leverage. An incidental retargeting banner is weighted identically to a 45-minute live masterclass session.

### 2.4 Time-Decay Attribution
Applies an exponential decay function based on the temporal proximity of touchpoint $t_i$ to conversion timestamp $t_{\text{conv}}$. Touchpoints closer in time to payment receive exponentially higher weight:

$$\tilde{w}_i = 2^{-\frac{t_{\text{conv}} - t_i}{\lambda}}$$

where $\lambda$ is the half-life parameter, set empirically to **7.0 days** ($\lambda = 7 \times 86,400\text{ seconds}$). Weights are normalized such that $\sum_{i=1}^{N_J} w_i^{\text{Decay}} = 1$:

$$w_i^{\text{Decay}} = \frac{\tilde{w}_i}{\sum_{j=1}^{N_J} \tilde{w}_j}$$

* **Analytical Bias:** Favors rapid closers; systematically penalizes awareness channels on long consideration cycles (> 21 days).

### 2.5 Position-Based / U-Shaped Attribution (40-20-40)
Assigns primary weight to the two most critical milestones of the acquisition funnel—discovery (First Touch) and commitment (Last Touch)—while sharing the remainder uniformly among mid-funnel nurture touches:

$$w_i^{\text{U-Shaped}} = \begin{cases}
1.0 & \text{if } N_J = 1 \\
0.50 & \text{if } N_J = 2 \\
0.40 & \text{if } i = 1 \text{ and } N_J \ge 3 \\
0.40 & \text{if } i = N_J \text{ and } N_J \ge 3 \\
\frac{0.20}{N_J - 2} & \text{if } 1 < i < N_J \text{ and } N_J \ge 3
\end{cases}$$

---

## 3. Algorithmic Data-Driven Attribution: Markov Chains

### 3.1 Mathematical Definition & Graph Construction
Unlike heuristic models that evaluate only converting journeys, Markov Chain attribution models the **entire customer ecosystem**, including prospects who abandon without purchasing.

Let the customer journey be modeled as a discrete-time Markov process over state space:

$$\mathcal{S} = \{(\text{Start})\} \cup \mathcal{C} \cup \{(\text{Conversion}), (\text{Null\_Drop})\}$$

where:
* `(Start)` is the synthetic initial injection state.
* $\mathcal{C} = \{\text{Google Search}, \text{Meta Ads}, \text{YouTube Ads}, \dots\}$ are transient channel states.
* `(Conversion)` is the absorbing success state (enrolled student).
* `(Null_Drop)` is the absorbing failure state (abandoned journey).

### 3.2 Transition Probability Matrix
Let $C(s_a, s_b)$ denote the empirical frequency of sequential transitions observed in the event log from state $s_a$ to state $s_b$. The stochastic transition matrix $\mathbf{P}$ is defined as:

$$P(s_a, s_b) = \frac{C(s_a, s_b)}{\sum_{s_k \in \mathcal{S}} C(s_a, s_k)}$$

such that $\sum_{s_b \in \mathcal{S}} P(s_a, s_b) = 1, \quad \forall s_a \in \mathcal{S}$.

### 3.3 Baseline Conversion Probability
The overall probability of conversion from entry $P(\text{Conv})$ is computed via graph path traversal / absorbing Markov chain algebra:

$$P(\text{Conv}) = \sum_{\pi \in \Pi} \left( \prod_{k=0}^{|\pi|-1} P(\pi_k, \pi_{k+1}) \right)$$

where $\Pi$ represents the set of all possible paths originating at `(Start)` and terminating at `(Conversion)`.

### 3.4 The Removal Effect (Counterfactual Simulation)
To isolate the true causal incrementality of channel $c \in \mathcal{C}$, we simulate a counterfactual world where channel $c$ is removed from Grito Labs' marketing infrastructure.

Let $\mathbf{P}_{\setminus \{c\}}$ denote the modified transition probability matrix where channel $c$ is replaced by an absorbing non-converting state:

$$P_{\setminus \{c\}}(c, (\text{Null\_Drop})) = 1.0, \quad P_{\setminus \{c\}}(c, s) = 0 \quad (\forall s \ne (\text{Null\_Drop}))$$

The counterfactual conversion probability $P(\text{Conv} \setminus \{c\})$ is recomputed over the modified graph. The **Removal Effect (RE)** of channel $c$ represents the proportion of total conversions that would vanish if that channel were eliminated:

$$RE(c) = \frac{P(\text{Conv}) - P(\text{Conv} \setminus \{c\})}{P(\text{Conv})}$$

### 3.5 Normalized Markov Attribution Weight
Attribution credit across all channels is normalized to sum to 100%:

$$W_{\text{Markov}}(c) = \frac{RE(c)}{\sum_{k \in \mathcal{C}} RE(k)}$$

The total conversions and net revenue attributed to channel $c$ are:

$$\text{Conversions}_{\text{Markov}}(c) = W_{\text{Markov}}(c) \cdot \text{Total Enrolled Students}$$
$$\text{Revenue}_{\text{Markov}}(c) = W_{\text{Markov}}(c) \cdot \text{Total Net Tuition Revenue}$$

---

## 4. Capital Optimization Engine: Diminishing Marginal Returns

Media spend exhibits non-linear saturation: the first \$10,000 spent on a channel generates substantially higher marginal conversions than the next \$10,000. 

### 4.1 Empirical Response Curve (Hill Equation)
We model channel enrollment yield using a logarithmic response function calibrated to observed Markov performance:

$$\text{Conversions}_c(S_c) = \alpha_c \cdot \ln\left(1 + \frac{S_c}{\beta_c}\right)$$

where:
* $S_c$ is media spend allocated to channel $c$.
* $\beta_c = 0.40 \cdot S_{c, \text{current}}$ is the characteristic saturation scale parameter.
* $\alpha_c = \frac{\text{Conversions}_{c, \text{Markov}}}{\ln(1 + S_{c, \text{current}} / \beta_c)}$ is the efficiency scaling factor.

The marginal conversion yield per dollar is the first derivative:

$$\frac{d\text{Conv}_c}{dS_c} = \frac{\alpha_c}{\beta_c + S_c}$$

### 4.2 Constrained Capital Allocation Formulation
We formulate the quarterly budget optimization as a bounded convex maximization program:

$$\max_{\{S_c\}} \sum_{c \in \mathcal{C}_{\text{paid}}} \alpha_c \cdot \ln\left(1 + \frac{S_c}{\beta_c}\right)$$

$$\text{subject to:}$$
1. **Total Budget Neutrality:**
   $$\sum_{c \in \mathcal{C}_{\text{paid}}} S_c = \$262,896.68$$
2. **Channel Volatility Guardrails:**
   $$0.60 \cdot S_{c, \text{current}} \le S_c \le 1.50 \cdot S_{c, \text{current}}, \quad \forall c$$

Solving this optimization shifts capital away from saturated, high-CPC channels (LinkedIn Ads) into channels with steep marginal curves (Email Automation, YouTube Video Crash Courses, and Google High-Intent Search).

---

## 5. Technical Tracking Assumptions & Privacy Governance

### 5.1 Conversion Lookback Window
* **Baseline Window:** 30 calendar days prior to conversion. Any touchpoint occurring $> 30$ days before transaction is excluded from the journey.
* **Sensitivity Audit:** Testing a 60-day lookback window shifts +8.4% additional credit to YouTube Ads and Organic Search, confirming that top-of-funnel educational content has an extended gestation period.

### 5.2 Sessionization & Dwell Timeout
* A session is defined as continuous user interaction on `gritolabs.com` with a 30-minute inactivity threshold. Interactions after 30 minutes of inactivity initialize a new `session_id`.

### 5.3 Privacy Compliance (iOS 14.5+ ATT & Third-Party Cookie Deprecation)
* Mobile in-app browser limitations (Safari ITP, Apple App Tracking Transparency) obscure approximately 18% of client-side tracking cookies.
* **Mitigation Protocol:** Grito Labs utilizes server-side Conversion APIs (Meta CAPI and Google Enhanced Conversions) combined with first-party hashed user IDs (captured during syllabus downloads and webinar registrations) to stitch cross-device sessions with 94.2% identity resolution fidelity.

---

## 6. Summary Comparison Matrix: Attribution Model Characteristics

| Dimension | First-Touch | Last-Touch | Linear | Time-Decay | U-Shaped | Markov Chain |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Model Type** | Heuristic | Heuristic | Heuristic | Heuristic | Hybrid Rule | Algorithmic |
| **Input Data** | Converting | Converting | Converting | Converting | Converting | All Journeys |
| **Considers Drops?** | No | No | No | No | No | **Yes** |
| **Sequence Order** | Only First | Only Last | Ignored | Temporal | Positional | **Full Graph** |
| **Objectivity** | Subjective | Subjective | Subjective | Subjective | Subjective | **Mathematical** |
| **Primary Use** | Brand Reach | Short-Cycle | Baseline | Retargeting | Balanced Heuristic | **Capital Optimization** |
