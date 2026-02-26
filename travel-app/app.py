import streamlit as st
import time
from datetime import date

# --- 1. GLOBAL STYLE ---
st.set_page_config(page_title="N-AME Travel", page_icon="🦅")
primary_teal = "#0CA38D"

# --- 2. THE APP'S "MEMORY" ---
# This tracks which page the user is currently looking at
if 'current_page' not in st.session_state:
    st.session_state.current_page = "splash"

# --- 3. PAGE 1: SPLASH SCREEN (Your Design Page 1) ---
if st.session_state.current_page == "splash":
    # Centered branding as per your design 
    st.markdown(f"""
        <div style='text-align: center; padding-top: 150px;'>
            <h1 style='font-size: 100px; margin: 0;'>🦅</h1>
            <h1 style='color: {primary_teal}; font-size: 60px; letter-spacing: 5px;'>N-AME</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # Wait for 2 seconds then switch pages
    time.sleep(2) 
    st.session_state.current_page = "search"
    st.rerun()

# --- 4. PAGE 2: SEARCH INPUTS (Your Design Page 2) ---
elif st.session_state.current_page == "search":
    # Header logo
    st.markdown(f"<h1 style='text-align: center; color: {primary_teal};'>N-AME</h1>", unsafe_allow_html=True)
    st.write("### Plan Your Trip")
    
    # Input fields from your design [cite: 70, 71, 72]
    location = st.text_input("📍 Location", placeholder="Where to?")
    
    col1, col2 = st.columns(2)
    with col1:
        travel_date = st.date_input("📅 Date", date.today())
    with col2:
        budget = st.number_input("💰 Budget ($)", min_value=0, step=100)

    # Search button
    if st.button("Search"):
        st.session_state.searching = True

    # --- PAGE 3: BUDGET ALLOCATION (If search is clicked) ---
    if st.session_state.get('searching'):
        st.markdown("---")
        st.markdown(f"<h3 style='color: {primary_teal};'>Fine-tune Your Budget</h3>", unsafe_allow_html=True)
        
        # Creating the green sliders from your design 
        acc = st.slider("🏠 Accommodation", 0, 100, 40)
        food = st.slider("🍔 Food", 0, 100, 20)
        trans = st.slider("🚗 Transportation", 0, 100, 20)
        exp = st.slider("🛍️ Expenditure", 0, 100, 20)
        
        # Calculate the money value based on total budget
        total_spent = (acc + food + trans + exp)
        
        if total_spent != 100:
            st.warning(f"Total is {total_spent}%. Adjust to 100% to see results!")
        else:
            st.success("Perfect! Showing your travel options...")
            # This is where Page 4 (The Result Cards) will appear next [cite: 16-22]