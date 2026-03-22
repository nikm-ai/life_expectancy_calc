import streamlit as st

st.set_page_config(
    page_title="Methodology & Sources — Lifespan Calculator",
    page_icon="⧖",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0e0e11; color: #f0ede8; }
[data-testid="stSidebar"] { background: #16161a; border-right: 1px solid #2a2a32; }
h1, h2, h3 { font-family: 'DM Serif Display', serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 860px; }

.section { margin: 2.5rem 0; }
.section h2 { font-size: 1.5rem; color: #f0ede8; margin-bottom: 0.25rem; }
.section-sub { font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase;
               color: #4a4855; margin-bottom: 1.25rem; }
.prose { color: #b4b2b8; line-height: 1.8; font-size: 0.92rem; }
.prose strong { color: #f0ede8; font-weight: 500; }

.factor-block {
    background: #16161a;
    border: 1px solid #2a2a35;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.factor-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: #f0ede8;
    margin-bottom: 0.5rem;
}
.factor-desc { color: #9997a0; font-size: 0.86rem; line-height: 1.7; margin-bottom: 0.75rem; }
.source-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.source-table th {
    text-align: left; color: #4a4855; font-weight: 500;
    letter-spacing: 0.06em; text-transform: uppercase; font-size: 0.72rem;
    padding: 4px 8px 8px 0; border-bottom: 1px solid #2a2a35;
}
.source-table td { padding: 6px 8px 6px 0; color: #9997a0; vertical-align: top; border-bottom: 1px solid #1e1e26; }
.source-table td:first-child { color: #f0ede8; font-weight: 400; white-space: nowrap; min-width: 160px; }
.source-table td.hr { color: #b69cf5; font-weight: 500; white-space: nowrap; min-width: 60px; }

.caveat-box {
    background: #1a1820;
    border: 1px solid #3a3060;
    border-left: 3px solid #7f77dd;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin: 1.5rem 0;
    color: #9997a0;
    font-size: 0.86rem;
    line-height: 1.7;
}
.caveat-box strong { color: #b69cf5; }

.formula-box {
    background: #111118;
    border: 1px solid #2a2a35;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-family: 'Courier New', monospace;
    font-size: 0.88rem;
    color: #7ef4cc;
    margin: 1rem 0;
    line-height: 1.8;
}
.chip {
    display: inline-block;
    background: #1e1e28;
    border: 1px solid #3a3a50;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.78rem;
    color: #9997a0;
    margin: 2px 3px 2px 0;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom:2rem;'>
    <div style='font-size:0.78rem; letter-spacing:0.1em; text-transform:uppercase;
                color:#4a4855; margin-bottom:0.5rem;'>← back to calculator</div>
    <h1 style='font-size:2.4rem; margin:0; color:#f0ede8;'>Methodology & Sources</h1>
    <div style='color:#4a4855; font-size:0.82rem; margin-top:0.4rem;'>
        How life expectancy adjustments are calculated, and where every number comes from.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Core Methodology ──────────────────────────────────────────────────────────
st.markdown("""
<div class="section">
<h2>Core methodology</h2>
<div class="section-sub">Actuarial engine</div>
<div class="prose">
The calculator starts from the <strong>SSA 2022 period life table</strong> (published in the 2025 Trustees Report),
which provides age-specific probabilities of death q(x) for males and females from age 0 to 119.
A period life table uses mortality rates from a single calendar year — in this case 2022 — applied
to a hypothetical cohort, producing a snapshot of current mortality conditions rather than a
projection of any real cohort's future experience.
<br><br>
Each risk factor is associated with a <strong>mortality hazard ratio (HR)</strong> drawn from published
epidemiological literature. HRs are applied to the baseline q(x) values via logit transformation
to keep adjusted probabilities bounded within (0, 1):
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="formula-box">
logit(q_adj) = logit(q_base) + log(HR)<br><br>
where logit(p) = log(p / (1 − p))<br><br>
q_adj = 1 / (1 + exp(−logit_adj))
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="prose">
This is equivalent to a proportional hazards model with a multiplicative HR applied to the
baseline hazard. The logit transformation prevents adjusted q(x) values from exceeding 1 at
high risk levels, which would occur under naive multiplicative scaling.
<br><br>
Risk factor HRs are <strong>multiplied together</strong> across dimensions, assuming approximate
independence between factors. This is a simplification — in reality, risk factors are correlated
(e.g., low income predicts poor diet, low activity, and higher smoking rates). Combined HRs at
extremes should therefore be interpreted as upper-bound estimates of joint risk.
</div>
<div class="caveat-box">
<strong>Important limitations.</strong> This calculator is for educational purposes only.
Period life expectancy reflects current mortality rates applied to a hypothetical cohort —
it is not a prediction of any individual's lifespan. Hazard ratios are population-level averages
from observational studies; they encode correlation, not pure causation, and vary across age groups,
sex, and time periods. Combining HRs multiplicatively assumes independence across risk factors,
which overstates joint risk when factors are correlated. Race/ethnicity HRs reflect population-level
differentials that absorb unmeasured SES, structural, and access-related mediators.
</div>
""", unsafe_allow_html=True)

# ── Baseline data ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="section">
<h2>Baseline life table</h2>
<div class="section-sub">SSA 2022 period life table</div>
<div class="prose">
<strong>Source:</strong> Social Security Administration Office of the Chief Actuary.
"Period Life Table, 2022, as used in the 2025 Trustees Report."
<a href="https://www.ssa.gov/oact/STATS/table4c6.html" style="color:#b69cf5;">ssa.gov/oact/STATS/table4c6.html</a>
<br><br>
The SSA area population includes residents of the 50 states and DC, civilian residents of US territories,
federal civilian employees abroad, and US citizens living outside the country who are insured for
Social Security benefits. It is slightly broader than the standard US resident population used
by NCHS, and mortality rates are calculated from death records linked to Social Security records.
<br><br>
Baseline life expectancy at birth: <strong>74.74 years (male)</strong> · <strong>80.19 years (female)</strong>.
The 2022 table reflects COVID-19 excess mortality that had not fully resolved by that year;
male life expectancy at birth declined approximately 2.4 years from the 2019 pre-pandemic baseline.
</div>
</div>
""", unsafe_allow_html=True)

# ── Factor sections ───────────────────────────────────────────────────────────
def factor_section(title, subtitle, description, rows, caveat=None):
    st.markdown(f"""
    <div class="section">
    <h2>{title}</h2>
    <div class="section-sub">{subtitle}</div>
    <div class="prose">{description}</div>
    {"<div class='caveat-box'>" + caveat + "</div>" if caveat else ""}
    <div class="factor-block">
    <table class="source-table">
    <thead><tr><th>Category</th><th>HR</th><th>Source / notes</th></tr></thead>
    <tbody>
    {"".join(f"<tr><td>{r[0]}</td><td class='hr'>{r[1]}</td><td>{r[2]}</td></tr>" for r in rows)}
    </tbody></table></div></div>
    """, unsafe_allow_html=True)

factor_section(
    "Smoking", "Mortality hazard ratios by smoking status",
    "Smoking is the single largest modifiable mortality risk factor in the US. The 2014 MMWR Surgeon General's Report "
    "estimated current smoking accounts for approximately 480,000 deaths annually. The HR gradient between never, "
    "former, and current smokers reflects both duration and intensity of exposure, as well as the reversibility of "
    "risk after cessation. Former smokers who quit before age 40 recover nearly all lost life expectancy by their 50s.",
    [
        ("Never smoker", "1.00×", "Reference — MMWR 2014; Jha et al. NEJM 2013"),
        ("Former, light (quit >10yr or <10 pack-yrs)", "1.14×", "Jha et al. NEJM 2013 — large prospective UK cohort"),
        ("Former, heavy (quit <10yr or >20 pack-yrs)", "1.55×", "Jha et al. NEJM 2013"),
        ("Current, light (<10 cigs/day)", "2.00×", "MMWR 2014 Surgeon General Report"),
        ("Current, heavy (≥1 pack/day)", "3.20×", "MMWR 2014; Doll et al. BMJ 2004 — British Doctors Study"),
        ("Vaping / e-cigarettes only", "1.35×", "Bhatta & Glantz AJPM 2020 — emerging; wider uncertainty"),
    ],
    caveat="<strong>Pack-years caveat.</strong> The former smoker HR is an average across a heterogeneous population. "
           "Someone who smoked 40 pack-years and quit at 60 has substantially higher residual risk than someone who "
           "smoked 5 pack-years and quit at 25. The light/heavy split is an approximation; pack-year-based models "
           "exist in the clinical literature but require more detailed input data."
)

factor_section(
    "BMI", "Body mass index mortality gradient",
    "The relationship between BMI and mortality follows a J-curve, with lowest mortality in the normal range "
    "(18.5–24.9). The Global BMI Mortality Collaboration meta-analysis pooled 239 prospective studies with "
    "10.6 million participants — the largest such analysis to date. All-cause mortality HRs are reported "
    "relative to the normal BMI reference category, excluding the first 5 years of follow-up and current "
    "smokers to reduce confounding.",
    [
        ("Underweight (<18.5)", "1.51×", "Global BMI Mortality Collaboration, Lancet 2016"),
        ("Normal (18.5–24.9)", "1.00×", "Reference — Lancet 2016"),
        ("Overweight (25–29.9)", "1.07×", "Lancet 2016 — attenuated in older adults ('obesity paradox')"),
        ("Obese Class I (30–34.9)", "1.20×", "Lancet 2016"),
        ("Obese Class II (35–39.9)", "1.45×", "Lancet 2016"),
        ("Obese Class III (40+)", "1.88×", "Lancet 2016"),
    ]
)

factor_section(
    "Alcohol", "Alcohol consumption mortality gradient",
    "Alcohol mortality follows a well-documented J-curve: moderate drinkers have slightly lower all-cause "
    "mortality than non-drinkers, primarily through cardiovascular benefits, though this protective effect "
    "is contested and may reflect confounding from sick quitters among the non-drinking reference group. "
    "Heavy and severe use carry substantial mortality risk across cardiovascular, liver, cancer, and injury pathways.",
    [
        ("Non-drinker", "1.05×", "Ronksley et al. BMJ 2011; slight excess vs. moderate (J-curve effect)"),
        ("Moderate (≤14 drinks/week)", "1.00×", "Reference — GBD 2020; Ronksley et al. BMJ 2011"),
        ("Heavy (15–28 drinks/week)", "1.40×", "GBD 2020; Ronksley et al. BMJ 2011"),
        ("Severe / AUD (>28 drinks/week)", "2.70×", "GBD 2020; Rehm et al. Lancet 2017"),
    ],
    caveat="<strong>J-curve controversy.</strong> The apparent protective effect of moderate alcohol is contested. "
           "A 2018 GBD analysis concluded there is no safe level of alcohol consumption when all health outcomes "
           "are considered (including cancer). The 1.05× HR for non-drinkers reflects the all-cause mortality "
           "J-curve from cardiovascular studies, but this may not hold for all populations or time periods."
)

factor_section(
    "Physical Activity", "Exercise and all-cause mortality",
    "Physical activity is among the most powerful mortality predictors, with a dose-response relationship "
    "that extends well above current public health guidelines. Arem et al. (2015) pooled data from 6 prospective "
    "cohorts (661,137 individuals) and found mortality benefits plateauing around 3–5× the recommended minimum "
    "activity level. The WHO recommends 150–300 minutes of moderate-intensity activity per week for adults.",
    [
        ("Sedentary (<30 min/week)", "1.35×", "Arem et al. JAMA Intern Med 2015 — pooled cohort analysis"),
        ("Insufficient (30–150 min/week)", "1.15×", "Arem et al. 2015"),
        ("Active (150–300 min/week)", "1.00×", "Reference — WHO guidelines met"),
        ("Highly active (>300 min/week)", "0.80×", "Arem et al. 2015 — benefit plateaus above ~5× guidelines"),
    ]
)

factor_section(
    "Sleep", "Sleep duration and mortality",
    "Both short and long sleep duration are associated with elevated mortality, though the mechanisms differ. "
    "Short sleep (<6 hrs) is associated with cardiovascular disease, metabolic dysfunction, and immune impairment. "
    "Long sleep (>9 hrs) is partially a disease marker — chronic illness increases sleep need — making "
    "the long sleep HR partly a reflection of underlying morbidity rather than a causal effect of sleep itself.",
    [
        ("Short (<6 hrs/night)", "1.13×", "Liu et al. Sleep 2017 — meta-analysis of 74 studies, 2.2M subjects"),
        ("Normal (7–8 hrs/night)", "1.00×", "Reference — Liu et al. Sleep 2017"),
        ("Long (>9 hrs/night)", "1.30×", "Liu et al. Sleep 2017 — partly disease marker"),
    ]
)

factor_section(
    "Diet Quality", "Dietary patterns and mortality",
    "Diet quality is associated with mortality primarily through cardiovascular, cancer, and metabolic pathways. "
    "The GBD 2019 Diet Collaborators estimated that suboptimal diet accounted for 11 million deaths globally. "
    "Mediterranean-style diets — high in vegetables, legumes, whole grains, fish, and olive oil — show the "
    "strongest evidence for mortality reduction. The Diet Quality Index (DQI) and Healthy Eating Index (HEI) "
    "are the most widely validated composite dietary quality measures.",
    [
        ("Poor diet quality", "1.22×", "GBD Diet Collaborators, Lancet 2019"),
        ("Average diet quality", "1.00×", "Reference"),
        ("High quality (Mediterranean-style)", "0.85×", "Sofi et al. BMJ 2008 meta-analysis; GBD 2019"),
    ]
)

factor_section(
    "Income", "Household income and life expectancy",
    "Chetty et al. (2016) linked IRS tax records to Social Security death records for 1.4 billion person-years "
    "of data, finding that higher income is associated with greater longevity throughout the distribution — "
    "with no evidence of a threshold below which income no longer matters. The top 1% of income earners live "
    "approximately 10–15 years longer than the bottom 1%. Dollar ranges reflect the approximate 2024 US "
    "household income distribution (Census ACS). Intermediate decile HRs (d2–d4, d6–d9) are interpolated "
    "from the Chetty quartile anchors and NCI income-mortality gradient data.",
    [
        ("d1 — bottom 10% (~<$15k/yr)", "2.10×", "Chetty et al. JAMA 2016 / NCI income-mortality gradient"),
        ("d2 (~$15k–$25k/yr)", "1.75×", "Interpolated from Chetty quartile anchors"),
        ("d3 (~$25k–$35k/yr)", "1.45×", "Interpolated"),
        ("d4 (~$35k–$47k/yr)", "1.20×", "Interpolated"),
        ("d5 (~$47k–$60k/yr)", "1.00×", "Reference — approximate US median household income"),
        ("d6 (~$60k–$75k/yr)", "0.88×", "Interpolated"),
        ("d7 (~$75k–$95k/yr)", "0.80×", "Interpolated"),
        ("d8 (~$95k–$130k/yr)", "0.74×", "Interpolated"),
        ("d9 (~$130k–$200k/yr)", "0.69×", "Interpolated"),
        ("d10 — top 10% (~>$200k/yr)", "0.62×", "Chetty et al. JAMA 2016"),
    ]
)

factor_section(
    "Education", "Educational attainment and mortality",
    "Education is one of the strongest socioeconomic predictors of mortality, with effects that persist "
    "after controlling for income. Pathways include health literacy, occupational access, health behavior "
    "patterns, and stress exposure. The mortality gap between college graduates and non-graduates has "
    "widened substantially since the 1980s. Olshansky et al. (2012) found that white women without "
    "a high school diploma experienced declining life expectancy between 1990 and 2008.",
    [
        ("Less than high school", "1.45×", "Meara et al. Health Affairs 2008; Olshansky et al. Health Affairs 2012"),
        ("High school diploma / GED", "1.20×", "Meara et al. 2008"),
        ("Some college, no degree", "1.08×", "Meara et al. 2008"),
        ("Bachelor's degree", "1.00×", "Reference"),
        ("Graduate / professional degree", "0.88×", "Meara et al. 2008; NCHS 2012"),
    ]
)

factor_section(
    "Social Connection", "Marital status and social isolation",
    "Social isolation and loneliness are now recognized as major mortality risk factors, with effect sizes "
    "comparable to smoking 15 cigarettes per day. Holt-Lunstad et al. (2010) meta-analyzed 148 studies "
    "(308,849 participants) and found that adequate social relationships were associated with a 50% increased "
    "likelihood of survival. The married/partnered survival advantage is well-replicated across cultures "
    "and time periods, though the protective effect is stronger for men than women.",
    [
        ("Socially isolated", "1.45×", "Holt-Lunstad et al. PLOS Med 2010 — meta-analysis, 308k subjects"),
        ("Widowed", "1.20×", "Holt-Lunstad 2010; elevated in first year post-loss"),
        ("Divorced / separated", "1.25×", "Holt-Lunstad 2010"),
        ("Never married", "1.10×", "Holt-Lunstad 2010"),
        ("Married / long-term partnered", "1.00×", "Reference"),
        ("Partnered + strong social network", "0.85×", "Holt-Lunstad 2010 — combined social integration"),
    ]
)

factor_section(
    "Race / Ethnicity", "Race/ethnicity mortality differentials",
    "Race/ethnicity HRs are derived from NCHS linked mortality data (Arias et al. 2021) and supplementary "
    "literature for subdivided categories. These HRs reflect population-level differentials that absorb "
    "structural racism, differential SES, healthcare access, occupational exposure, and neighborhood effects — "
    "they are not estimates of biological race effects. Combining race HRs with income and education HRs "
    "will double-count some of the pathway through which race affects mortality.",
    [
        ("Non-Hispanic White", "1.00×", "Reference — NCHS Arias et al. 2021"),
        ("Middle Eastern / North African", "0.90×", "Dallo et al. Ethn Dis 2008; Arab-American cohort studies. Classified as White in US vital statistics — HR is estimated from community-based studies."),
        ("Non-Hispanic Black, US-born", "1.22×", "NCHS Arias 2021; Williams et al. — structural racism, weathering hypothesis"),
        ("African immigrant (Sub-Saharan)", "0.90×", "Singh & Siahpush AJPH 2002 — strong healthy immigrant effect"),
        ("Caribbean Black", "1.05×", "Read et al. Soc Sci Med 2005 — between US-born Black and African immigrant"),
        ("Mexican-American", "0.80×", "Strongest Hispanic paradox; Markides & Coreil 1986; NCHS"),
        ("Puerto Rican", "0.97×", "Attenuated paradox; Borrell 2006; NCHS"),
        ("Cuban-American", "0.87×", "Abraído-Lanza et al. AJPH 1999"),
        ("Central / South American", "0.83×", "Healthy immigrant effect; NCHS Other Hispanic category"),
        ("East Asian (Chinese, Japanese, Korean)", "0.60×", "Lowest US mortality group; NCHS Arias 2021 disaggregated data"),
        ("Southeast Asian (Vietnamese, Cambodian, Thai)", "0.72×", "Higher CVD and cancer than East Asian aggregate; NCHS"),
        ("Filipino", "0.78×", "Elevated CVD and diabetes vs. East Asian; Araneta & Barrett-Connor 2005"),
        ("South Asian (Indian, Pakistani, Bangladeshi)", "0.72×", "Elevated CVD offsets Asian advantage; Palaniappan et al. Circulation 2010; Misra et al. 2017"),
        ("American Indian (continental)", "1.35×", "NCHS Arias 2021; IHS data — data quality concerns (undercounting)"),
        ("Alaska Native", "1.45×", "IHS / Alaska DHSS data — higher than continental AIAN"),
        ("Native Hawaiian", "1.10×", "Hawaii DHHL cohort; elevated obesity, CVD, T2D"),
        ("Other Pacific Islander", "0.88×", "NCHS NHOPI residual category"),
    ],
    caveat="<strong>Data quality warning.</strong> American Indian / Alaska Native mortality is systematically "
           "underestimated in vital statistics due to racial misclassification on death certificates. "
           "True AIAN mortality disadvantage is likely larger than the HRs shown. MENA mortality is not "
           "tracked separately in US vital statistics — the HR is estimated from community-based studies "
           "and carries wider uncertainty. South Asian and Southeast Asian HRs overlap with the aggregate "
           "Non-Hispanic Asian category, from which they are subdivided using diaspora health literature."
)

factor_section(
    "Chronic Conditions", "Disease-specific mortality hazard ratios",
    "Chronic condition HRs reflect all-cause mortality among individuals with each condition relative to "
    "those without. Conditions are treated as independent in the multiplicative model, which overstates "
    "combined risk for highly comorbid conditions (e.g., T2D + heart disease + CKD often co-occur). "
    "The 'multiple major conditions' category is intended to approximate the comorbidity cluster rather "
    "than simply multiplying individual HRs.",
    [
        ("None", "1.00×", "Reference"),
        ("Hypertension, controlled", "1.05×", "Ettehad et al. Lancet 2016 — BP-lowering meta-analysis"),
        ("Hypertension, uncontrolled", "1.42×", "Ettehad et al. Lancet 2016"),
        ("Type 1 diabetes", "2.60×", "Livingstone et al. JAMA 2015 — Scottish nationwide cohort"),
        ("Type 2 diabetes", "1.65×", "Emerging Risk Factors Collaboration, JAMA 2011 — 820k subjects"),
        ("Coronary heart disease", "1.90×", "AHA Heart Disease & Stroke Statistics 2023"),
        ("Atrial fibrillation", "1.70×", "Benjamin et al. Circulation 2019"),
        ("Chronic kidney disease", "1.90×", "Go et al. NEJM 2004 — 1.1M subjects"),
        ("COPD", "2.20×", "GBD COPD Collaborators, Lancet 2017"),
        ("Cancer history (any)", "1.85×", "SEER / ACS Cancer Facts 2023 — average across cancer types"),
        ("Chronic liver disease / cirrhosis", "2.90×", "GBD Cirrhosis Collaborators 2020"),
        ("Major depressive disorder", "1.52×", "Walker et al. JAMA Psychiatry 2015 — meta-analysis of 29 studies"),
        ("Serious mental illness", "2.50×", "Walker et al. JAMA Psychiatry 2015 — schizophrenia, bipolar I"),
        ("HIV on modern ART", "1.65×", "ART Cohort Collaboration, Lancet 2017 — dramatic improvement from pre-ART era"),
        ("Multiple major conditions (2+)", "3.20×", "Estimated from comorbidity literature; not a simple product"),
    ]
)

factor_section(
    "Geography", "Geographic mortality variation",
    "Geographic mortality variation in the US is substantial — a resident of a distressed Appalachian county "
    "has a life expectancy comparable to residents of low-income developing countries, while residents of "
    "affluent urban counties match the healthiest populations in the world. NCHS publishes annual Urban-Rural "
    "classification data linking mortality to county-level urbanicity. The Appalachian and Mississippi Delta "
    "HRs reflect the specific mortality burden of those economically distressed regions.",
    [
        ("Urban / large metropolitan", "1.00×", "Reference — NCHS Urban-Rural Classification 2023"),
        ("Suburban / medium metro", "1.02×", "NCHS 2023"),
        ("Small city / micropolitan", "1.06×", "NCHS 2023"),
        ("Rural (non-core county)", "1.23×", "Cosby et al. JAMA 2019 — rural mortality gap widening since 1999"),
        ("Appalachian region (distressed counties)", "1.38×", "Hendryx & Ahern AJPH 2014; CDC Atlas"),
        ("Mississippi Delta", "1.45×", "CDC Atlas of Heart Disease; highest US county-level mortality region"),
    ]
)

factor_section(
    "Occupation", "Occupational mortality differentials",
    "Occupation affects mortality through multiple pathways: physical hazard and injury exposure, occupational "
    "carcinogen contact, psychosocial stress, and health behavior norms. Healthcare workers show a survival "
    "advantage attributed to better health literacy, access to care, and preventive screening uptake. "
    "Unemployment carries a substantial mortality risk, though this reflects both direct effects (loss of "
    "income, social connection, purpose) and selection (people in poor health are more likely to be unemployed).",
    [
        ("Blue collar / manual labor", "1.22×", "NIOSH occupational mortality data; physical hazard, injury, exposure"),
        ("Service / food / retail", "1.12×", "CDC NHIS occupational mortality — physical demand, lower wages"),
        ("White collar / professional", "1.00×", "Reference"),
        ("Healthcare worker", "0.85×", "Schwartz et al. APHA 2018 — healthy worker effect + access advantage"),
        ("Unemployed / not in labor force", "1.50×", "Roelfs et al. Am J Epidemiology 2011 — meta-analysis, 42 studies"),
    ]
)

# ── Further reading ───────────────────────────────────────────────────────────
st.markdown("""
<div class="section">
<h2>Key references</h2>
<div class="section-sub">Primary literature</div>
<div class="prose" style="column-count:1;">
<strong>Baseline data</strong><br>
Social Security Administration Office of the Chief Actuary. "Period Life Table, 2022, as used in the 2025 Trustees Report." <a href="https://www.ssa.gov/oact/STATS/table4c6.html" style="color:#b69cf5;">ssa.gov/oact/STATS</a>
<br><br>
<strong>Income & SES</strong><br>
Chetty R, Stepner M, Abraham S, et al. "The Association Between Income and Life Expectancy in the United States, 2001–2014." <em>JAMA</em> 2016;315(16):1750–1766.
<br><br>
Meara ER, Richards S, Cutler DM. "The Gap Gets Bigger: Changes in Mortality and Life Expectancy, by Education, 1981–2000." <em>Health Affairs</em> 2008;27(2):350–360.
<br><br>
<strong>Smoking</strong><br>
Jha P, Ramasundarahettige C, Landsman V, et al. "21st-Century Hazards of Smoking and Benefits of Cessation in the United States." <em>NEJM</em> 2013;368:341–350.
<br><br>
US Department of Health and Human Services. "The Health Consequences of Smoking — 50 Years of Progress." MMWR 2014.
<br><br>
<strong>BMI</strong><br>
Global BMI Mortality Collaboration. "Body-mass index and all-cause mortality: individual-participant-data meta-analysis of 239 prospective studies in four continents." <em>Lancet</em> 2016;388(10046):776–786.
<br><br>
<strong>Physical activity</strong><br>
Arem H, Moore SC, Patel A, et al. "Leisure Time Physical Activity and Mortality." <em>JAMA Intern Med</em> 2015;175(6):959–967.
<br><br>
<strong>Social connection</strong><br>
Holt-Lunstad J, Smith TB, Layton JB. "Social Relationships and Mortality Risk: A Meta-analytic Review." <em>PLOS Med</em> 2010;7(7):e1000316.
<br><br>
<strong>Alcohol</strong><br>
Ronksley PE, Brien SE, Turner BJ, et al. "Association of alcohol consumption with selected cardiovascular disease outcomes: a systematic review and meta-analysis." <em>BMJ</em> 2011;342:d671.
<br><br>
<strong>Sleep</strong><br>
Liu TZ, Xu C, Rota M, et al. "Sleep duration and risk of all-cause mortality: A flexible, non-linear, meta-regression of 40 prospective cohort studies." <em>Sleep Med Rev</em> 2017;32:28–36.
<br><br>
<strong>Diet</strong><br>
GBD 2019 Diet Collaborators. "Health effects of dietary risks in 195 countries." <em>Lancet</em> 2019;393(10184):1958–1972.
<br><br>
<strong>Race / ethnicity</strong><br>
Arias E, Tejada-Vera B, Kochanek KD, Ahmad FB. "Provisional Life Expectancy Estimates for 2021." NCHS Vital Statistics Rapid Release 2022.
<br><br>
Palaniappan LP, Araneta MR, Assimes TL, et al. "Call to Action: Cardiovascular Disease in Asian Americans." <em>Circulation</em> 2010;122(12):1242–1252.
<br><br>
Chetty R, et al. "The association between income and life expectancy in the United States, 2001–2014." <em>JAMA</em> 2016. (Also primary source for geography analysis by income x geography interaction.)
<br><br>
<strong>Chronic conditions</strong><br>
Walker ER, McGee RE, Druss BG. "Mortality in mental disorders and global disease burden implications." <em>JAMA Psychiatry</em> 2015;72(4):334–341.
<br><br>
Go AS, Chertow GM, Fan D, et al. "Chronic Kidney Disease and the Risks of Death, Cardiovascular Events, and Hospitalization." <em>NEJM</em> 2004;351:1296–1305.
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='margin-top:3rem; border-top:1px solid #1e1e26; padding-top:1.25rem;
     font-size:0.72rem; color:#3a3845; line-height:1.7;'>
    Lifespan Calculator · SSA 2022 Period Life Table · For educational purposes only ·
    Not medical advice
</div>
""", unsafe_allow_html=True)
