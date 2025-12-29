import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Polymerize Platform ROI Dashboard", layout="wide")
st.title("🚀 Polymerize Platform ROI Dashboard")

# --- TRANSLATION & CURRENCY DICTIONARY ---
lang_map = {
    "USD ($)": {
        "symbol": "$", "rate": 1.0,
        "summary": "Executive Summary: With Polymerize, your {fte}-person R&D team typically saves ~{hrs:,.0f} hours annually, equivalent to {sym}{savings:,.0f} in recovered productivity. At an annual investment of {sym}{cost:,.0f}, the ROI is {roi:.0f}% with a payback of {pb:.1f} months.",
        "headers": {"settings": "📋 Settings", "invest": "💰 Platform Investment", "labor": "Labor & Personnel", "lab_data": "Lab & Data", "rd_act": "R&D Activity", "scale": "Scale & Legacy"},
        "inputs": {
            "p_annual": "Annual Platform License Cost", "p_impl": "One-time Implementation Cost", "fte": "Total R&D Employees (FTE)", 
            "f_dev": "Formulation Developers (FTE)", "hr_c": "Avg. Hourly Cost", "lab_c": "Avg. Lab Cost / Work Order", 
            "lab_o": "Total Work Orders / Year", "new_f": "New Formulations / Year", "adj_f": "Formulation Adjustments / Year",
            "t_new": "Avg. Time to Develop New Material (Hrs)", "t_adj": "Avg. Time to Adjust Material (Hrs)", "sem": "SEM Images Analyzed / Year",
            "mat": "Annual Raw Material Spend", "leg": "Current Annual ELN + DoE Cost"
        },
        "metrics": {"savings": "Annual Savings (Mid)", "profit": "Net Profit (Year 1)", "roi": "ROI (%)", "payback": "Payback Period (Months)"},
        "table": {"driver": "Value Driver", "method": "Calculation Methodology", "bar_t": "Annual Benefits vs. Costs", "donut_t": "Savings Composition", "tab_t": "Detailed Savings Calculation Table"},
        "drivers": {
            "collab": "Improved Collaboration", "double": "Prevented Double-Work", "analytics": "Enhanced Data Analytics", "sem_ai": "AI Image Analysis (SEM)", 
            "data_ai": "AI Data Extraction (TDS)", "mat_dev": "AI Material Development", "form_adj": "AI Formulation Adjustment", 
            "legacy": "Legacy Tool Replacement", "lab_red": "Reduced Lab Expenses", "mat_opt": "Material Optimization"
        },
        "methods": {"prod": "{h} hrs × {s}{c:,.0f}/hr", "leg": "Direct offset of {s}{v:,.0f} systems", "lab": "10/20/30% reduction of {s}{v:,.0f} spend", "mat": "0.01/0.1/0.5% optimization of {s}{v:,.0f} spend"}
    },
    "EUR (€)": {
        "symbol": "€", "rate": 0.92,
        "summary": "Executive Summary: Mit Polymerize spart Ihr {fte}-köpfiges Team ca. {hrs:,.0f} Stunden jährlich, was {sym}{savings:,.0f} entspricht. ROI: {roi:.0f}%, Amortisation: {pb:.1f} Monate.",
        "headers": {"settings": "📋 Einstellungen", "invest": "💰 Investition", "labor": "Personal", "lab_data": "Labor & Daten", "rd_act": "F&E-Aktivität", "scale": "Skalierung & Legacy"},
        "inputs": {
            "p_annual": "Jährliche Lizenzgebühr", "p_impl": "Einmalige Implementierungskosten", "fte": "F&E Mitarbeiter (FTE)", 
            "f_dev": "Formulierungs-Entwickler (FTE)", "hr_c": "Durchschnittlicher Stundensatz", "lab_c": "Laborkosten pro Auftrag", 
            "lab_o": "Laboraufträge pro Jahr", "new_f": "Neue Formulierungen / Jahr", "adj_f": "Anpassungen / Jahr",
            "t_new": "Zeitaufwand neue Materialien (Std)", "t_adj": "Zeitaufwand Anpassungen (Std)", "sem": "SEM-Bilder pro Jahr",
            "mat": "Jährliche Materialausgaben", "leg": "Aktuelle ELN + DoE Kosten"
        },
        "metrics": {"savings": "Ersparnis (Mittel)", "profit": "Nettogewinn (Jahr 1)", "roi": "ROI (%)", "payback": "Amortisation (Monate)"},
        "table": {"driver": "Werttreiber", "method": "Berechnungsmethodik", "bar_t": "Nutzen vs. Kosten", "donut_t": "Zusammensetzung", "tab_t": "Detaillierte Berechnungstabelle"},
        "drivers": {
            "collab": "Verbesserte Zusammenarbeit", "double": "Vermeidung von Doppelarbeit", "analytics": "Erweiterte Datenanalyse", "sem_ai": "KI-Bildanalyse (SEM)", 
            "data_ai": "KI-Datenextraktion (TDS)", "mat_dev": "KI-Materialentwicklung", "form_adj": "KI-Formulierungsanpassung", 
            "legacy": "Ersatz von Altsystemen", "lab_red": "Reduzierte Laborkosten", "mat_opt": "Materialoptimierung"
        },
        "methods": {"prod": "{h} Std × {s}{c:,.0f}/Std", "leg": "Direkter Versatz von {s}{v:,.0f} Systemen", "lab": "10/20/30% Senkung der {s}{v:,.0f} Ausgaben", "mat": "0,01/0,1/0,5% Optimierung der {s}{v:,.0f} Ausgaben"}
    },
    "KRW (₩)": {
        "symbol": "₩", "rate": 1320.0,
        "summary": "Executive Summary: Polymerize를 통해 {fte}명의 R&D 팀은 연간 약 {hrs:,.0f}시간을 절약하며, 이는 {sym}{savings:,.0f} 이상의 가치가 있습니다. ROI: {roi:.0f}%, 회수 기간: {pb:.1f}개월.",
        "headers": {"settings": "📋 설정", "invest": "💰 플랫폼 투자", "labor": "인력 및 비용", "lab_data": "실험 및 데이터", "rd_act": "R&D 활동량", "scale": "규모 및 레거시"},
        "inputs": {
            "p_annual": "연간 라이선스 비용", "p_impl": "일회성 구축 비용", "fte": "총 R&D 인원 (FTE)", 
            "f_dev": "배합 개발자 인원 (FTE)", "hr_c": "평균 시간당 비용", "lab_c": "실험당 평균 비용", 
            "lab_o": "연간 총 실험 횟수", "new_f": "연간 신규 배합 개발 수", "adj_f": "연간 배합 조정 수",
            "t_new": "신규 소재 개발 시간 (시간)", "t_adj": "소재 조정 시간 (시간)", "sem": "연간 SEM 이미지 분석 수",
            "mat": "연간 원자재 구매액", "leg": "기존 ELN + DoE 비용"
        },
        "metrics": {"savings": "연간 절감액 (중간)", "profit": "순이익 (1년차)", "roi": "ROI (%)", "payback": "회수 기간 (개월)"},
        "table": {"driver": "가치 동인", "method": "계산 방법론", "bar_t": "편익 vs 비용", "donut_t": "절감액 구성", "tab_t": "상세 계산표"},
        "drivers": {
            "collab": "협업 효율성 향상", "double": "중복 작업 방지", "analytics": "데이터 분석 강화", "sem_ai": "AI 이미지 분석 (SEM)", 
            "data_ai": "AI 데이터 추출 (TDS)", "mat_dev": "AI 소재 개발", "form_adj": "AI 배합 조정", 
            "legacy": "기존 시스템 대체", "lab_red": "실험 비용 절감", "mat_opt": "원자재 최적화"
        },
        "methods": {"prod": "{h} 시간 × {s}{c:,.0f}/시간", "leg": "{s}{v:,.0f} 시스템 직접 대체", "lab": "총 지출 {s}{v:,.0f}의 10/20/30% 절감", "mat": "총 지출 {s}{v:,.0f}의 0.01/0.1/0.5% 최적화"}
    },
    "JPY (¥)": {
        "symbol": "¥", "rate": 150.0,
        "summary": "Executive Summary: Polymerizeの導入により、{fte}名のR&Dチームは年間約{hrs:,.0f}時間を削減し、{sym}{savings:,.0f}相当の生産性向上を実現します。ROI: {roi:.0f}%, 回収期間: {pb:.1f}ヶ月.",
        "headers": {"settings": "📋 設定", "invest": "💰 投資額", "labor": "労務", "lab_data": "ラボ・データ", "rd_act": "R&D活動", "scale": "スケール・レガシー"},
        "inputs": {
            "p_annual": "年間ライセンス料", "p_impl": "導入費用（一時金）", "fte": "R&D従業員数 (FTE)", 
            "f_dev": "配合開発者数 (FTE)", "hr_c": "平均時給", "lab_c": "ラボ依頼あたりのコスト", 
            "lab_o": "年間のラボ依頼数", "new_f": "新規配合開発数 / 年", "adj_f": "配合調整数 / 年",
            "t_new": "新規材料開発時間 (時)", "t_adj": "材料調整時間 (時)", "sem": "SEM画像解析数 / 年",
            "mat": "原材料費合計 / 年", "leg": "現行システムのコスト / 年"
        },
        "metrics": {"savings": "年間節約額 (中間)", "profit": "純利益 (初年度)", "roi": "ROI (%)", "payback": "回収期間 (ヶ月)"},
        "table": {"driver": "価値ドライバー", "method": "計算方法", "bar_t": "便益 vs コスト", "donut_t": "節約額の内訳", "tab_t": "詳細計算表"},
        "drivers": {
            "collab": "コラボレーションの改善", "double": "重複作業の防止", "analytics": "データ分析の強化", "sem_ai": "AI画像解析 (SEM)", 
            "data_ai": "AIデータ抽出 (TDS)", "mat_dev": "AI材料開発", "form_adj": "AI配合調整", 
            "legacy": "レガシーシステムの置換", "lab_red": "ラボ経費の削減", "mat_opt": "原材料の最適化"
        },
        "methods": {"prod": "{h} 時間 × {s}{c:,.0f}/時", "leg": "{s}{v:,.0f} システムの直接削減", "lab": "年間支出 {s}{v:,.0f} の 10/20/30% 削減", "mat": "年間支出 {s}{v:,.0f} の 0.01/0.1/0.5% 最適化"}
    }
}

