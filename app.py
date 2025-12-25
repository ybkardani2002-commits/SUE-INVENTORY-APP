import streamlit as st
import pandas as pd

# 1. SETTINGS - Ensure this matches your file on GitHub exactly
DATA_FILENAME = "SUE STOCK PRICE.csv"

@st.cache_data
def load_data():
    try:
        # We use engine='python' to prevent "Buffer Overflow" errors
        # We use on_bad_lines='skip' to ignore rows that are broken
        df = pd.read_csv(
            DATA_FILENAME, 
            encoding='latin1', 
            engine='python', 
            on_bad_lines='skip'
        )
        
        # Clean column names
        df.columns = [str(c).strip() for c in df.columns]
        
        # Clean numeric data
        cols_to_fix = ['STOCK', 'Purchase Rate', 'Last Sale Rate']
        for col in cols_to_fix:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    except FileNotFoundError:
        st.error(f"❌ Could not find the file: {DATA_FILENAME}")
        return None
    except Exception as e:
        st.error(f"❌ Data Error: {e}")
        return None

# --- APP SETUP ---
st.set_page_config(page_title="SUE Inventory", layout="wide")
st.title("📊 Shree Umiya Electricals")

df = load_data()

if df is not None:
    # --- Search ---
    search = st.text_input("🔍 Search Item Name (e.g. Pump, Motor, etc.)")

    if search:
        # Simple search filter
        filtered_df = df[df['NAME'].astype(str).str.contains(search, case=False, na=False)]
    else:
        filtered_df = df

    # --- Summary Metrics ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Items", len(filtered_df))
    
    if 'STOCK' in filtered_df.columns:
        low_stock = len(filtered_df[filtered_df['STOCK'] <= 0])
        c2.metric("Out of Stock", low_stock)
        
        if 'Purchase Rate' in filtered_df.columns:
            total_val = (filtered_df['STOCK'] * filtered_df['Purchase Rate']).sum()
            c3.metric("Stock Value", f"₹{total_val:,.0f}")

    # --- Display Table ---
    # Only showing the most important columns to keep it clean
    display_cols = ['NAME', 'STOCK', 'Purchase Rate', 'Last Sale Rate', 'NEW HSN 8']
    existing_cols = [c for c in display_cols if c in filtered_df.columns]
    
    st.dataframe(filtered_df[existing_cols], use_container_width=True, hide_index=True)

else:
    st.info("Searching for your CSV file on GitHub...")
