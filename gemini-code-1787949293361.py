import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="MaxMillions Risk Manager", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR DARK/GREEN THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #0A0E17; color: #FFFFFF; }
    .stMetric { background-color: #1A1F2B; padding: 15px; border-radius: 8px; border-left: 4px solid #00A859; }
    h1, h2, h3 { color: #00A859; }
    </style>
""", unsafe_allow_html=True)

st.title("📈 The MaxMillions Universal Calculator")
st.markdown("### *Rule: Protect the Drawdown. Follow the Math.*")

# --- USER INPUTS (SIDEBAR) ---
st.sidebar.header("⚙️ Trade Parameters")

phase = st.sidebar.radio("1. Trading Phase", ["Evaluation / Funded (10% Risk)", "Live Consolidation (2% Risk)"])
num_accounts = st.sidebar.number_input("2. Number of Accounts (Copier)", min_value=1, max_value=20, value=1, step=1)
current_buffer = st.sidebar.number_input("3. Current Drawdown Buffer ($ per account)", min_value=100, max_value=50000, value=500, step=50)

# --- MATHEMATICAL ENGINE ---
# Set Risk Percentage based on Phase
risk_pct = 0.10 if "10%" in phase else 0.02

# Calculate Base Risk & Contracts
risk_per_acct = current_buffer * risk_pct

if current_buffer < 2000:
    contracts_per_acct = 1
else:
    contracts_per_acct = int(current_buffer // 1000)

# MNQ Math ($2 per point, 4 ticks per point)
mnq_pt_value = 2.0
sl_points = risk_per_acct / (contracts_per_acct * mnq_pt_value)
sl_ticks = sl_points * 4

tp_points = sl_points * 2.5
tp_ticks = tp_points * 4
profit_per_acct = risk_per_acct * 2.5

# Copier Math (Total Portfolio)
total_risk = risk_per_acct * num_accounts
total_profit = profit_per_acct * num_accounts
total_contracts = contracts_per_acct * num_accounts

# --- UI DISPLAY: THE MASTER CHART SETTINGS ---
st.header("🎯 Chart Execution (Master Account)")
st.info("Enter these exact numbers into your Bracket Order.")

col1, col2, col3 = st.columns(3)
col1.metric("Contracts (MNQ)", f"{contracts_per_acct} Micro(s)", "Strict Volume Rule")
col2.metric("Stop Loss", f"{sl_points:.2f} Pts ({int(sl_ticks)} Ticks)", f"-$ {risk_per_acct:,.2f} Risk")
col3.metric("Take Profit (2.5 RR)", f"{tp_points:.2f} Pts ({int(tp_ticks)} Ticks)", f"+$ {profit_per_acct:,.2f} Reward")

st.divider()

# --- UI DISPLAY: PORTFOLIO EXPOSURE ---
st.header("🌐 Portfolio Exposure (Trade Copier)")
st.markdown(f"Metrics across **{num_accounts}** linked accounts.")

col4, col5, col6 = st.columns(3)
col4.metric("Total Contracts Fired", f"{total_contracts} Micros")
col5.metric("Total Portfolio Risk", f"-$ {total_risk:,.2f}", "Max Loss")
col6.metric("Total Portfolio Profit", f"+$ {total_profit:,.2f}", "Take Profit Hit")

st.divider()

# --- THE RULES ALERTS ---
if "10%" in phase:
    st.warning("⚡ **SPEED MODE ACTIVE:** You are risking 10%. Stop trading for the day if you hit 2 consecutive losses.")
else:
    st.success("🛡️ **PRESERVATION MODE ACTIVE:** You are risking 2%. You have a 50-trade survival armor built in.")

if current_buffer >= 10000:
    st.info("🏆 **PRO LEVEL UNLOCKED:** You have the math to trade 1 Mini (ES/NQ) instead of 10 Micros.")