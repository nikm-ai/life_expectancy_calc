"""
SSA Period Life Table - Subpopulation Recalculator
Applies relative risk multipliers to baseline q(x) values and outputs a life table CSV.
See pages/methodology.py for full source citations.
"""

import csv, sys, argparse

SSA_2022 = {
    0: (0.006064, 0.005119), 1: (0.000491, 0.000398), 2: (0.000309, 0.000240),
    3: (0.000248, 0.000198), 4: (0.000199, 0.000160), 5: (0.000167, 0.000134),
    6: (0.000143, 0.000118), 7: (0.000126, 0.000109), 8: (0.000121, 0.000106),
    9: (0.000121, 0.000106), 10: (0.000127, 0.000111), 11: (0.000143, 0.000121),
    12: (0.000171, 0.000140), 13: (0.000227, 0.000162), 14: (0.000320, 0.000188),
    15: (0.000451, 0.000224), 16: (0.000622, 0.000276), 17: (0.000826, 0.000337),
    18: (0.001026, 0.000395), 19: (0.001182, 0.000450), 20: (0.001301, 0.000496),
    21: (0.001404, 0.000532), 22: (0.001498, 0.000567), 23: (0.001586, 0.000610),
    24: (0.001679, 0.000650), 25: (0.001776, 0.000699), 26: (0.001881, 0.000743),
    27: (0.001985, 0.000796), 28: (0.002095, 0.000855), 29: (0.002219, 0.000924),
    30: (0.002332, 0.000988), 31: (0.002445, 0.001053), 32: (0.002562, 0.001123),
    33: (0.002653, 0.001198), 34: (0.002716, 0.001263), 35: (0.002791, 0.001324),
    36: (0.002894, 0.001403), 37: (0.002994, 0.001493), 38: (0.003091, 0.001596),
    39: (0.003217, 0.001700), 40: (0.003353, 0.001803), 41: (0.003499, 0.001905),
    42: (0.003642, 0.002009), 43: (0.003811, 0.002116), 44: (0.003996, 0.002223),
    45: (0.004175, 0.002352), 46: (0.004388, 0.002516), 47: (0.004666, 0.002712),
    48: (0.004973, 0.002936), 49: (0.005305, 0.003177), 50: (0.005666, 0.003407),
    51: (0.006069, 0.003642), 52: (0.006539, 0.003917), 53: (0.007073, 0.004238),
    54: (0.007675, 0.004619), 55: (0.008348, 0.005040), 56: (0.009051, 0.005493),
    57: (0.009822, 0.005987), 58: (0.010669, 0.006509), 59: (0.011548, 0.007067),
    60: (0.012458, 0.007658), 61: (0.013403, 0.008305), 62: (0.014450, 0.008991),
    63: (0.015571, 0.009681), 64: (0.016737, 0.010343), 65: (0.017897, 0.011018),
    66: (0.019017, 0.011743), 67: (0.020213, 0.012532), 68: (0.021569, 0.013512),
    69: (0.023088, 0.014684), 70: (0.024828, 0.016025), 71: (0.026705, 0.017468),
    72: (0.028761, 0.019195), 73: (0.031116, 0.021195), 74: (0.033861, 0.023452),
    75: (0.037088, 0.025980), 76: (0.041126, 0.029153), 77: (0.045241, 0.032394),
    78: (0.049793, 0.035888), 79: (0.054768, 0.039676), 80: (0.060660, 0.044156),
    81: (0.067027, 0.049087), 82: (0.073999, 0.054635), 83: (0.081737, 0.061066),
    84: (0.090458, 0.068431), 85: (0.100525, 0.076841), 86: (0.111793, 0.086205),
    87: (0.124494, 0.096851), 88: (0.138398, 0.109019), 89: (0.153207, 0.121867),
    90: (0.169704, 0.135805), 91: (0.187963, 0.151108), 92: (0.208395, 0.168020),
    93: (0.230808, 0.186340), 94: (0.253914, 0.206432), 95: (0.277402, 0.228086),
    96: (0.300882, 0.250406), 97: (0.324326, 0.273699), 98: (0.347332, 0.296984),
    99: (0.369430, 0.319502), 100: (0.391927, 0.342716), 101: (0.414726, 0.366532),
    102: (0.437722, 0.390844), 103: (0.460800, 0.415531), 104: (0.483840, 0.440463),
    105: (0.508032, 0.466891), 106: (0.533434, 0.494904), 107: (0.560105, 0.524599),
    108: (0.588111, 0.556075), 109: (0.617516, 0.589439), 110: (0.648392, 0.624805),
    111: (0.680812, 0.662294), 112: (0.714852, 0.702031), 113: (0.750595, 0.744153),
    114: (0.788125, 0.788125), 115: (0.827531, 0.827531), 116: (0.868907, 0.868907),
    117: (0.912353, 0.912353), 118: (0.957970, 0.957970), 119: (1.000000, 1.000000),
}

