import streamlit as st
import pandas as pd

# 1. SETTINGS
DATA_FILENAME = "sue master stock.csv"

@st.cache_data
def load_data():
    try:
        # We use on_bad_lines='skip' to ignore rows that don't match the table
        # We use engine='python' because it is more flexible with messy files
        df = pd.read_csv(
            DATA_FILENAME, 
            encoding='latin1', 
            on_bad_lines='skip', 
            engine='python'
        )
        
        # CLEANUP: If the first few rows are empty or metadata, 
        # we look for the row that contains 'NAME' and make that the header
        if 'NAME' not in df.columns:
            # Try to find the header row automatically
            for i in range(len(df)):
                if 'NAME' in df.iloc[i].values:
                    df.columns = df.iloc[i]
                    df = df.iloc[i+1:].reset_index(drop=True)
                    break

        # Standardize column names
        df.columns = [str(c).strip() for c in df.columns]
        
        # Clean up Numeric Columns
        numeric_cols = ['STOCK', 'Purchase Rate', 'Last Sale Rate', 'MRP']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        return None

# --- APP UI ---
st.set_page_config(page_title="SUE Inventory", layout="wide")
st.title("📊 Shree Umiya Electricals")

df = load_data()

if df is not None and not df.empty:
    # Sidebar search
    search = st.sidebar.text_input("🔍 Search Item Name")
    
    # Filter logic
    if search:
        # Clean 'NAME' column in case of NaN
        df['NAME'] = df['NAME'].astype(str)
        filtered_df = df[df['NAME'].str.contains(search, case=False, na=False)]
    else:
        filtered_df = df

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Items Found", len(filtered_df))
    
    if 'STOCK' in filtered_df.columns:
        out_of_stock = len(filtered_df[filtered_df['STOCK'] <= 0])
        c2.metric("Out of Stock", out_of_stock)
        
        if 'Purchase Rate' in filtered_df.columns:
            total_val = (filtered_df['STOCK'] * filtered_df['Purchase Rate']).sum()
            c3.metric("Stock Value", f"₹{total_val:,.0f}")

    # Final Display
    # Pick only columns that actually exist
    cols = ['NAME', 'STOCK', 'Purchase Rate', 'Last Sale Rate', 'NEW HSN 8']
    valid_cols = [c for c in cols if c in filtered_df.columns]
    
    st.dataframe(filtered_df[valid_cols], use_container_width=True)
else:
    st.info("Searching for valid data in the uploaded file...")
