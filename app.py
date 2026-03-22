import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from life_table_calculator import (
    SSA_2022, RISK_FACTORS, combined_hr, apply_hr_to_qx, build_life_table
)

st.set_page_config(
    page_title="Lifespan Calculator",
    page_icon="⧖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0e0e11; color: #f0ede8; }
[data-testid="stSidebar"] { background: #16161a; border-right: 1px solid #2a2a32; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stRadio label {
    color: #9997a0 !important; font-size: 0.78rem; font-weight: 500;
    letter-spacing: 0.06em; text-transform: uppercase;
}
h1, h2, h3 { font-family: 'DM Serif Display', serif; }
.metric-card {
    background: #1a1a20; border: 1px solid #2a2a35;
    border-radius: 12px; padding: 1.25rem 1.5rem; text-align: center;
}
.metric-label { font-size: 0.72rem; font-weight: 500; letter-spacing: 0.08em;
                text-transform: uppercase; color: #6b6875; margin-bottom: 0.4rem; }
.metric-value { font-family: 'DM Serif Display', serif; font-size: 2.8rem;
                line-height: 1; color: #f0ede8; }
.metric-unit { font-size: 0.95rem; color: #9997a0; margin-left: 3px; }
.metric-delta { font-size: 0.8rem; margin-top: 0.35rem; color: #9997a0; }
.metric-delta.pos { color: #4ade80; }
.metric-delta.neg { color: #f87171; }
.section-title { font-size: 0.7rem; font-weight: 500; letter-spacing: 0.12em;
                 text-transform: uppercase; color: #4a4855; margin: 1.25rem 0 0.6rem;
                 border-bottom: 1px solid #1e1e26; padding-bottom: 0.4rem; }
.factor-card {
    background: #1a1a20; border: 1px solid #2a2a35; border-radius: 10px;
    padding: 0.9rem 1.1rem; height: 100%;
}
.factor-card .flabel { font-size: 0.68rem; color: #4a4855; text-transform: uppercase;
                        letter-spacing: 0.07em; margin-bottom: 4px; }
.factor-card .fval { font-size: 0.88rem; color: #f0ede8; line-height: 1.3; margin-bottom: 6px; }
.factor-card .fhr { font-size: 0.8rem; font-weight: 500; }
.meth-link { display:inline-flex; align-items:center; gap:6px; background:#1e1e28;
             border:1px solid #3a3a50; border-radius:8px; padding:8px 16px;
             font-size:0.82rem; color:#b69cf5; text-decoration:none; cursor:pointer; }
.meth-link:hover { background:#252535; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.75rem; padding-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# ── Display labels ────────────────────────────────────────────────────────────
LABELS = {
    "smoking": {
        "never": "Never smoker", "former_light": "Former — light / quit >10yr",
        "former_heavy": "Former — heavy / quit <10yr", "current_light": "Current — light (<10/day)",
        "current_heavy": "Current — heavy (≥1 pack/day)", "vaping": "Vaping / e-cigs only",
    },
    "bmi": {
        "underweight": "Underweight  (<18.5)", "normal": "Normal  (18.5–24.9)",
        "overweight": "Overweight  (25–29.9)", "obese1": "Obese Class I  (30–34.9)",
        "obese2": "Obese Class II  (35–39.9)", "obese3": "Obese Class III  (40+)",
    },
    "alcohol": {
        "none": "Non-drinker", "moderate": "Moderate  (≤14/week)",
        "heavy": "Heavy  (15–28/week)", "severe": "Severe / AUD  (>28/week)",
    },
    "activity": {
        "sedentary": "Sedentary  (<30 min/week)", "insufficient": "Insufficient  (30–150 min/week)",
        "active": "Active  (150–300 min/week)", "highly_active": "Highly active  (>300 min/week)",
    },
    "sleep": {
        "short": "Short sleeper  (<6 hrs)", "normal": "Normal  (7–8 hrs)",
        "long": "Long sleeper  (>9 hrs)",
    },
    "diet": {
        "poor": "Poor diet quality", "average": "Average diet quality",
        "good": "High quality diet (Mediterranean-style)",
    },
    "income": {
        "d1": "< $15,000 / yr  (bottom 10%)", "d2": "$15,000 – $25,000", "d3": "$25,000 – $35,000",
        "d4": "$35,000 – $47,000", "d5": "$47,000 – $60,000  (median)", "d6": "$60,000 – $75,000",
        "d7": "$75,000 – $95,000", "d8": "$95,000 – $130,000", "d9": "$130,000 – $200,000",
        "d10": "> $200,000 / yr  (top 10%)",
    },
    "education": {
        "less_than_hs": "Less than high school", "hs_diploma": "High school diploma / GED",
        "some_college": "Some college, no degree", "bachelors": "Bachelor's degree",
        "graduate": "Graduate / professional degree",
    },
    "social": {
        "isolated": "Socially isolated", "widowed": "Widowed",
        "divorced": "Divorced / separated", "never_married": "Never married",
        "partnered": "Married / partnered", "strong_social": "Partnered + strong social network",
    },
    "race": {
        "white_nh": "Non-Hispanic White", "mena": "Middle Eastern / North African",
        "black_usborn": "Black — US-born", "black_african": "Black — African immigrant",
        "black_caribbean": "Black — Caribbean", "hispanic_mexican": "Hispanic — Mexican-American",
        "hispanic_pr": "Hispanic — Puerto Rican", "hispanic_cuban": "Hispanic — Cuban-American",
        "hispanic_other": "Hispanic — Central/South American",
        "east_asian": "East Asian (Chinese, Japanese, Korean)",
        "southeast_asian": "Southeast Asian (Vietnamese, Cambodian, Thai)",
        "filipino": "Filipino", "south_asian": "South Asian (Indian, Pakistani, Bangladeshi)",
        "american_indian": "American Indian", "alaska_native": "Alaska Native",
        "native_hawaiian": "Native Hawaiian", "pacific_islander": "Other Pacific Islander",
    },
    "conditions": {
        "none": "No chronic conditions", "hypertension_ctrl": "Hypertension — controlled",
        "hypertension_unctrl": "Hypertension — uncontrolled", "diabetes_t1": "Type 1 diabetes",
        "diabetes_t2": "Type 2 diabetes", "heart_disease": "Coronary heart disease",
        "afib": "Atrial fibrillation", "ckd": "Chronic kidney disease",
        "copd": "COPD", "cancer_history": "Cancer history (any)",
        "liver_disease": "Liver disease / cirrhosis", "depression": "Major depression",
        "serious_mental": "Serious mental illness", "hiv_treated": "HIV on modern ART",
        "multi": "Multiple major conditions (2+)",
    },
    "geography": {
        "urban_metro": "Urban / large metro", "suburban": "Suburban / medium metro",
        "small_city": "Small city / micropolitan", "rural": "Rural (non-core county)",
        "appalachia": "Appalachian region", "ms_delta": "Mississippi Delta",
    },
    "occupation": {
        "blue_collar": "Blue collar / manual labor", "service": "Service / food / retail",
        "white_collar": "White collar / professional", "healthcare": "Healthcare worker",
        "unemployed": "Unemployed / not in labor force",
    },
}

FACTOR_GROUPS = [
    ("Lifestyle", ["smoking", "alcohol", "activity", "sleep", "diet", "bmi"]),
    ("Socioeconomic", ["income", "education", "social", "occupation", "geography"]),
    ("Health", ["conditions"]),
    ("Demographics", ["race"]),
]

# ── Helpers ───────────────────────────────────────────────────────────────────
@st.cache_data
def get_baseline_table(sex):
    sex_idx = 0 if sex == "male" else 1
    ages = sorted(SSA_2022.keys())
    qx = [SSA_2022[a][sex_idx] for a in ages]
    return build_life_table(qx)

def get_adjusted_table(sex, selections):
    sex_idx = 0 if sex == "male" else 1
    ages = sorted(SSA_2022.keys())
    qx_base = [SSA_2022[a][sex_idx] for a in ages]
    hr = combined_hr(selections)
    qx_adj = [apply_hr_to_qx(q, hr) for q in qx_base]
    return build_life_table(qx_adj), hr

def prob_reach(table, from_age, to_age):
    if to_age >= len(table) or from_age >= len(table): return 0.0
    lf = table[from_age]["lx"]
    return round(100 * table[to_age]["lx"] / lf, 1) if lf > 0 else 0.0

def dc(d): return "pos" if d >= 0 else "neg"
def ds(d): return f"+{d:.1f}" if d >= 0 else f"{d:.1f}"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 1.25rem;'>
        <div style='font-family:"DM Serif Display",serif;font-size:1.5rem;color:#f0ede8;line-height:1.1;'>
            ⧖ Lifespan<br>Calculator
        </div>
        <div style='font-size:0.7rem;color:#4a4855;margin-top:0.4rem;letter-spacing:0.05em;'>
            SSA 2022 PERIOD LIFE TABLE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">About you</div>', unsafe_allow_html=True)
    sex = st.radio("Sex", ["Male", "Female"], horizontal=True).lower()
    age = st.slider("Current age", 0, 100, 31)

    selections = {}
    for group_name, factors in FACTOR_GROUPS:
        st.markdown(f'<div class="section-title">{group_name}</div>', unsafe_allow_html=True)
        for f in factors:
            meta = RISK_FACTORS[f]
            opts = list(meta["options"].keys())
            ref  = meta["reference"]
            default_idx = opts.index(ref) if ref in opts else 0
            key = st.selectbox(
                meta["label"], opts,
                format_func=lambda k, f=f: LABELS[f][k],
                index=default_idx,
                key=f"sel_{f}",
            )
            selections[f] = key

    st.markdown('<div class="section-title">Display</div>', unsafe_allow_html=True)
    show_baseline = st.toggle("Show population baseline", value=True)

    st.markdown("""
    <div style='margin-top:1.5rem;font-size:0.68rem;color:#3a3845;line-height:1.6;'>
    Hazard ratios applied via logit transformation to SSA 2022 q(x) values.
    Multiplicative combination assumes approximate independence.
    </div>
    """, unsafe_allow_html=True)

# ── Compute ───────────────────────────────────────────────────────────────────
table_base = get_baseline_table(sex)
table_adj, hr = get_adjusted_table(sex, selections)

e_base = table_base[age]["ex"] if age < len(table_base) else 0.0
e_adj  = table_adj[age]["ex"]  if age < len(table_adj)  else 0.0
delta  = e_adj - e_base
expected_age_adj = age + e_adj

max_age   = 110
surv_ages = list(range(age, max_age + 1))
l_base_now = table_base[age]["lx"] if age < len(table_base) else 1
l_adj_now  = table_adj[age]["lx"]  if age < len(table_adj)  else 1

surv_base = [round(100 * table_base[a]["lx"] / l_base_now, 2) if a < len(table_base) else 0 for a in surv_ages]
surv_adj  = [round(100 * table_adj[a]["lx"]  / l_adj_now,  2) if a < len(table_adj)  else 0 for a in surv_ages]

milestones = [65, 75, 85, 90, 95, 100]
mile_base  = [prob_reach(table_base, age, m) for m in milestones]
mile_adj   = [prob_reach(table_adj,  age, m) for m in milestones]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='margin-bottom:1.25rem;'>
    <h1 style='font-size:2.2rem;margin:0;color:#f0ede8;line-height:1.1;'>Your longevity profile</h1>
    <div style='color:#4a4855;font-size:0.8rem;margin-top:0.35rem;'>
        {sex.title()} · Age {age} · SSA 2022 period life table
    </div>
</div>
""", unsafe_allow_html=True)

# ── Metric cards ──────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
hr_pct = (hr - 1) * 100
hr_col = "#f87171" if hr > 1 else "#4ade80"
p75 = prob_reach(table_adj, age, 75) if age < 75 else 100.0

for col, label, val, unit, sub, sub_cls in [
    (c1, "Life expectancy", f"{e_adj:.1f}", "yrs", f"{ds(delta)} vs population", dc(delta)),
    (c2, "Expected age",    f"{expected_age_adj:.0f}", "", "years old", ""),
    (c3, "Odds of reaching 75", f"{p75:.0f}", "%", f"from age {age}", ""),
    (c4, "Risk multiplier", f"{hr:.2f}", "×", f"{abs(hr_pct):.0f}% {'higher' if hr>1 else 'lower'} mortality", dc(-delta)),
]:
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" {'style="color:'+hr_col+';"' if label=="Risk multiplier" else ""}>{val}<span class="metric-unit">{unit}</span></div>
        <div class="metric-delta {sub_cls}">{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1.25rem;'></div>", unsafe_allow_html=True)

# ── Survival curve + milestones ───────────────────────────────────────────────
col_l, col_r = st.columns([3, 2], gap="large")

with col_l:
    st.markdown('<div class="section-title">Survival curve</div>', unsafe_allow_html=True)
    fig = go.Figure()
    if show_baseline:
        fig.add_trace(go.Scatter(
            x=surv_ages, y=surv_base, mode="lines", name="Population baseline",
            line=dict(color="#7ef4cc", width=1.5, dash="dot"),
            fill="tozeroy", fillcolor="rgba(126,244,204,0.04)",
            hovertemplate="%{x}y old · %{y:.1f}% survival<extra>Baseline</extra>",
        ))
    fig.add_trace(go.Scatter(
        x=surv_ages, y=surv_adj, mode="lines", name="Your profile",
        line=dict(color="#b69cf5", width=2.5),
        fill="tozeroy", fillcolor="rgba(182,156,245,0.08)",
        hovertemplate="%{x}y old · %{y:.1f}% survival<extra>Your profile</extra>",
    ))
    fig.add_vline(x=age, line_color="#2a2a35", line_width=1, line_dash="dash",
                  annotation_text=f"  Age {age}", annotation_font_color="#4a4855", annotation_font_size=10)
    fig.add_vline(x=expected_age_adj, line_color="#b69cf5", line_width=1, line_dash="dot",
                  annotation_text=f"  e={expected_age_adj:.0f}", annotation_font_color="#b69cf5", annotation_font_size=10)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#9997a0", size=11),
        margin=dict(l=0, r=0, t=10, b=0), height=310,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                    font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(title="Age", gridcolor="#1e1e26", zerolinecolor="#1e1e26",
                   tickfont=dict(size=10), range=[age, max_age]),
        yaxis=dict(title="Survival (%)", gridcolor="#1e1e26", zerolinecolor="#1e1e26",
                   tickfont=dict(size=10), range=[0, 102], ticksuffix="%"),
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with col_r:
    st.markdown('<div class="section-title">Milestone probabilities</div>', unsafe_allow_html=True)
    valid = [(m, b, a) for m, b, a in zip(milestones, mile_base, mile_adj) if m > age]
    if valid:
        fig2 = go.Figure()
        if show_baseline:
            fig2.add_trace(go.Bar(
                name="Baseline", x=[f"Age {m}" for m, *_ in valid],
                y=[b for _, b, _ in valid], marker_color="#252530",
                marker_line_color="#3a3a4a", marker_line_width=1,
                hovertemplate="%{x}: %{y:.1f}%<extra>Baseline</extra>",
            ))
        fig2.add_trace(go.Bar(
            name="Your profile", x=[f"Age {m}" for m, *_ in valid],
            y=[a for _, _, a in valid], marker_color="#b69cf5",
            hovertemplate="%{x}: %{y:.1f}%<extra>Your profile</extra>",
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#9997a0", size=11),
            margin=dict(l=0, r=0, t=10, b=0), height=310,
            barmode="group", bargap=0.25, bargroupgap=0.08,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                        font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="#1e1e26", tickfont=dict(size=10)),
            yaxis=dict(gridcolor="#1e1e26", tickfont=dict(size=10), range=[0, 105], ticksuffix="%"),
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ── Factor breakdown ──────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Risk factor breakdown</div>', unsafe_allow_html=True)

all_factors = [f for _, flist in FACTOR_GROUPS for f in flist]
cols = st.columns(len(all_factors))
for col, f in zip(cols, all_factors):
    k   = selections[f]
    fhr = RISK_FACTORS[f]["options"][k]["hr"]
    pct = (fhr - 1) * 100
    col_c = "#f87171" if fhr > 1.05 else "#4ade80" if fhr < 0.95 else "#9997a0"
    sign  = "+" if pct >= 0 else ""
    with col:
        st.markdown(f"""
        <div class="factor-card">
            <div class="flabel">{RISK_FACTORS[f]['label']}</div>
            <div class="fval">{LABELS[f][k]}</div>
            <div class="fhr" style="color:{col_c};">{fhr:.2f}× <span style="color:#3a3845;font-size:0.72rem;">({sign}{pct:.0f}%)</span></div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

# ── Waterfall ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Impact on life expectancy by factor</div>', unsafe_allow_html=True)

sex_idx  = 0 if sex == "male" else 1
ages_all = sorted(SSA_2022.keys())
qx_base  = [SSA_2022[a][sex_idx] for a in ages_all]
t_ref    = build_life_table(qx_base)

impacts, wlabels = [], []
for f in all_factors:
    k   = selections[f]
    fhr = RISK_FACTORS[f]["options"][k]["hr"]
    qx_w = [apply_hr_to_qx(q, fhr) for q in qx_base]
    t_w  = build_life_table(qx_w)
    impact = (t_w[age]["ex"] - t_ref[age]["ex"]) if age < len(t_ref) else 0.0
    impacts.append(round(impact, 2))
    wlabels.append(RISK_FACTORS[f]["label"])

bar_colors = ["#f87171" if v < -0.1 else "#4ade80" if v > 0.1 else "#3a3a48" for v in impacts]
fig3 = go.Figure(go.Bar(
    x=wlabels, y=impacts, marker_color=bar_colors, marker_line_width=0,
    hovertemplate="%{x}<br>%{y:+.2f} years<extra></extra>",
    text=[f"{v:+.1f}y" for v in impacts], textposition="outside",
    textfont=dict(size=10, color="#9997a0"),
))
fig3.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#9997a0", size=11),
    margin=dict(l=0, r=0, t=20, b=0), height=230, showlegend=False,
    xaxis=dict(gridcolor="#1e1e26", tickfont=dict(size=10)),
    yaxis=dict(gridcolor="#1e1e26", zerolinecolor="#3a3845", zerolinewidth=1,
               tickfont=dict(size=10), ticksuffix=" yrs"),
)
st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

# ── Footer with methodology link ──────────────────────────────────────────────
st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
col_foot_l, col_foot_r = st.columns([2, 1])
with col_foot_l:
    st.markdown("""
    <div style='font-size:0.72rem;color:#3a3845;line-height:1.7;'>
        SSA 2022 period life table · Logit-transformed hazard ratios · Multiplicative independence assumption ·
        For educational purposes only · Not medical advice
    </div>""", unsafe_allow_html=True)
with col_foot_r:
    st.markdown("""
    <a href="/Methodology" target="_self" style="display:inline-flex;align-items:center;gap:6px;
       background:#1e1e28;border:1px solid #3a3a50;border-radius:8px;padding:8px 16px;
       font-size:0.82rem;color:#b69cf5;text-decoration:none;">
       📖 Methodology &amp; Sources →
    </a>""", unsafe_allow_html=True)