RISK_FACTORS = {
    "smoking": {
        "label": "Smoking Status", "reference": "never",
        "options": {
            "never":         {"hr": 1.00, "desc": "Never smoker (reference)"},
            "former_light":  {"hr": 1.14, "desc": "Former smoker, quit >10 yrs ago or <10 pack-years — Jha et al. NEJM 2013"},
            "former_heavy":  {"hr": 1.55, "desc": "Former smoker, quit <10 yrs ago or >20 pack-years — Jha et al. NEJM 2013"},
            "current_light": {"hr": 2.00, "desc": "Current light smoker (<10 cigarettes/day) — MMWR 2014"},
            "current_heavy": {"hr": 3.20, "desc": "Current heavy smoker (≥1 pack/day) — MMWR 2014; Doll et al. BMJ 2004"},
            "vaping":        {"hr": 1.35, "desc": "E-cigarette/vaping only — Bhatta & Glantz AJPM 2020"},
        }
    },
    "bmi": {
        "label": "BMI Category", "reference": "normal",
        "options": {
            "underweight": {"hr": 1.51, "desc": "Underweight (<18.5) — Global BMI Mortality Collaboration, Lancet 2016"},
            "normal":      {"hr": 1.00, "desc": "Normal (18.5–24.9) — reference"},
            "overweight":  {"hr": 1.07, "desc": "Overweight (25–29.9) — Lancet 2016"},
            "obese1":      {"hr": 1.20, "desc": "Obese Class I (30–34.9) — Lancet 2016"},
            "obese2":      {"hr": 1.45, "desc": "Obese Class II (35–39.9) — Lancet 2016"},
            "obese3":      {"hr": 1.88, "desc": "Obese Class III (40+) — Lancet 2016"},
        }
    },
    "alcohol": {
        "label": "Alcohol Consumption", "reference": "moderate",
        "options": {
            "none":     {"hr": 1.05, "desc": "Non-drinker — slight excess vs. moderate (J-curve); Ronksley et al. BMJ 2011"},
            "moderate": {"hr": 1.00, "desc": "Moderate (≤14 drinks/week) — reference; GBD 2020"},
            "heavy":    {"hr": 1.40, "desc": "Heavy (15–28 drinks/week) — GBD 2020; Ronksley et al. BMJ 2011"},
            "severe":   {"hr": 2.70, "desc": "Severe / AUD (>28 drinks/week) — GBD 2020; Rehm et al. Lancet 2017"},
        }
    },
    "activity": {
        "label": "Physical Activity", "reference": "active",
        "options": {
            "sedentary":     {"hr": 1.35, "desc": "Sedentary (<30 min/week) — Arem et al. JAMA Intern Med 2015"},
            "insufficient":  {"hr": 1.15, "desc": "Insufficient (30–150 min/week) — Arem et al. 2015"},
            "active":        {"hr": 1.00, "desc": "Active (150–300 min/week, WHO guidelines) — reference"},
            "highly_active": {"hr": 0.80, "desc": "Highly active (>300 min/week) — Arem et al. JAMA Intern Med 2015"},
        }
    },
    "sleep": {
        "label": "Sleep Duration", "reference": "normal",
        "options": {
            "short":  {"hr": 1.13, "desc": "Short sleeper (<6 hrs/night) — Liu et al. Sleep 2017 meta-analysis (2M+ subjects)"},
            "normal": {"hr": 1.00, "desc": "Normal (7–8 hrs/night) — reference"},
            "long":   {"hr": 1.30, "desc": "Long sleeper (>9 hrs/night) — Liu et al. Sleep 2017"},
        }
    },
    "diet": {
        "label": "Diet Quality", "reference": "average",
        "options": {
            "poor":    {"hr": 1.22, "desc": "Poor diet quality — GBD Diet Collaborators, Lancet 2019"},
            "average": {"hr": 1.00, "desc": "Average diet quality — reference"},
            "good":    {"hr": 0.85, "desc": "High quality diet (Mediterranean-style) — Sofi et al. BMJ 2008; GBD 2019"},
        }
    },
    "income": {
        "label": "Household Income", "reference": "d5",
        "options": {
            "d1":  {"hr": 2.10, "desc": "Bottom 10% (~<$15,000/yr) — Chetty et al. JAMA 2016"},
            "d2":  {"hr": 1.75, "desc": "2nd decile (~$15,000–$25,000/yr)"},
            "d3":  {"hr": 1.45, "desc": "3rd decile (~$25,000–$35,000/yr)"},
            "d4":  {"hr": 1.20, "desc": "4th decile (~$35,000–$47,000/yr)"},
            "d5":  {"hr": 1.00, "desc": "5th decile — reference (~$47,000–$60,000/yr)"},
            "d6":  {"hr": 0.88, "desc": "6th decile (~$60,000–$75,000/yr)"},
            "d7":  {"hr": 0.80, "desc": "7th decile (~$75,000–$95,000/yr)"},
            "d8":  {"hr": 0.74, "desc": "8th decile (~$95,000–$130,000/yr)"},
            "d9":  {"hr": 0.69, "desc": "9th decile (~$130,000–$200,000/yr)"},
            "d10": {"hr": 0.62, "desc": "Top 10% (~>$200,000/yr) — Chetty et al. JAMA 2016"},
        }
    },
    "education": {
        "label": "Education Level", "reference": "bachelors",
        "options": {
            "less_than_hs": {"hr": 1.45, "desc": "Less than high school — Meara et al. Health Affairs 2008"},
            "hs_diploma":   {"hr": 1.20, "desc": "High school diploma / GED — Meara et al. 2008"},
            "some_college": {"hr": 1.08, "desc": "Some college, no degree — Meara et al. 2008"},
            "bachelors":    {"hr": 1.00, "desc": "Bachelor's degree — reference"},
            "graduate":     {"hr": 0.88, "desc": "Graduate / professional degree — Meara et al. 2008; NCHS 2012"},
        }
    },
    "social": {
        "label": "Social Connection", "reference": "partnered",
        "options": {
            "isolated":      {"hr": 1.45, "desc": "Socially isolated — Holt-Lunstad et al. PLOS Med 2010"},
            "widowed":       {"hr": 1.20, "desc": "Widowed — Holt-Lunstad et al. 2010"},
            "divorced":      {"hr": 1.25, "desc": "Divorced / separated — Holt-Lunstad et al. 2010"},
            "never_married": {"hr": 1.10, "desc": "Never married — Holt-Lunstad et al. 2010"},
            "partnered":     {"hr": 1.00, "desc": "Married / long-term partnered — reference"},
            "strong_social": {"hr": 0.85, "desc": "Partnered + strong social network — Holt-Lunstad et al. 2010"},
        }
    },
    "race": {
        "label": "Race / Ethnicity", "reference": "white_nh",
        "options": {
            "white_nh":         {"hr": 1.00, "desc": "Non-Hispanic White (reference) — NCHS Arias et al. 2021"},
            "mena":             {"hr": 0.90, "desc": "Middle Eastern / North African — Dallo et al. Ethn Dis 2008"},
            "black_usborn":     {"hr": 1.22, "desc": "Non-Hispanic Black, US-born — NCHS Arias 2021"},
            "black_african":    {"hr": 0.90, "desc": "African immigrant (Sub-Saharan) — Singh & Siahpush AJPH 2002"},
            "black_caribbean":  {"hr": 1.05, "desc": "Caribbean Black — Read et al. Soc Sci Med 2005"},
            "hispanic_mexican": {"hr": 0.80, "desc": "Mexican-American — Markides & Coreil 1986; NCHS"},
            "hispanic_pr":      {"hr": 0.97, "desc": "Puerto Rican — Borrell 2006; NCHS"},
            "hispanic_cuban":   {"hr": 0.87, "desc": "Cuban-American — Abraído-Lanza et al. AJPH 1999"},
            "hispanic_other":   {"hr": 0.83, "desc": "Central / South American — NCHS Other Hispanic"},
            "east_asian":       {"hr": 0.60, "desc": "East Asian (Chinese, Japanese, Korean) — NCHS Arias 2021 disaggregated"},
            "southeast_asian":  {"hr": 0.72, "desc": "Southeast Asian (Vietnamese, Cambodian, Thai) — NCHS"},
            "filipino":         {"hr": 0.78, "desc": "Filipino — elevated CVD/diabetes; Araneta & Barrett-Connor 2005"},
            "south_asian":      {"hr": 0.72, "desc": "South Asian — elevated CVD; Palaniappan et al. Circulation 2010"},
            "american_indian":  {"hr": 1.35, "desc": "American Indian (continental) — NCHS Arias 2021; IHS data"},
            "alaska_native":    {"hr": 1.45, "desc": "Alaska Native — IHS / Alaska DHSS data"},
            "native_hawaiian":  {"hr": 1.10, "desc": "Native Hawaiian — Hawaii DHHL cohort data"},
            "pacific_islander": {"hr": 0.88, "desc": "Other Pacific Islander — NCHS NHOPI residual"},
        }
    },
    "conditions": {
        "label": "Chronic Conditions", "reference": "none",
        "options": {
            "none":               {"hr": 1.00, "desc": "No chronic conditions (reference)"},
            "hypertension_ctrl":  {"hr": 1.05, "desc": "Hypertension, controlled — Ettehad et al. Lancet 2016"},
            "hypertension_unctrl":{"hr": 1.42, "desc": "Hypertension, uncontrolled — Ettehad et al. Lancet 2016"},
            "diabetes_t1":        {"hr": 2.60, "desc": "Type 1 diabetes — Livingstone et al. JAMA 2015"},
            "diabetes_t2":        {"hr": 1.65, "desc": "Type 2 diabetes — Emerging Risk Factors Collaboration, JAMA 2011"},
            "heart_disease":      {"hr": 1.90, "desc": "Coronary heart disease — AHA Statistics 2023"},
            "afib":               {"hr": 1.70, "desc": "Atrial fibrillation — Benjamin et al. Circulation 2019"},
            "ckd":                {"hr": 1.90, "desc": "Chronic kidney disease — Go et al. NEJM 2004"},
            "copd":               {"hr": 2.20, "desc": "COPD — GBD Collaborators, Lancet 2017"},
            "cancer_history":     {"hr": 1.85, "desc": "Cancer history (any) — SEER / ACS 2023"},
            "liver_disease":      {"hr": 2.90, "desc": "Chronic liver disease / cirrhosis — GBD Cirrhosis Collaborators 2020"},
            "depression":         {"hr": 1.52, "desc": "Major depressive disorder — Walker et al. JAMA Psychiatry 2015"},
            "serious_mental":     {"hr": 2.50, "desc": "Serious mental illness (schizophrenia/bipolar I) — Walker et al. 2015"},
            "hiv_treated":        {"hr": 1.65, "desc": "HIV on modern ART — ART Cohort Collaboration, Lancet 2017"},
            "multi":              {"hr": 3.20, "desc": "Multiple major conditions (2+)"},
        }
    },
    "geography": {
        "label": "Geography", "reference": "urban_metro",
        "options": {
            "urban_metro":  {"hr": 1.00, "desc": "Urban / large metropolitan — reference; NCHS Urban-Rural 2023"},
            "suburban":     {"hr": 1.02, "desc": "Suburban / medium metro — NCHS 2023"},
            "small_city":   {"hr": 1.06, "desc": "Small city / micropolitan — NCHS 2023"},
            "rural":        {"hr": 1.23, "desc": "Rural (non-core county) — Cosby et al. JAMA 2019"},
            "appalachia":   {"hr": 1.38, "desc": "Appalachian region (distressed counties) — Hendryx & Ahern AJPH 2014"},
            "ms_delta":     {"hr": 1.45, "desc": "Mississippi Delta — CDC Atlas of Heart Disease"},
        }
    },
    "occupation": {
        "label": "Occupation", "reference": "white_collar",
        "options": {
            "blue_collar":  {"hr": 1.22, "desc": "Blue collar / manual labor — NIOSH occupational data"},
            "service":      {"hr": 1.12, "desc": "Service / food / retail — CDC NHIS occupational mortality"},
            "white_collar": {"hr": 1.00, "desc": "White collar / professional — reference"},
            "healthcare":   {"hr": 0.85, "desc": "Healthcare worker — Schwartz et al. APHA 2018"},
            "unemployed":   {"hr": 1.50, "desc": "Unemployed / not in labor force — Roelfs et al. Am J Epidemiology 2011"},
        }
    },
}


