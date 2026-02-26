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
for key in ['page', 'state', 'budget', 'adults', 'kids', 'days', 'selected_city']:
    if key not in st.session_state:
        st.session_state[key] = "splash" if key == 'page' else None

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
    
    st.write("📅 **Select Travel Period** (Arrival & Departure)")
    selected_dates = st.date_input(
        "Select Range",
        value=(date.today(), date.today()), # Default to today
        min_value=date.today(),
        help="Select your start and end date. Click the same day twice for a 1-day trip."
    )
    st.write("👥 **Travelers**")
    col_adults, col_kids = st.columns(2)
    with col_adults:
        adults = st.number_input("Adults (12+ yrs)", min_value=1, value=1, step=1)
    with col_kids:
        kids = st.number_input("Children (2-12 yrs)", min_value=0, value=0, step=1)
    
    st.write("💰 **Budget ($)**")
    user_budget = st.number_input("Total budget", min_value=10, value=1500)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2026 Width Standard
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🔍 Search Now", width="stretch"):
            if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
                st.session_state.page = "discovery"
                st.session_state.state = selected_state
                st.session_state.budget = user_budget
                st.session_state.start_date = selected_dates[0]
                st.session_state.end_date = selected_dates[1]
                st.session_state.adults = adults
                st.session_state.kids = kids
                
                # Calculate stay duration
                st.session_state.days = (selected_dates[1] - selected_dates[0]).days + 1
                st.rerun()
            else:
                st.warning("Please select both an arrival and departure date on the calendar.")
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

# --- PAGE 2.5: DISCOVERY LIST ---
elif st.session_state.page == "discovery":
    st.markdown(f"## 📍 Explore {st.session_state.state}")
    st.caption(f"Showing affordable spots for {st.session_state.adults} Adults & {st.session_state.kids} Children")

    # Filter by State first
    all_places = df[df['State'] == st.session_state.state]
    
    affordable_places = []

    # Math to check compatibility
    for _, row in all_places.iterrows():
        daily_food = (st.session_state.adults * row['Food_Daily']) + (st.session_state.kids * row['Food_Daily'] * 0.6)
        # Total = (Hotel + Food + Transport) * Days
        total_needed = (row['Accommodation_Daily'] + daily_food + row['Transport_Daily']) * st.session_state.days
        
        if total_needed <= st.session_state.budget:
            affordable_places.append(row)

    if not affordable_places:
        st.warning("❌ No places found within your budget for this state. Try increasing your budget or reducing days.")
    else:
        # Display the list
        for place in affordable_places:
            with st.container(border=True): # New 2026 container style
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.image(place['Image_URL'], width="stretch")
                with c2:
                    st.subheader(place['City'])
                    st.write(f"⭐ {place['Rating']} | 📍 {place['Distance_Hub']}km from Hub")
                    st.write(f"**Travel Type:** {place.get('Travel_Type', 'General')}")
                    
                    if st.button(f"Select {place['City']}", key=f"sel_{place['City']}", width="stretch"):
                        st.session_state.selected_city = place['City']
                        st.session_state.page = "results"
                        st.rerun()

    if st.button("⬅️ Back to Search", width="stretch"):
        st.session_state.page = "search"
        st.rerun()

# --- 6. PAGE 3: DYNAMIC RESULTS (Updated with Logic) ---
elif st.session_state.page == "results":
    # 1. Fetch CSV Data for the chosen city
    city_data = df[df['City'] == st.session_state.selected_city].iloc[0]
    st.title(f"Plan for {city_data['City']}")
    # 2. Get variables from Session State
    num_days = st.session_state.days
    adults = st.session_state.adults
    kids = st.session_state.kids
    total_budget = st.session_state.budget

    # 3. CALCULATE COSTS
    # We assume kids cost 60% of an adult for food/transport
    daily_acc = city_data['Accommodation_Daily'] # Usually per room, not per person
    daily_food_adult = city_data['Food_Daily']
    daily_food_kids = city_data['Food_Daily'] * 0.6
    daily_trans = city_data['Transport_Daily']

    # Total per day for the whole group
    total_daily = daily_acc + (adults * daily_food_adult) + (kids * daily_food_kids) + daily_trans
    
    # Total for the entire trip duration
    grand_total = total_daily * num_days

    # --- UI DISPLAY ---
    st.markdown(f"<h1 style='color: {primary_teal}; margin-bottom:0;'>{st.session_state.selected_city}</h1>", unsafe_allow_html=True)
    st.caption(f"Trip Duration: {num_days} Days | Travelers: {adults} Adults, {kids} Children")

    if 'Image_URL' in city_data and pd.notna(city_data['Image_URL']):
        st.image(city_data['Image_URL'], width="stretch")

    # Budget Health Check
    budget_diff = total_budget - grand_total
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown(f"""
            <div class="result-card">
                <h4>📊 Estimated Trip Cost</h4>
                <p>Total for <b>{num_days} days</b> for your group:</p>
                <h2 style='color: {primary_teal};'>${grand_total:,.2f}</h2>
                <hr>
                <p>🏨 Accommodation: ${daily_acc * num_days:,.2f}</p>
                <p>🍔 Food & Misc: ${(adults * daily_food_adult + kids * daily_food_kids) * num_days:,.2f}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.info(f"✨ **Why visit?** {city_data['Description']}")

    with col_right:
        if budget_diff >= 0:
            st.success(f"✅ Within Budget! You have **${budget_diff:,.2f}** extra for shopping.")
        else:
            st.error(f"⚠️ Over Budget by **${abs(budget_diff):,.2f}**. Consider reducing days or travelers.")
        
        # Metrics for quick view
        st.metric("Daily Avg", f"${total_daily:,.2f}")
        st.metric("Trip Total", f"${grand_total:,.2f}")

    if st.button("⬅️ Change Details", width="stretch"):
        st.session_state.page = "search"
        st.rerun()