# --- SIDEBAR: ALL 12 USER INPUTS ---
with st.sidebar:
    selected_cur = st.selectbox("Currency / Language", list(lang_map.keys()))
    l = lang_map[selected_cur]
    c_sym, c_rate = l["symbol"], l["rate"]

    st.header(l["headers"]["settings"])
    st.subheader(l["headers"]["invest"])
    platform_annual_cost = st.number_input(l["inputs"]["p_annual"], value=50000.0) * c_rate
    impl_cost = st.number_input(l["inputs"]["p_impl"], value=10000.0) * c_rate
    
    st.subheader(l["headers"]["labor"])
    total_fte = st.number_input(l["inputs"]["fte"], value=10)
    form_devs = st.number_input(l["inputs"]["f_dev"], value=3)
    hr_cost = st.number_input(f"{l['inputs']['hr_c']} ({c_sym})", value=80.0) * c_rate
    
    st.subheader(l["headers"]["lab_data"])
    lab_cost_order = st.number_input(f"{l['inputs']['lab_c']} ({c_sym})", value=800.0) * c_rate
    annual_orders = st.number_input(l["inputs"]["lab_o"], value=250)
    sem_images = st.number_input(l["inputs"]["sem"], value=2000)

    st.subheader(l["headers"]["rd_act"])
    new_forms = st.number_input(l["inputs"]["new_f"], value=30)
    adj_forms = st.number_input(l["inputs"]["adj_f"], value=70)
    time_new = st.number_input(l["inputs"]["t_new"], value=60)
    time_adj = st.number_input(l["inputs"]["t_adj"], value=30)

    st.subheader(l["headers"]["scale"])
    mat_spend = st.number_input(f"{l['inputs']['mat']} ({c_sym})", value=100_000_000.0, step=1_000_000.0) * c_rate
    legacy_cost = st.number_input(f"{l['inputs']['leg']} ({c_sym})", value=4000.0) * c_rate