def combined_hr(selections: dict) -> float:
    hr = 1.0
    for factor, choice in selections.items():
        hr *= RISK_FACTORS[factor]["options"][choice]["hr"]
    return hr


def apply_hr_to_qx(q: float, hr: float) -> float:
    import math
    if q <= 0: return 0.0
    if q >= 1: return 1.0
    logit_q   = math.log(q / (1 - q))
    logit_adj = logit_q + math.log(hr)
    q_adj     = 1 / (1 + math.exp(-logit_adj))
    return min(q_adj, 0.9999)


def build_life_table(qx_series: list) -> list:
    radix = 100_000
    rows  = []
    lx    = radix
    for age, qx in enumerate(qx_series):
        dx     = lx * qx
        lx_next = lx - dx
        Lx = (lx + lx_next) / 2 if age < len(qx_series) - 1 else (lx / qx if qx > 0 else 0)
        rows.append({"age": age, "qx": qx, "lx": lx, "dx": dx, "Lx": Lx, "Tx": 0.0, "ex": 0.0})
        lx = lx_next
    Tx = 0.0
    for row in reversed(rows):
        Tx += row["Lx"]
        row["Tx"] = Tx
    for row in rows:
        row["ex"] = row["Tx"] / row["lx"] if row["lx"] > 0 else 0.0
    return rows


