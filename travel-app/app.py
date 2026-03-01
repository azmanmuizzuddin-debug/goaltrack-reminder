import streamlit as st
import pandas as pd
import time
from datetime import date
import os

# --- 1. GLOBAL UI CONFIG (Mobile-First Style) ---
st.set_page_config(page_title="N-AME Travel", page_icon="🦅", layout="centered")
primary_teal = "#0CA38D"

def apply_custom_styles():
    st.markdown(f"""
        <style>
        /* This is the magic code that makes the Island float at the top */
        .floating-island {{
            position: fixed !important;
            top: 20px !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            background-color: {primary_teal} !important;
            color: white !important;
            padding: 10px 30px !important;
            border-radius: 50px !important;
            z-index: 999999 !important;
            display: flex !important;
            gap: 15px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
            font-family: sans-serif !important;
        }}
        /* Modern Rounded Buttons */
        .stButton>button {{ 
            background-color: {primary_teal}; color: white; border-radius: 25px; 
            height: 3.5em; border: none; font-weight: bold; width: 100%;
            transition: 0.3s;
        }}
        .stButton>button:hover {{ opacity: 0.8; transform: scale(1.02); }}
        
        /* Floating Cards */
        .result-card {{ 
            background-color: #ffffff; padding: 20px; border-radius: 15px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 10px solid {primary_teal};
            margin-bottom: 20px; 
        }}
        
        /* Brand Header */
        .logo-container {{ text-align: center; margin-top: 20px; margin-bottom: 20px; }}
        .brand-icon {{ font-size: 80px !important; margin: 0; }}
        .brand-title {{ 
            color: {primary_teal}; font-size: 45px !important; font-weight: 900; 
            letter-spacing: 8px; margin-top: -15px; text-transform: uppercase; 
        }}
        </style>
        """, unsafe_allow_html=True)

# --- 2. DATA & LOGIC ---
@st.cache_data
def get_malaysia_data():
    paths = ['malaysia_travel.csv', 'travel-app/malaysia_travel.csv']
    for path in paths:
        if os.path.exists(path): return pd.read_csv(path)
    return None

def calculate_costs(row, adults, kids, days):
    daily_acc = row['Accommodation_Daily']
    daily_food = (adults * row['Food_Daily']) + (kids * row['Food_Daily'] * 0.6)
    daily_trans = row['Transport_Daily']
    total_daily = daily_acc + daily_food + daily_trans
    return total_daily * days, total_daily, daily_acc, daily_food

# --- 3. PAGE 1: SPLASH ---
def show_splash():
    st.markdown('<div class="logo-container" style="padding-top:100px;"><p class="brand-icon">🦅</p><p class="brand-title">N-AME</p></div>', unsafe_allow_html=True)
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1)
    st.session_state.page = "search"
    st.rerun()

