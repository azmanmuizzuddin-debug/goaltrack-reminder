import streamlit as st
import time
from datetime import date

# --- 1. SETTINGS & CSS ---
st.set_page_config(page_title="N-AME Travel", page_icon="🦅")
primary_teal = "#0CA38D"

st.markdown(f"""
    <style>
    .stButton>button {{
        background-color: {primary_teal};
        color: white;
        border-radius: 10px;
    }}
    .result-card {{
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        margin-bottom: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. NAVIGATION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "splash"

# --- 3. PAGE 1: SPLASH SCREEN ---
if st.session_state.page == "splash":
    st.markdown(f"<div style='text-align: center; padding-top: 150px;'><h1 style='font-size: 100px;'>🦅</h1><h1 style='color: {primary_teal}; font-size: 60px;'>N-AME</h1></div>", unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.page = "search"
    st.rerun()

# --- 4. PAGE 2: SEARCH INPUTS ---
elif st.session_state.page == "search":
    st.markdown(f"<div style='text-align: center;'><h1 style='margin: 0;'>🦅</h1><h1 style='color: {primary_teal}; margin-top: -15px;'>N-AME</h1></div>", unsafe_allow_html=True)
    st.write("### Plan Your Trip")
    
    location = st.text_input("📍 Destination", placeholder="Where to?")
    col1, col2 = st.columns(2)
    with col1:
        date_trip = st.date_input("📅 Date", date.today())
    with col2:
        budget = st.number_input("💰 Budget ($)", min_value=0, value=1000)

    # Buttons
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        if st.button("🔍 Search Now", use_container_width=True):
            if location:
                st.session_state.page = "results"
                st.session_state.last_location = location
                st.session_state.last_budget = budget
                st.rerun()
            else:
                st.warning("Enter a location!")
    with b_col2:
        with st.popover("⚙️ Filter Budget", use_container_width=True):
            st.slider("🏠 Accommodation (%)", 0, 100, 40)
            st.slider("🍔 Food (%)", 0, 100, 20)
            st.slider("🚗 Transportation (%)", 0, 100, 20)
            st.slider("🛍️ Expenditure (%)", 0, 100, 20)

# --- 5. PAGE 3: RESULTS VIEW (Different Page) ---
elif st.session_state.page == "results":
    st.markdown(f"<h2 style='color: {primary_teal};'>Results for {st.session_state.last_location}</h2>", unsafe_allow_html=True)
    st.write(f"Showing options for a **${st.session_state.last_budget}** budget.")
    
    # Result Cards
    st.markdown(f"""
        <div class="result-card">
            <h4>🏨 Standard Stay</h4>
            <p>A balanced mix of comfort and value.</p>
            <h5 style='color: {primary_teal};'>${st.session_state.last_budget * 0.8:.0f}</h5>
        </div>
        <div class="result-card">
            <h4>🌟 Premium Stay</h4>
            <p>The best hotels and fine dining.</p>
            <h5 style='color: {primary_teal};'>${st.session_state.last_budget * 1.2:.0f}</h5>
        </div>
    """, unsafe_allow_html=True)

    # Back Button
    if st.button("⬅️ Back to Search"):
        st.session_state.page = "search"
        st.rerun()