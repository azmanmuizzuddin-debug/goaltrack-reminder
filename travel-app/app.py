import streamlit as st
import pandas as pd
import time
from datetime import date
import os

# --- 1. GLOBAL UI CONFIG ---
st.set_page_config(page_title="N-AME Travel", page_icon="🦅", layout="centered")
primary_teal = "#0CA38D"

st.markdown(f"""
    <style>
    /* Fixed Button & Card Styles */
    .stButton>button {{ background-color: {primary_teal}; color: white; border-radius: 12px; height: 3.5em; border: none; font-weight: bold; }}
    .result-card {{ background-color: #f9f9f9; padding: 25px; border-radius: 20px; border-left: 8px solid {primary_teal}; margin-bottom: 20px; }}
    
    /* Force Logo to stay Large and Centered */
    .logo-container {{
        text-align: center;
        width: 100%;
        margin-top: 50px;
    }}
    .brand-icon {{ font-size: 100px !important; margin: 0; line-height: 1; }}
    .brand-title {{ 
        color: {primary_teal}; 
        font-size: 60px !important; 
        font-weight: 900; 
        letter-spacing: 10px; 
        margin-top: -10px;
        text-transform: uppercase;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADING ---
@st.cache_data
def get_malaysia_data():
    paths = ['malaysia_travel.csv', 'travel-app/malaysia_travel.csv']
    for path in paths:
        if os.path.exists(path):
            return pd.read_csv(path)
    return None

df = get_malaysia_data()

# --- 3. SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "splash"

# --- 4. PAGE 1: SPLASH SCREEN ---
if st.session_state.page == "splash":
    st.markdown('<div class="logo-container" style="padding-top:100px;"><p class="brand-icon">🦅</p><p class="brand-title">N-AME</p></div>', unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.page = "search"
    st.rerun()

# --- 5. PAGE 2: SEARCH DASHBOARD ---
elif st.session_state.page == "search":
    # Logo Header
    st.markdown('<div class="logo-container"><p class="brand-icon">🦅</p><p class="brand-title">N-AME</p></div>', unsafe_allow_html=True)

    if df is None:
        st.error("⚠️ CSV File not found! Check your folder.")
        st.stop()

    st.write("### ✈️ Plan Your Trip")
    selected_state = st.selectbox("📍 Select State", sorted(df['State'].unique()))
    selected_city = st.selectbox("🏙️ Select City/Spot", df[df['State'] == selected_state]['City'])
    
    col_a, col_b = st.columns(2)
    with col_a:
        travel_date = st.date_input("📅 Travel Date", date.today())
    with col_b:
        user_budget = st.number_input("💰 Budget ($)", min_value=10, value=1500)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2026 Width Standard
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🔍 Search Now", width="stretch"):
            st.session_state.page = "results"
            st.session_state.city = selected_city
            st.session_state.budget = user_budget
            st.rerun()
    with btn_col2:
        with st.popover("⚙️ Filters", width="stretch"):
            st.markdown(f"<h4 style='color: {primary_teal};'>Budget Allocation</h4>", unsafe_allow_html=True)
            acc = st.slider("🏠 Accommodation (%)", 0, 100, 40)
            food = st.slider("🍔 Food (%)", 0, 100, 20)
            trans = st.slider("🚗 Transportation (%)", 0, 100, 20)
            exp = st.slider("🛍️ Expenditure (%)", 0, 100, 20)
            
            total_pct = acc + food + trans + exp
            st.write(f"**Total: {total_pct}%**")
            if total_pct != 100:
                st.warning("Must equal 100% to apply.")

# --- 6. PAGE 3: DYNAMIC RESULTS ---
elif st.session_state.page == "results":
    # CRITICAL: Re-fetch the data row here to ensure details aren't "missing"
    city_data = df[df['City'] == st.session_state.city].iloc[0]
    
    st.markdown(f"<h1 style='color: {primary_teal}; margin-bottom:0;'>{st.session_state.city}</h1>", unsafe_allow_html=True)
    st.caption(f"Location: {city_data['State']} | Date: {date.today()}")
    
    # Hero Image
    if 'Image_URL' in city_data and pd.notna(city_data['Image_URL']):
        st.image(city_data['Image_URL'], width="stretch")
    
    # Detailed Cards
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown(f"""
            <div class="result-card">
                <h4>📍 About {st.session_state.city}</h4>
                <p>{city_data['Description']}</p>
                <hr>
                <p><b>Accommodation:</b> ${city_data['Accommodation_Daily']}/night</p>
                <p><b>Daily Meals:</b> ${city_data['Food_Daily']}/day</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        daily_total = city_data['Accommodation_Daily'] + city_data['Food_Daily'] + city_data['Transport_Daily']
        days = int(st.session_state.budget / daily_total) if daily_total > 0 else 0
        st.metric("Affordable Days", f"{days} Days")
        st.metric("Budget Remaining", f"${st.session_state.budget % daily_total}")

    if st.button("⬅️ Change Destination", width="stretch"):
        st.session_state.page = "search"
        st.rerun()