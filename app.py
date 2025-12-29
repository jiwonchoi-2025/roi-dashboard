import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="Polymerize Platform ROI Dashboard", layout="wide")
st.title("🚀 Polymerize Platform ROI Dashboard")

# --- SIDEBAR: ALL 12+ USER INPUTS ---
with st.sidebar:
    st.header("📋 Baseline Settings")
    
    # 1. Platform Investment
    st.subheader("💰 Platform Investment")
    platform_annual_cost = st.number_input("Annual Platform License Cost", value=50000.0)
    impl_cost = st.number_input("One-time Implementation Cost", value=10000.0)
    
    # 2. Labor & Personnel
    st.subheader("👥 Labor & Personnel")
    total_fte = st.number_input("Total R&D Employees (FTE)", value=10)
    form_devs = st.number_input("Formulation Developers (FTE)", value=3)
    hr_cost = st.number_input("Avg. Hourly Cost ($)", value=80.0)
    
    # 3. Lab & Data
    st.subheader("🧪 Lab & Data")
    lab_cost_order = st.number_input("Avg. Lab Cost / Work Order ($)", value=800.0)
    annual_orders = st.number_input("Total Work Orders / Year", value=250)
    sem_images = st.number_input("SEM Images Analyzed / Year", value=2000)

    # 4. R&D Activity
    st.subheader("⚗️ R&D Activity")
    new_forms = st.number_input("New Formulations / Year", value=30)
    adj_forms = st.number_input("Formulation Adjustments / Year", value=70)
    time_new = st.number_input("Avg. Time to Develop New Material (Hrs)", value=60)
    time_adj = st.number_input("Avg. Time to Adjust Material (Hrs)", value=30)

    # 5. Scale & Legacy
    st.subheader("📈 Scale & Legacy")
    mat_spend = st.number_input("Annual Raw Material Spend ($)", value=100_000_000.0, step=1_000_000.0)
    legacy_cost = st.number_input("Current Annual ELN + DoE Cost ($)", value=4000.0)

    # 6. Usage Tracking (Metrics from Analytics Screenshot)
    st.divider()
    st.header("📊 Actual Platform Usage")
    curr_month = st.slider("Current Implementation Month", 1, 12, 6)
    act_wo = st.number_input("Work Orders Completed", value=208)
    act_exp = st.number_input("Total Experiments", value=7036)
    act_mods = st.number_input("Models Created", value=83)
    act_fwd = st.number_input("Forward Predictions Run", value=56)
    act_inv = st.number_input("Inverse Predictions Run", value=130)

# --- CALCULATION ENGINE ---
productivity_hours = {
    "Improved Collaboration":      264,
    "Prevented Double-Work":       440,
    "Enhanced Data Analytics":      528,
    "AI Image Analysis (SEM)":     333,
    "AI Data Extraction (TDS)":    120,
    "AI Material Development":     810,
    "AI Formulation Adjustment":    945,
}

total_hrs_mid = sum(productivity_hours.values())
rows = []
for driver, hrs in productivity_hours.items():
    rows.append({
        "Value Driver": driver,
        "Min Case": hrs * 0.6 * hr_cost,
        "Mid Case": hrs * hr_cost,
        "Good Case": hrs * 1.5 * hr_cost,
        "Calculation Methodology": f"{hrs} hrs × ${hr_cost:,.0f}/hr"
    })

# Direct Savings Calculations
rows.append({"Value Driver": "Legacy Tool Replacement", "Min Case": legacy_cost, "Mid Case": legacy_cost, "Good Case": legacy_cost, "Calculation Methodology": f"Direct offset of current systems"})
lab_total_ann = lab_cost_order * annual_orders
rows.append({"Value Driver": "Reduced Lab Expenses", "Min Case": lab_total_ann*0.1, "Mid Case": lab_total_ann*0.2, "Good Case": lab_total_ann*0.3, "Calculation Methodology": "10/20/30% reduction of lab spend"})
rows.append({"Value Driver": "Material Optimization", "Min Case": mat_spend*0.0001, "Mid Case": mat_spend*0.001, "Good Case": mat_spend*0.005, "Calculation Methodology": "Optimization of raw material spend"})

df = pd.DataFrame(rows)
total_ann_savings = [df["Min Case"].sum(), df["Mid Case"].sum(), df["Good Case"].sum()]
total_inv = platform_annual_cost + impl_cost
roi = ((total_ann_savings[1] - total_inv) / total_inv) * 100 if total_inv > 0 else 0
payback = (total_inv / (total_ann_savings[1] / 12)) if total_ann_savings[1] > 0 else 0

# --- VALUE REALIZATION LOGIC ---
months = np.arange(1, 13)
cum_min = np.cumsum([total_ann_savings[0] / 12] * 12)
cum_mid = np.cumsum([total_ann_savings[1] / 12] * 12)
cum_good = np.cumsum([total_ann_savings[2] / 12] * 12)

