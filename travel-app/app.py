import streamlit as st
import pandas as pd
import time
from datetime import date
import os

# --- 1. GLOBAL UI CONFIG ---
st.set_page_config(page_title="N-AME Travel", page_icon="🦅", layout="centered")
primary_teal = "#0CA38D"

def apply_custom_styles():
    st.markdown(f"""
        <style>
        .stButton>button {{ background-color: {primary_teal}; color: white; border-radius: 12px; height: 3.5em; border: none; font-weight: bold; width: 100%; }}
        .result-card {{ background-color: #f9f9f9; padding: 25px; border-radius: 20px; border-left: 8px solid {primary_teal}; margin-bottom: 20px; }}
        .logo-container {{ text-align: center; width: 100%; margin-top: 50px; }}
        .brand-icon {{ font-size: 100px !important; margin: 0; line-height: 1; }}
        .brand-title {{ color: {primary_teal}; font-size: 60px !important; font-weight: 900; letter-spacing: 10px; margin-top: -10px; text-transform: uppercase; }}
        </style>
        """, unsafe_allow_html=True)

# --- 2. DATA & LOGIC FUNCTIONS ---
@st.cache_data
def get_malaysia_data():
    paths = ['malaysia_travel.csv', 'travel-app/malaysia_travel.csv']
    for path in paths:
        if os.path.exists(path): return pd.read_csv(path)
    return None

def calculate_costs(row, adults, kids, days):
    """Preserves your 60% kids discount logic"""
    daily_acc = row['Accommodation_Daily']
    daily_food = (adults * row['Food_Daily']) + (kids * row['Food_Daily'] * 0.6)
    daily_trans = row['Transport_Daily']
    
    total_daily = daily_acc + daily_food + daily_trans
    grand_total = total_daily * days
    return grand_total, total_daily, daily_acc, daily_food

# --- 3. PAGE FUNCTIONS ---

def show_splash():
    st.markdown('<div class="logo-container" style="padding-top:100px;"><p class="brand-icon">🦅</p><p class="brand-title">N-AME</p></div>', unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.page = "search"
    st.rerun()

def show_search_page(df):
    st.markdown('<div class="logo-container"><p class="brand-icon">🦅</p><p class="brand-title">N-AME</p></div>', unsafe_allow_html=True)
    
    st.write("### ✈️ Plan Your Trip")
    selected_state = st.selectbox("📍 Select State", sorted(df['State'].unique()))
    selected_dates = st.date_input("Select Range", value=(date.today(), date.today()), min_value=date.today())
    
    c1, c2 = st.columns(2)
    with c1: adults = st.number_input("Adults", min_value=1, value=1)
    with c2: kids = st.number_input("Children", min_value=0, value=0)
    
    user_budget = st.number_input("💰 Total Budget ($)", min_value=10, value=1500)

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🔍 Search Now"):
            if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
                st.session_state.update({
                    "page": "discovery", "state": selected_state, "budget": user_budget,
                    "adults": adults, "kids": kids, "days": (selected_dates[1] - selected_dates[0]).days + 1
                })
                st.rerun()
            else: st.warning("Please select start and end dates.")
    
    with btn_col2:
        with st.popover("⚙️ Filters"):
            st.markdown(f"<h4 style='color: {primary_teal};'>Budget Allocation</h4>", unsafe_allow_html=True)
            # We keep the sliders but since they don't affect filtering yet, we just store them
            st.slider("🏠 Accommodation (%)", 0, 100, 40)
            st.slider("🍔 Food (%)", 0, 100, 20)
            st.write("Tip: Allocation helps fine-tune your results.")

def show_discovery_page(df):
    st.markdown(f"## 📍 Explore {st.session_state.state}")
    all_places = df[df['State'] == st.session_state.state]
    
    for _, row in all_places.iterrows():
        grand_total, _, _, _ = calculate_costs(row, st.session_state.adults, st.session_state.kids, st.session_state.days)
        
        if grand_total <= st.session_state.budget:
            with st.container(border=True):
                c1, c2 = st.columns([1, 2])
                with c1: st.image(row['Image_URL'], use_container_width=True)
                with c2:
                    st.subheader(row['City'])
                    st.write(f"⭐ {row['Rating']} | 📍 {row['Distance_Hub']}km from Hub")
                    st.write(f"**Est. Cost:** ${grand_total:,.2f}")
                    if st.button(f"Select {row['City']}", key=f"sel_{row['City']}"):
                        st.session_state.selected_city = row['City']
                        st.session_state.page = "results"
                        st.rerun()

    if st.button("⬅️ Back to Search"):
        st.session_state.page = "search"
        st.rerun()

def show_results_page(df):
    city_data = df[df['City'] == st.session_state.selected_city].iloc[0]
    grand_total, total_daily, daily_acc, daily_food = calculate_costs(
        city_data, st.session_state.adults, st.session_state.kids, st.session_state.days
    )

    st.markdown(f"<h1 style='color: {primary_teal};'>{city_data['City']}</h1>", unsafe_allow_html=True)
    st.image(city_data['Image_URL'], use_container_width=True)
    
    # Cost Breakdown
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown(f"""
            <div class="result-card">
                <h4>📊 Estimated Trip Cost</h4>
                <h2 style='color: {primary_teal};'>${grand_total:,.2f}</h2>
                <p>🏨 Accommodation ({st.session_state.days} days): ${daily_acc * st.session_state.days:,.2f}</p>
                <p>🍔 Food & Misc: ${daily_food * st.session_state.days:,.2f}</p>
            </div>
        """, unsafe_allow_html=True)
        st.info(f"✨ **Why visit?** {city_data['Description']}")

    with col_right:
        budget_diff = st.session_state.budget - grand_total
        if budget_diff >= 0:
            st.success(f"✅ Within Budget! +${budget_diff:,.2f}")
        else:
            st.error(f"⚠️ Over Budget by ${abs(budget_diff):,.2f}")
        st.metric("Daily Avg", f"${total_daily:,.2f}")

    if st.button("⬅️ Back to Discovery"):
        st.session_state.page = "discovery"
        st.rerun()

# --- 4. MAIN CONTROLLER ---
def main():
    apply_custom_styles()
    df = get_malaysia_data()
    
    if df is None:
        st.error("CSV not found.")
        return

    # Initialization
    for key in ['page', 'state', 'budget', 'adults', 'kids', 'days', 'selected_city']:
        if key not in st.session_state:
            st.session_state[key] = "splash" if key == 'page' else None

    # Page Routing
    if st.session_state.page == "splash": show_splash()
    elif st.session_state.page == "search": show_search_page(df)
    elif st.session_state.page == "discovery": show_discovery_page(df)
    elif st.session_state.page == "results": show_results_page(df)

if __name__ == "__main__":
    main()