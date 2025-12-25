import streamlit as st
import pandas as pd

# 1. Update this to match your NEW filename on GitHub exactly
# If the file is named "sue stock price.csv", type it exactly like that:
DATA_FILENAME = "SUE STOCK PRICE.csv" 

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(DATA_FILENAME)
        
        # Standardize columns (cleaning up spaces)
        df.columns = df.columns.str.strip()
        
        # Basic Data Cleaning
        if 'STOCK' in df.columns:
            df['STOCK'] = df['STOCK'].fillna(0)
        if 'Margin' in df.columns:
            df['Margin'] = pd.to_numeric(df['Margin'], errors='coerce').fillna(0) * 100
            
        return df
    except FileNotFoundError:
        st.error(f"❌ Error: The file '{DATA_FILENAME}' was not found in your GitHub folder.")
        st.info("Please make sure you uploaded the file and the name matches perfectly.")
        return None

# --- UI Setup ---
st.set_page_config(page_title="SUE Inventory", layout="wide")
st.title("📊 Shree Umiya Electricals")

df = load_data()

if df is not None:
    # Search box
    search = st.text_input("🔍 Search Item Name")
    
    # Filter data
    if search:
        filtered_df = df[df['NAME'].str.contains(search, case=False, na=False)]
    else:
        filtered_df = df

    # Display Metrics
    c1, c2 = st.columns(2)
    c1.metric("Total Items", len(filtered_df))
    if 'STOCK' in filtered_df.columns:
        low_stock = len(filtered_df[filtered_df['STOCK'] <= 0])
        c2.metric("Out of Stock", low_stock)

    # Display Table
    st.dataframe(filtered_df, use_container_width=True)