# --- CALCULATION ENGINE ---
productivity_hours = {
    "collab": {"min": 132, "mid": 264, "good": 440},
    "double": {"min": 220, "mid": 440, "good": 660},
    "analytics": {"min": 308, "mid": 528, "good": 880},
    "sem_ai": {"min": 167, "mid": 333, "good": 500},
    "data_ai": {"min": 50, "mid": 120, "good": 200},
    "mat_dev": {"min": 540, "mid": 810, "good": 1080},
    "form_adj": {"min": 630, "mid": 945, "good": 1260},
}

total_hrs_mid = sum(h["mid"] for h in productivity_hours.values())
rows = []
for key, hrs in productivity_hours.items():
    rows.append({
        l["table"]["driver"]: l["drivers"][key],
        "Min Case": hrs["min"] * hr_cost,
        "Mid Case": hrs["mid"] * hr_cost,
        "Good Case": hrs["good"] * hr_cost,
        l["table"]["method"]: l["methods"]["prod"].format(h=hrs['mid'], s=c_sym, c=hr_cost)
    })

# Add Direct Drivers
rows.append({l["table"]["driver"]: l["drivers"]["legacy"], "Min Case": legacy_cost, "Mid Case": legacy_cost, "Good Case": legacy_cost, l["table"]["method"]: l["methods"]["leg"].format(s=c_sym, v=legacy_cost)})
lab_spend = lab_cost_order * annual_orders
rows.append({l["table"]["driver"]: l["drivers"]["lab_red"], "Min Case": lab_spend*0.1, "Mid Case": lab_spend*0.2, "Good Case": lab_spend*0.3, l["table"]["method"]: l["methods"]["lab"].format(s=c_sym, v=lab_spend)})
rows.append({l["table"]["driver"]: l["drivers"]["mat_opt"], "Min Case": mat_spend*0.0001, "Mid Case": mat_spend*0.001, "Good Case": mat_spend*0.005, l["table"]["method"]: l["methods"]["mat"].format(s=c_sym, v=mat_spend)})

