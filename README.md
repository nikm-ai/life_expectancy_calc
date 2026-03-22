# ⧖ Lifespan Calculator

A personalized actuarial life expectancy calculator built on the SSA 2022 period life table. Input your age, sex, and risk profile across 13 dimensions to see your adjusted survival curve, milestone probabilities, and how each factor independently shifts your life expectancy.

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![Streamlit](https://img.shields.io/badge/streamlit-1.32%2B-red) ![License](https://img.shields.io/badge/license-MIT-green)

---

## Quickstart

```bash
git clone https://github.com/YOUR_USERNAME/lifespan-calculator.git
cd lifespan-calculator
pip install -r requirements.txt
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501). The methodology and sources page is accessible via the link in the app footer, or directly at `http://localhost:8501/Methodology`.

---

## What it does

The app takes your age, sex, and selections across 13 risk factor dimensions and produces:

- **Personalized life expectancy** — remaining years from your current age, adjusted from the SSA 2022 baseline
- **Expected age at death** — your current age plus adjusted life expectancy
- **Odds of reaching key milestones** — probability of surviving to 65, 75, 85, 90, 95, and 100
- **Risk multiplier** — combined hazard ratio across all selected factors
- **Survival curve** — probability of surviving to each age from now to 110, vs. population baseline
- **Factor impact waterfall** — how each risk factor independently adds or subtracts years

All of this updates live as you adjust any input in the sidebar.

---

## Risk factors modeled

13 dimensions, 89 total levels.

| Factor | Levels | Reference | Sources |
|---|---|---|---|
| **Smoking** | 6 | Never smoker | Jha et al. NEJM 2013; MMWR 2014; Doll et al. BMJ 2004 |
| **BMI** | 6 | Normal (18.5–24.9) | Global BMI Mortality Collaboration, Lancet 2016 |
| **Alcohol** | 4 | Moderate (≤14/week) | Ronksley et al. BMJ 2011; GBD 2020; Rehm et al. Lancet 2017 |
| **Physical activity** | 4 | Active (150–300 min/week) | Arem et al. JAMA Intern Med 2015 |
| **Sleep** | 3 | Normal (7–8 hrs) | Liu et al. Sleep Med Rev 2017 |
| **Diet quality** | 3 | Average | GBD Diet Collaborators, Lancet 2019; Sofi et al. BMJ 2008 |
| **Household income** | 10 deciles | 5th decile (~$47–60k/yr) | Chetty et al. JAMA 2016; NCI |
| **Education** | 5 | Bachelor's degree | Meara et al. Health Affairs 2008 |
| **Social connection** | 6 | Married/partnered | Holt-Lunstad et al. PLOS Med 2010 |
| **Race / ethnicity** | 17 | Non-Hispanic White | NCHS Arias et al. 2021; diaspora health literature |
| **Chronic conditions** | 15 | None | Multiple — see Methodology page |
| **Geography** | 6 | Urban / large metro | NCHS Urban-Rural 2023; Cosby et al. JAMA 2019 |
| **Occupation** | 5 | White collar / professional | NIOSH; Roelfs et al. Am J Epidemiology 2011 |

### Race / ethnicity categories

17 categories covering the major US racial/ethnic groups and clinically meaningful subdivisions:

- Non-Hispanic White · Middle Eastern / North African
- Non-Hispanic Black: US-born · African immigrant · Caribbean Black
- Hispanic: Mexican-American · Puerto Rican · Cuban-American · Central/South American
- Asian: East Asian · Southeast Asian · Filipino · South Asian
- American Indian · Alaska Native
- Native Hawaiian · Other Pacific Islander

### Chronic conditions covered

15 levels including: no conditions, hypertension (controlled and uncontrolled), Type 1 diabetes, Type 2 diabetes, coronary heart disease, atrial fibrillation, chronic kidney disease, COPD, cancer history, liver disease/cirrhosis, major depressive disorder, serious mental illness, HIV on modern ART, and multiple major conditions.

---

## Methodology

### Baseline

q(x) values from the **SSA 2022 period life table** (2025 Trustees Report). This table covers ages 0–119 for males and females separately, using mortality data from the Social Security area population.

Baseline life expectancy at birth: **74.74 years (male)** · **80.19 years (female)**

### Hazard ratio application

Each risk factor is assigned a mortality hazard ratio (HR) from published epidemiological literature. HRs are applied to baseline q(x) values via **logit transformation**:

```
logit(q_adj) = logit(q_base) + log(HR)
q_adj = 1 / (1 + exp(−logit_adj))
```

This is equivalent to a proportional hazards model and keeps adjusted probabilities bounded within (0, 1), which naive multiplicative scaling does not.

### Combining factors

HRs are **multiplied together** across all 13 dimensions, assuming approximate independence. This is a simplification — risk factors are correlated in the real population (low income predicts poor diet, lower activity, higher smoking rates, etc.), so combined HRs at extremes overstate joint risk.

### Limitations

- **Period vs. cohort**: A period life table reflects current mortality rates, not projections of future medical progress. Actual cohort life expectancy for someone alive today will likely be higher than period estimates suggest.
- **Multiplicative independence**: Assumes risk factors are uncorrelated. Combining many high-risk factors produces HRs that exceed what real-world comorbidity literature supports.
- **Population averages**: HRs are group-level estimates with confidence intervals that widen substantially for smaller subpopulations.
- **Race/ethnicity**: Race HRs absorb structural, socioeconomic, and access-related factors — they do not represent biological effects. Combining race HRs with income and education HRs will partially double-count these pathways.
- **Not medical advice**: This tool is for educational and research purposes only.

Full methodology with per-factor source citations is available in the app at the Methodology & Sources page.

---

## CLI usage

The actuarial engine (`life_table_calculator.py`) can be used independently to generate CSVs.

### Single subgroup

```bash
python life_table_calculator.py --single \
  --sex female \
  --smoking never \
  --bmi normal \
  --alcohol moderate \
  --activity active \
  --sleep normal \
  --diet good \
  --income d7 \
  --education graduate \
  --social partnered \
  --race east_asian \
  --conditions none \
  --geography urban_metro \
  --occupation healthcare \
  --output my_profile.csv
```

### See all options and HRs

```bash
python life_table_calculator.py --help-factors
```

### Full enumeration (use with caution)

```bash
python life_table_calculator.py --output life_table_all_subgroups.csv
```

> **Warning**: With 13 factors and 89 total levels, the full enumeration produces ~11.9 billion combinations × 2 sexes × 120 ages = an extremely large file. Run enumeration on a filtered subset by modifying `FACTOR_ORDER` in the script to include only the dimensions you need.

---

## Project structure

```
lifespan-calculator/
├── app.py                    # Streamlit dashboard (main entry point)
├── life_table_calculator.py  # Actuarial engine, risk factor definitions, CLI
├── pages/
│   └── 1_Methodology.py     # Full methodology and source citations page
├── requirements.txt
└── README.md
```

---

## Deployment

Deploy for free on [Streamlit Community Cloud](https://share.streamlit.io):

1. Push this repo to GitHub
2. Go to share.streamlit.io and connect your repo
3. Set **Main file path** to `app.py`
4. Deploy — no configuration needed

---

## Key references

**Baseline data**
- Social Security Administration OACT. Period Life Table, 2022 (2025 Trustees Report). [ssa.gov/oact/STATS/table4c6.html](https://www.ssa.gov/oact/STATS/table4c6.html)

**Income & SES**
- Chetty R, et al. "The Association Between Income and Life Expectancy in the United States, 2001–2014." *JAMA* 2016;315(16):1750–1766.
- Meara ER, Richards S, Cutler DM. "The Gap Gets Bigger: Changes in Mortality and Life Expectancy, by Education, 1981–2000." *Health Affairs* 2008;27(2):350–360.

**Behavioral factors**
- Jha P, et al. "21st-Century Hazards of Smoking and Benefits of Cessation in the United States." *NEJM* 2013;368:341–350.
- Global BMI Mortality Collaboration. "Body-mass index and all-cause mortality." *Lancet* 2016;388(10046):776–786.
- Arem H, et al. "Leisure Time Physical Activity and Mortality." *JAMA Intern Med* 2015;175(6):959–967.
- Ronksley PE, et al. "Association of alcohol consumption with selected cardiovascular disease outcomes." *BMJ* 2011;342:d671.
- Liu TZ, et al. "Sleep duration and risk of all-cause mortality." *Sleep Med Rev* 2017;32:28–36.
- GBD 2019 Diet Collaborators. "Health effects of dietary risks in 195 countries." *Lancet* 2019;393(10184):1958–1972.

**Social & psychosocial**
- Holt-Lunstad J, Smith TB, Layton JB. "Social Relationships and Mortality Risk: A Meta-analytic Review." *PLOS Med* 2010;7(7):e1000316.
- Walker ER, McGee RE, Druss BG. "Mortality in mental disorders and global disease burden implications." *JAMA Psychiatry* 2015;72(4):334–341.

**Race / ethnicity**
- Arias E, et al. "Provisional Life Expectancy Estimates for 2021." NCHS Vital Statistics Rapid Release 2022.
- Palaniappan LP, et al. "Call to Action: Cardiovascular Disease in Asian Americans." *Circulation* 2010;122(12):1242–1252.

**Geography & occupation**
- Cosby AG, et al. "Mortality and the Rural-Urban Continuum." *JAMA* 2019.
- Roelfs DJ, et al. "Losing life and livelihood: A systematic review and meta-analysis of unemployment and all-cause mortality." *Am J Epidemiology* 2011.

---

## License

MIT
