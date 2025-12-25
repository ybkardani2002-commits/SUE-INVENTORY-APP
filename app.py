import streamlit as st
import pandas as pd

# 1. Configuration
st.set_page_config(page_title="SUE Inventory", layout="wide")

# 2. Load Data from GitHub
@st.cache_data
def load_data():
    # This must match your filename exactly
    df = pd.read_csv("SUE STOCK PRICE.xlsx - Master.csv")
    df['STOCK'] = df['STOCK'].fillna(0)
    # Convert margin to percentage for display
    if 'Margin' in df.columns:
        df['Margin'] = df['Margin'].fillna(0) * 100
    return df

try:
    df = load_data()
    
    st.title("📊 Shree Umiya Electricals")
    st.subheader("Inventory Management System")

    # --- Search Bar ---
    search = st.text_input("🔍 Search for an Item (e.g., 'Pump' or 'Motor')")
    
    if search:
        display_df = df[df['NAME'].str.contains(search, case=False, na=False)]
    else:
        display_df = df

    # --- Key Stats ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Items", len(display_df))
    low_stock = len(display_df[display_df['STOCK'] <= 0])
    c2.metric("Out of Stock", low_stock, delta_color="inverse")
    
    # --- Table ---
    st.dataframe(
        display_df[['NAME', 'Category', 'STOCK', 'Purchase Rate', 'Last Sale Rate', 'NEW HSN 8']], 
        use_container_width=True
    )

except Exception as e:
    st.error(f"Error loading file: {e}")
    st.info("Make sure the filename in app.py matches the file uploaded to GitHub.")
