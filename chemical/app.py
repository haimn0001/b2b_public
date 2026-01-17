import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# --- 1. CONFIGURATION & HIGH-TECH THEME ---
st.set_page_config(
    page_title="NEXUS GLOBAL | Industrial Trade",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for "Billion Dollar" Aesthetics (Dark Mode, Glassmorphism, Neon Accents)
st.markdown("""
    <style>
    /* GLOBAL DARK THEME & FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp {
        background-color: #050510;
        background-image: radial-gradient(circle at 50% 50%, #1a1a40 0%, #050510 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* HEADINGS - CYBERPUNK/HIGH-TECH STYLE */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        color: #FFFFFF;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    h1 {
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }
    
    /* GLASSMORPHISM CARDS */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #00d4ff;
    }
    
    /* BUTTONS - NEON GLOW */
    .stButton>button {
        background: linear-gradient(45deg, #00d4ff, #005bea);
        color: white;
        border: none;
        border-radius: 5px;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px #00d4ff;
    }
    
    /* INPUT FIELDS - MINIMALIST */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 5px;
    }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #02020a;
        border-right: 1px solid #1f1f3a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
DATA_FILE = 'b2b_leads.csv'
ADMIN_PASSWORD = 'admin'

def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=['Date', 'Company', 'Industry', 'Region', 'Material', 'Volume_MT', 'Status'])
    return pd.read_csv(DATA_FILE)

def save_lead(company, industry, region, material, volume):
    df = load_data()
    new_data = pd.DataFrame({
        'Date': [datetime.now().strftime("%Y-%m-%d %H:%M")],
        'Company': [company],
        'Industry': [industry],
        'Region': [region],
        'Material': [material],
        'Volume_MT': [volume],
        'Status': ['Pending Analysis']
    })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# --- 3. NAVIGATION ---
st.sidebar.title("🔐 ACCESS")
mode = st.sidebar.radio("", ["Global Trading Portal", "Command Center (Admin)"])

# --- 4. THE LANDING PAGE (CLIENT VIEW) ---
if mode == "Global Trading Portal":
    # HERO SECTION
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("NEXUS GLOBAL")
        st.subheader("Next-Gen Industrial Procurement & Supply Chain Architecture.")
        st.markdown("**Mobilizing Critical Raw Materials for the Future Economy.**")
        
    with col2:
        # FAKE LIVE TICKER
        st.markdown("""
        <div style="background: rgba(0,255,0,0.1); padding: 10px; border-radius: 5px; border: 1px solid #00ff00;">
            <span style="color: #00ff00; font-family: 'Orbitron';">● LIVE MARKET</span><br>
            LITHIUM: $13,450 (+1.2%)<br>
            COBALT: $32,100 (-0.4%)<br>
            SCRAP STEEL: $380 (+0.8%)
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # INTERACTIVE GLOBE (VISUAL ONLY)
    st.markdown("### 🌍 Global Supply Network Active")
    # Generating a dummy map to look impressive
    map_data = pd.DataFrame({
        'lat': [20.5937, 35.8617, -25.2744, 56.1304, 37.0902],
        'lon': [78.9629, 104.1954, 133.7751, -106.3468, -95.7129],
        'volume': [100, 80, 60, 40, 90]
    })
    st.map(map_data, zoom=1, use_container_width=True)

    st.markdown("---")

    # THE "BILLION DOLLAR" FORM
    st.markdown("### 🤝 Initiate Trade Partnership")
    st.write("Restricted Access. Institutional Partners Only.")
    
    with st.form("premium_rfq"):
        c1, c2 = st.columns(2)
        with c1:
            company = st.text_input("Entity / Company Name")
            industry = st.selectbox("Industry Vertical", ["EV Battery Mfg", "Aerospace & Defense", "Heavy Industries", "Pharmaceuticals", "Construction"])
            region = st.selectbox("Delivery Region", ["APAC (Asia-Pacific)", "EMEA (Europe/Mid-East)", "Americas"])
        with c2:
            material = st.selectbox("Strategic Material Required", ["Lithium Carbonate (Battery Grade)", "Industrial Scrap Metal (Ferrous)", "Rare Earth Elements", "Polymers & Resins", "Bulk Agro Commodities"])
            volume = st.number_input("Est. Quarterly Volume (Metric Tonnes)", min_value=100)
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("REQUEST PROCUREMENT ACCESS >")
        
        if submitted:
            if company:
                save_lead(company, industry, region, material, volume)
                st.balloons()
                st.success("TRANSMISSION RECEIVED. Our Trade Desk will initiate protocol shortly.")
            else:
                st.error("ENTITY NAME REQUIRED FOR PROTOCOL INITIATION.")

# --- 5. THE COMMAND CENTER (ADMIN VIEW) ---
elif mode == "Command Center (Admin)":
    pwd = st.sidebar.text_input("Enter Clearance Code", type="password")
    
    if pwd == ADMIN_PASSWORD:
        st.title("🚀 STRATEGY COMMAND CENTER")
        st.markdown("Real-time Intelligence on Supply Demand.")
        
        df = load_data()
        
        if not df.empty:
            # KPIS ROW
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Active Leads", len(df), "+2 today")
            k2.metric("Total Demand (MT)", f"{df['Volume_MT'].sum():,.0f}", "High Volume")
            k3.metric("Top Region", df['Region'].mode()[0])
            k4.metric("Est. Pipeline Value", "$4.2M", "+12%")
            
            st.markdown("---")
            
            # ADVANCED CHARTS
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("#### Demand Segmentation (By Industry)")
                fig_pie = px.pie(df, names='Industry', hole=0.6, color_discrete_sequence=px.colors.sequential.Cyan)
                fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with c2:
                st.markdown("#### Volume Requirements (Metric Tonnes)")
                fig_bar = px.bar(df, x='Company', y='Volume_MT', color='Material', template="plotly_dark")
                fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # THE DATABASE
            st.markdown("### 📂 Inbound Data Stream")
            st.dataframe(df, use_container_width=True)
        
        else:
            st.info("Awaiting Data Stream...")
            
    else:
        st.warning("ACCESS DENIED. AUTHORIZED PERSONNEL ONLY.")