# --- 4. PAGE 2: SEARCH (The Funnel) ---
def show_search_page(df):
    st.markdown('<div class="logo-container"><p class="brand-icon">🦅</p><p class="brand-title">N-AME</p></div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.write("### 📍 Where to?")
        selected_state = st.selectbox("Destination", ["All States"] + sorted(df['State'].unique().tolist()), label_visibility="collapsed")
        
        st.write("📅 **Dates**")
        selected_dates = st.date_input("Travel Period", value=(date.today(), date.today()), label_visibility="collapsed")

        c1, c2 = st.columns(2)
        with c1: adults = st.number_input("Adults", min_value=1, value=1)
        with c2: kids = st.number_input("Children", min_value=0, value=0)

    # Advanced Filters (Hidden by Default)
    with st.expander("✨ Personalize Your Vibe"):
        moods = st.multiselect("Select Moods (Default: All)", ["Nature", "Dating/Romantic", "Foodie Hunt", "Busy/Street", "Hidden Gem"])
        c_rent, c_food = st.columns(2)
        with c_rent: transport = st.radio("Transport", ["Any", "Public", "Rent Car"])
        with c_food: dining = st.radio("Dining", ["All", "Local Stalls", "Hotel"])

    st.write("💰 **Total Trip Budget ($)**")
    user_budget = st.slider("Budget", 100, 5000, 1500, step=50, label_visibility="collapsed")

    if st.button("🔍 Find My Match"):
        if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
            st.session_state.update({
                "page": "discovery", "state": selected_state, "budget": user_budget,
                "adults": adults, "kids": kids, "moods": moods if moods else "All",
                "transport": transport, "dining": dining,
                "days": (selected_dates[1] - selected_dates[0]).days + 1
            })
            st.rerun()
        else: st.warning("Please select a valid date range!")

# --- 5. PAGE 3: DISCOVERY (The Selection) ---
def show_discovery_page(df):
    found_any = False
    # --- THE ISLAND (FORCED) ---
    st.markdown(f"""
        <div class="floating-island">
            <span>📍 {st.session_state.state}</span>
            <span style="opacity: 0.4;">|</span>
            <span>💰 ${st.session_state.budget}</span>
            <span style="opacity: 0.4;">|</span>
            <span>📅 {st.session_state.days} Days</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("##") # Space for the island

    # --- FILTERING LOGIC ---
    filtered_df = df.copy()
    if st.session_state.state != "All States":
        filtered_df = filtered_df[filtered_df['State'] == st.session_state.state]
    
    if isinstance(st.session_state.moods, list) and len(st.session_state.moods) > 0:
        filtered_df = filtered_df[filtered_df['Vibe'].isin(st.session_state.moods)]

    # --- THE LOOP ---
    found_any = False  # <--- THIS PREVENTS THE NAMEERROR
    
    st.markdown(f"### 📍 Results for {st.session_state.state}")

    for _, row in filtered_df.iterrows():
        total, _, _, _ = calculate_costs(row, st.session_state.adults, st.session_state.kids, st.session_state.days)
        
        if total <= st.session_state.budget:
            found_any = True
            with st.container(border=True):
                c1, c2 = st.columns([1, 2])
                with c1:
                    # Fix for the "0" broken image in your screenshot
                    img_url = row['Image_URL']
                    if str(img_url) == "0" or not img_url:
                        st.image("https://via.placeholder.com/400x250?text=N-AME+Travel", use_container_width=True)
                    else:
                        st.image(img_url, use_container_width=True)
                with c2:
                    st.subheader(row['City'])
                    st.caption(f"🎭 {row['Vibe']} | ⭐ {row['Rating']}")
                    st.write(f"💰 Est. **${total:,.2f}**")
                    if st.button(f"View {row['City']}", key=f"btn_{row['City']}"):
                        st.session_state.selected_city = row['City']
                        st.session_state.page = "results"
                        st.rerun()

    # --- FOOTER ---
    if not found_any:
        st.warning("No matches! Try increasing your budget or changing moods.")
        
    if st.button("⬅️ Back to Search"):
        st.session_state.page = "search"
        st.rerun()

# --- 6. PAGE 4: RESULTS (The "All-Out" Detail) ---
def show_results_page(df):
    city_data = df[df['City'] == st.session_state.selected_city].iloc[0]
    total, _, acc, food = calculate_costs(city_data, st.session_state.adults, st.session_state.kids, st.session_state.days)

    # 1. Header & Image (Top of your sketch)
    st.markdown(f"## 🌴 {city_data['City']} Itinerary")
    if city_data['Image_URL'] and str(city_data['Image_URL']) != "0":
        st.image(city_data['Image_URL'], use_container_width=True)
    
    # 2. Details Section (The white box in your sketch)
    with st.container(border=True):
        st.write("### 📄 Details")
        st.write(f"{city_data['Description']}")
        
        # 3. Comments Area (Sub-section in your sketch)
        st.markdown("#### 💬 Comments")
        st.caption("⭐⭐⭐⭐⭐ 'The view was breathtaking, definitely coming back!' - @traveler_amy")
        st.caption("⭐⭐⭐⭐ 'Great food spots nearby, but bring an umbrella.' - @zack_fly")

    # 4. Foods Section (The horizontal bar in your sketch)
    st.write("### 🍜 Local Foods")
    f1, f2, f3 = st.columns(3)
    # Using placeholders for now since we haven't added food images to CSV yet
    f1.image("https://via.placeholder.com/150?text=Food+1", caption="Signature Dish")
    f2.image("https://via.placeholder.com/150?text=Food+2", caption="Local Drink")
    f3.image("https://via.placeholder.com/150?text=Food+3", caption="Dessert")

    # 5. Activities Section (The bottom list in your sketch)
    st.write("### 🎯 Activities")
    # We split the 'Activities' column we made earlier
    if 'Activities' in city_data:
        acts = city_data['Activities'].split(", ")
        for a in acts:
            with st.container(border=True):
                col_icon, col_txt = st.columns([1, 4])
                col_icon.write("📍") # Icon placeholder
                col_txt.write(f"**{a}**")

    # 6. Booking Summary & Buttons (Footer)
    st.divider()
    st.write(f"💰 **Estimated Total: ${total:,.2f}**")
    
    col_btn1, col_btn2 = st.columns(2)
    if col_btn1.button("🚀 Book My Trip"):
        st.balloons()
    if col_btn2.button("⬅️ Back", type="secondary"):
        st.session_state.page = "discovery"
        st.rerun()

# --- 7. MAIN APP ---
def main():
    apply_custom_styles()
    df = get_malaysia_data()
    if df is None: return st.error("Please run your Data Generator first!")

    for key in ['page', 'state', 'budget', 'adults', 'kids', 'days', 'selected_city', 'moods']:
        if key not in st.session_state:
            st.session_state[key] = "splash" if key == 'page' else None

    if st.session_state.page == "splash": show_splash()
    elif st.session_state.page == "search": show_search_page(df)
    elif st.session_state.page == "discovery": show_discovery_page(df)
    elif st.session_state.page == "results": show_results_page(df)

if __name__ == "__main__":
    main()