# Usage Intensity Logic
wo_intensity = min(act_wo / annual_orders, 1.0) if annual_orders > 0 else 0
pred_intensity = min((act_fwd + act_inv) / 300, 1.0) # Assume 300 preds as target for full efficiency
total_intensity = (wo_intensity * 0.5) + (pred_intensity * 0.5)
actual_realized = total_ann_savings[1] * total_intensity * (curr_month / 12)

# --- VIEW TABS ---
tab_proj, tab_real = st.tabs(["💰 ROI Projection", "📊 Monthly Value Realization"])

with tab_proj:
    # --- CLEANED EXECUTIVE SUMMARY BOX ---
    st.info(f"""
    **Executive Summary:** With Polymerize, your **{total_fte}-person R&D team** typically saves **~{total_hrs_mid:,.0f} hours annually**, 
    equivalent to **${total_ann_savings[1]:,.0f}** in recovered productivity and direct cost reductions. 
    At an annual investment of **${platform_annual_cost:,.0f}**, the platform delivers an **ROI of {roi:.0f}%** within the first year, 
    achieving full payback in just **{payback:.1f} months**.
    """)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Annual Savings (Mid)", f"${total_ann_savings[1]:,.0f}")
    m2.metric("Net Profit (Year 1)", f"${total_ann_savings[1] - total_inv:,.0f}")
    m3.metric("ROI (%)", f"{roi:.0f}%")
    m4.metric("Payback (Months)", f"{payback:.1f}")

    st.divider()
    chart_col1, chart_col2 = st.columns([1, 1])
    with chart_col1:
        st.subheader("Annual Benefits vs. Costs ($)")
        fig_bar = go.Figure(data=[
            go.Bar(name='Savings', x=["Min", "Mid", "Good"], y=total_ann_savings, marker_color='#00CC96'),
            go.Bar(name='Investment', x=["Min", "Mid", "Good"], y=[total_inv]*3, marker_color='#EF553B')
        ])
        fig_bar.update_layout(barmode='group', height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    with chart_col2:
        st.subheader("Savings Composition")
        st.plotly_chart(go.Figure(data=[go.Pie(labels=df["Value Driver"], values=df["Mid Case"], hole=.5)]), use_container_width=True)

    st.divider()
    st.subheader("Detailed Savings Calculation Table")
    st.table(df.style.format({"Min Case": "${:,.0f}", "Mid Case": "${:,.0f}", "Good Case": "${:,.0f}"}))

with tab_real:
    st.subheader("Monthly Value Realization Progress")
    
    # Value Realization KPIs
    k1, k2, k3 = st.columns(3)
    k1.metric("Current Month", f"Month {curr_month}")
    k2.metric("Target ROI Realization", f"{total_intensity*100:.1f}%")
    k3.metric("Realized Value (To Date)", f"${actual_realized:,.0f}")
    
    # Cumulative Growth Graph
    fig_prog = go.Figure()
    fig_prog.add_trace(go.Scatter(x=months, y=cum_good, name='Good Case Projection', line=dict(color='#00CC96', dash='dot')))
    fig_prog.add_trace(go.Scatter(x=months, y=cum_mid, name='Mid Case Projection', line=dict(color='#636EFA', dash='dot')))
    fig_prog.add_trace(go.Scatter(x=months, y=cum_min, name='Min Case Projection', line=dict(color='#FFA15A', dash='dot')))
    
    # Actual realized path based on usage logs
    actual_path = np.linspace(0, actual_realized, curr_month)
    fig_prog.add_trace(go.Scatter(x=months[:curr_month], y=actual_path, name='Actual Realized (Usage-Based)', line=dict(color='#2CA02C', width=5)))
    
    fig_prog.update_layout(height=500, yaxis_title="Cumulative Value ($)", xaxis_title="Implementation Month")
    st.plotly_chart(fig_prog, use_container_width=True)

    # Platform Usage Metrics Grid
    st.divider()
    st.subheader("Platform Usage Metrics")
    u1, u2, u3, u4, u5 = st.columns(5)
    u1.metric("Work Orders", f"{act_wo}", f"{(act_wo/annual_orders)*100:.1f}% Target")
    u2.metric("Experiments", f"{act_exp:,.0f}")
    u3.metric("Models Created", f"{act_mods}")
    u4.metric("Forward Predictions", f"{act_fwd}")
    u5.metric("Inverse Predictions", f"{act_inv}")

    # Written Commentary
    st.info(f"""
    **Value Realization Commentary:**
    * Your team has completed **{act_wo}** out of **{annual_orders}** target work orders.
    * Platform adoption is currently driving a **{total_intensity*100:.1f}% realization** of the Mid-Case ROI projections.
    * The **Actual Realized Value** of **${actual_realized:,.0f}** is based on the combination of digitized lab workflows, **{act_fwd} Forward Predictions**, and **{act_inv} Inverse Predictions**.
    """)
