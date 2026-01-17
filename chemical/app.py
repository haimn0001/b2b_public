import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- CONFIGURATION ---
DATA_FILE = 'b2b_leads.csv'
ADMIN_PASSWORD = 'admin'  # Simple password for the dashboard

# --- SETUP DATA STORAGE ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=['Date', 'Company_Name', 'Material_Category', 'Quantity_Kg', 'Contact_Info', 'Status'])
    return pd.read_csv(DATA_FILE)

def save_lead(company, material, quantity, contact):
    df = load_data()
    new_data = pd.DataFrame({
        'Date': [datetime.now().strftime("%Y-%m-%d %H:%M")],
        'Company_Name': [company],
        'Material_Category': [material],
        'Quantity_Kg': [quantity],
        'Contact_Info': [contact],
        'Status': ['New']
    })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# --- APP INTERFACE ---
st.set_page_config(page_title="RawMat B2B Portal", layout="wide")

# Sidebar for Navigation
page = st.sidebar.radio("Navigate", ["Buyer Portal (Public)", "Admin Dashboard (Private)"])

# --- PAGE 1: BUYER PORTAL (The "Opening") ---
if page == "Buyer Portal (Public)":
    st.title("🏭 Industrial Raw Materials Procurement")
    st.write("### Sourcing High-Grade Materials for Manufacturing")
    st.info("Currently serving: Specialty Chemicals, Metals, and Bulk Polymers.")

    with st.form("rfq_form"):
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name")
            contact_info = st.text_input("Email / Phone Number")
        with col2:
            material_type = st.selectbox("Material Category", 
                ["Specialty Chemicals", "Industrial Metals", "Polymers", "Agro-Commodities", "Other"])
            quantity = st.number_input("Est. Monthly Requirement (Kg/Tons)", min_value=0)
        
        requirements = st.text_area("Specific Requirements (Purity, Grade, Delivery Location)")
        
        submitted = st.form_submit_button("Request Quote")
        
        if submitted:
            if company_name and contact_info:
                save_lead(company_name, material_type, quantity, contact_info)
                st.success(f"Request received! We will contact {company_name} shortly.")
            else:
                st.error("Please fill in your company name and contact info.")

# --- PAGE 2: ADMIN DASHBOARD (The "Checking") ---
elif page == "Admin Dashboard (Private)":
    st.sidebar.markdown("---")
    pwd = st.sidebar.text_input("Admin Password", type="password")
    
    if pwd == ADMIN_PASSWORD:
        st.title("📊 Procurement Strategy Dashboard")
        
        df = load_data()
        
        if not df.empty:
            # 1. High-Level Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Leads", len(df))
            col2.metric("Top Category", df['Material_Category'].mode()[0] if not df.empty else "N/A")
            col3.metric("Recent Inquiry", df['Date'].iloc[-1])
            
            # 2. Visualizations
            st.subheader("Demand Analysis")
            c1, c2 = st.columns(2)
            
            with c1:
                # Pie chart of material categories
                fig_cat = px.pie(df, names='Material_Category', title='Demand by Material Type')
                st.plotly_chart(fig_cat, use_container_width=True)
                
            with c2:
                # Bar chart of quantities
                # Ensure Quantity is numeric for plotting
                df['Quantity_Kg'] = pd.to_numeric(df['Quantity_Kg'])
                fig_vol = px.bar(df, x='Company_Name', y='Quantity_Kg', color='Material_Category', title='Volume Requested per Lead')
                st.plotly_chart(fig_vol, use_container_width=True)

            # 3. Data Table
            st.subheader("Recent Inquiries")
            st.dataframe(df)
            
            # Simple Download Button for Excel
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Leads CSV", csv, "leads.csv", "text/csv")
            
        else:
            st.warning("No data yet. Go to the Buyer Portal and submit a test request.")
            
    else:
        st.warning("Please enter the admin password to view strategy data.")