df = pd.DataFrame(rows)
total_savings = [df["Min Case"].sum(), df["Mid Case"].sum(), df["Good Case"].sum()]
total_costs = platform_annual_cost + impl_cost
mid_savings, net_profit = total_savings[1], total_savings[1] - total_costs
roi = (net_profit / total_costs) * 100 if total_costs > 0 else 0
pb = (total_costs / (mid_savings / 12)) if mid_savings > 0 else 0

# --- VIEW ---
# 1. Summary Box
st.info(l["summary"].format(fte=total_fte, hrs=total_hrs_mid, sym=c_sym, savings=mid_savings, cost=platform_annual_cost, roi=roi, pb=pb))

# 2. Key Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric(l["metrics"]["savings"], f"{c_sym}{mid_savings:,.0f}")
c2.metric(l["metrics"]["profit"], f"{c_sym}{net_profit:,.0f}")
c3.metric(l["metrics"]["roi"], f"{roi:.0f}%")
c4.metric(l["metrics"]["payback"], f"{pb:.1f}")

st.divider()

# 3. Interactive Charts
chart_col1, chart_col2 = st.columns([1, 1])
with chart_col1:
    st.subheader(f"{l['table']['bar_t']} ({c_sym})")
    fig_bar = go.Figure(data=[go.Bar(name='Savings', x=["Min", "Mid", "Good"], y=total_savings, marker_color='#00CC96')])
    fig_bar.add_trace(go.Bar(name='Investment', x=["Min", "Mid", "Good"], y=[total_costs]*3, marker_color='#EF553B'))
    fig_bar.update_layout(barmode='group', height=400)
    st.plotly_chart(fig_bar, use_container_width=True)
with chart_col2:
    st.subheader(l["table"]["donut_t"])
    st.plotly_chart(go.Figure(data=[go.Pie(labels=df[l["table"]["driver"]], values=df["Mid Case"], hole=.5)]), use_container_width=True)

# 4. Detailed Calculation Table
st.divider()
st.subheader(f"{l['table']['tab_t']} ({c_sym})")
st.table(df.style.format({"Min Case": f"{c_sym}"+"{:,.0f}", "Mid Case": f"{c_sym}"+"{:,.0f}", "Good Case": f"{c_sym}"+"{:,.0f}"}))