def load_baseline(path: str, sex: str) -> dict:
    result = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            age = int(row["age"])
            if "q_male" in row and "q_female" in row:
                result[age] = (float(row["q_male"]), float(row["q_female"]))
            elif "qx" in row:
                result[age] = (float(row["qx"]), float(row["qx"]))
    return result


FACTOR_ORDER = ["smoking","bmi","alcohol","activity","sleep","diet",
                "income","education","social","race","conditions","geography","occupation"]

HEADER = (["age",
    "qx_baseline","lx_baseline","dx_baseline","Lx_baseline","Tx_baseline","ex_baseline",
    "qx_adjusted","lx_adjusted","dx_adjusted","Lx_adjusted","Tx_adjusted","ex_adjusted",
    "combined_hr","sex"] + FACTOR_ORDER)


def compute_subgroup(baseline, sex_idx, selections):
    ages    = sorted(baseline.keys())
    qx_base = [baseline[a][sex_idx] for a in ages]
    hr      = combined_hr(selections)
    qx_adj  = [apply_hr_to_qx(q, hr) for q in qx_base]
    return build_life_table(qx_base), build_life_table(qx_adj), hr


def write_rows(writer, table_base, table_adj, hr, sex, selections):
    for b, a in zip(table_base, table_adj):
        writer.writerow([
            b["age"],
            round(b["qx"],8), round(b["lx"],2), round(b["dx"],2),
            round(b["Lx"],2), round(b["Tx"],2), round(b["ex"],4),
            round(a["qx"],8), round(a["lx"],2), round(a["dx"],2),
            round(a["Lx"],2), round(a["Tx"],2), round(a["ex"],4),
            round(hr,4), sex,
        ] + [selections[f] for f in FACTOR_ORDER])


