import streamlit as st
import pandas as pd
import time
from datetime import date

# --- 1. GLOBAL SETTINGS ---
st.set_page_config(page_title="N-AME Travel", page_icon="🦅")
primary_teal = "#0CA38D"

st.markdown(f"""
    <style>
    .stButton>button {{ background-color: {primary_teal}; color: white; border-radius: 10px; border: none; }}
    .result-card {{ background-color: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 5px solid {primary_teal}; margin-bottom: 15px; }}
    .brand {{ text-align: center; padding-bottom: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    # Ensure this matches your folder structure in VS Code
    return pd.read_csv('travel-app/malaysia_travel.csv')

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

# --- 3. STATE MANAGEMENT ---
if 'page' not in st.session_state:
    st.session_state.page = "splash"

# --- 4. PAGE 1: SPLASH SCREEN ---
if st.session_state.page == "splash":
    st.markdown(f"<div style='text-align: center; padding-top: 150px;'><h1 style='font-size: 100px;'>🦅</h1><h1 style='color: {primary_teal}; font-size: 60px;'>N-AME</h1></div>", unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.page = "search"
    st.rerun()

# --- 5. PAGE 2: SEARCH (MALAYSIA) ---
elif st.session_state.page == "search":
    # Logo at the top of the name
    st.markdown(f"<div class='brand'><h1>🦅</h1><h1 style='color:{primary_teal}; margin-top:-20px;'>N-AME</h1></div>", unsafe_allow_html=True)
    
    # Malaysia State & City Selection
    selected_state = st.selectbox("📍 Select State", df['State'].unique())
    city = st.selectbox("🏙️ Select City", df[df['State'] == selected_state]['City'])
    
    col1, col2 = st.columns(2)
    with col1:
        trip_date = st.date_input("📅 Travel Date", date.today())
    with col2:
        budget = st.number_input("💰 Total Budget ($)", min_value=0, value=1000)

    st.markdown("<br>", unsafe_allow_html=True)
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🔍 Search Now", use_container_width=True):
            st.session_state.page = "results"
            st.session_state.city = city
            st.session_state.budget = budget
            st.rerun()
    with btn_col2:
        with st.popover("⚙️ Filter Budget", use_container_width=True):
            st.write("### Allocation")
            st.slider("🏠 Accommodation", 0, 100, 40)
            st.slider("🍔 Food", 0, 100, 20)
            st.slider("🚗 Transport", 0, 100, 20)

# --- 6. PAGE 3: DIFFERENT RESULTS PAGE ---
elif st.session_state.page == "results":
    city_info = df[df['City'] == st.session_state.city].iloc[0]
    
    st.markdown(f"<h2 style='color: {primary_teal};'>{st.session_state.city}, {city_info['State']}</h2>", unsafe_allow_html=True)
    
    # Real Data Card
    st.markdown(f"""
        <div class="result-card">
            <h4>📍 Destination Overview</h4>
            <p>{city_info['Description']}</p>
            <p><b>Estimated Daily Cost:</b> ${city_info['Accommodation_Daily'] + city_info['Food_Daily']}</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("⬅️ Back to Search"):
        st.session_state.page = "search"
        st.rerun()