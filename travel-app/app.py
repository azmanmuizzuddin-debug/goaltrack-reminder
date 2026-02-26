import streamlit as st
import time
from datetime import date

# --- CONFIG ---
st.set_page_config(page_title="N-AME Travel", page_icon="🦅")
primary_teal = "#0CA38D"

# --- SESSION STATE ---
# This helps the app remember if it already showed the splash screen
if 'splashed' not in st.session_state:
    st.session_state.splashed = False

placeholder = st.empty()

# --- PAGE 1: SPLASH SCREEN ---
if not st.session_state.splashed:
    with placeholder.container():
        st.markdown(f"""
            <div style='text-align: center; padding-top: 150px;'>
                <h1 style='font-size: 100px; margin: 0;'>🦅</h1>
                <h1 style='color: {primary_teal}; font-size: 60px; letter-spacing: 5px;'>N-AME</h1>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(2) # The 2-second delay you asked for
        st.session_state.splashed = True
        st.rerun()

# --- PAGE 2: MAIN SEARCH (After splash) ---
with placeholder.container():
    st.markdown(f"<h1 style='text-align: center; color: {primary_teal};'>N-AME</h1>", unsafe_allow_html=True)
    st.write("### Plan Your Trip")
    
    location = st.text_input("📍 Where to?", placeholder="Enter destination...")
    
    col1, col2 = st.columns(2)
    with col1:
        travel_date = st.date_input("📅 Date", date.today())
    with col2:
        budget = st.number_input("💰 Total Budget ($)", min_value=0, step=100)

    if st.button("Search"):
        st.success(f"Searching for trips to {location}...")