def run_all(args, baseline):
    import itertools
    factor_levels = [list(RISK_FACTORS[f]["options"].keys()) for f in FACTOR_ORDER]
    sexes      = ["male", "female"]
    all_combos = list(itertools.product(*factor_levels))
    total      = len(all_combos) * len(sexes)
    print(f"Generating {total:,} subgroups ({len(all_combos):,} combos × 2 sexes) …")
    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        for sex in sexes:
            sex_idx = 0 if sex == "male" else 1
            for combo in all_combos:
                selections = dict(zip(FACTOR_ORDER, combo))
                tb, ta, hr = compute_subgroup(baseline, sex_idx, selections)
                write_rows(writer, tb, ta, hr, sex, selections)
    print(f"Done. Output: {args.output}  ({total * 120:,} rows + header)")


def run_single(args, baseline):
    sex_idx    = 0 if args.sex == "male" else 1
    selections = {f: getattr(args, f) for f in FACTOR_ORDER}
    tb, ta, hr = compute_subgroup(baseline, sex_idx, selections)
    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        write_rows(writer, tb, ta, hr, args.sex, selections)
    e0b = tb[0]["ex"]; e0a = ta[0]["ex"]
    print(f"Done. Output: {args.output}")
    print(f"Combined HR: {hr:.4f}")
    print(f"Life expectancy at birth — Baseline: {e0b:.2f} | Adjusted: {e0a:.2f} (Δ {e0a-e0b:+.2f})")


def main():
    p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--baseline",      choices=["ssa2022","custom"], default="ssa2022")
    p.add_argument("--baseline-file", default=None)
    p.add_argument("--output",        default="life_table_all_subgroups.csv")
    p.add_argument("--single",        action="store_true")
    p.add_argument("--sex",           choices=["male","female"], default="male")
    for f in FACTOR_ORDER:
        p.add_argument(f"--{f}", choices=list(RISK_FACTORS[f]["options"].keys()),
                       default=RISK_FACTORS[f]["reference"])
    p.add_argument("--help-factors", action="store_true")
    args = p.parse_args()
    if args.help_factors:
        for f, meta in RISK_FACTORS.items():
            print(f"\n{meta['label']} (--{f})")
            for k, info in meta["options"].items():
                print(f"  {k:22s}  HR={info['hr']:.2f}  {info['desc']}")
        sys.exit(0)
    if args.baseline == "custom" and not args.baseline_file:
        p.error("--baseline-file required when --baseline=custom")
    baseline = SSA_2022 if args.baseline == "ssa2022" else load_baseline(args.baseline_file, "")
    run_single(args, baseline) if args.single else run_all(args, baseline)


if __name__ == "__main__":
    main()
