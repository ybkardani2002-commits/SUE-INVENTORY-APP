import streamlit as st
import pandas as pd

# 1. SETTINGS
DATA_FILENAME = "SUE STOCK PRICE.csv"

@st.cache_data
def load_data():
    try:
        # Loading with 'latin1' for Excel characters and skipping messy rows
        df = pd.read_csv(DATA_FILENAME, encoding='latin1', on_bad_lines='skip')
        
        # Remove extra spaces from column names
        df.columns = [str(c).strip() for c in df.columns]
        
        # Convert numbers correctly
        numeric_cols = ['STOCK', 'Purchase Rate', 'Last Sale Rate', 'MRP']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    except FileNotFoundError:
        st.error(f"❌ File Not Found: {DATA_FILENAME}")
        return None
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None

# --- APP INTERFACE ---
st.set_page_config(page_title="SUE Inventory", layout="wide")
st.title("📊 Shree Umiya Electricals")

df = load_data()

if df is not None:
    # --- Search ---
    search = st.text_input("🔍 Search Item Name or HSN")

    if search:
        # Filters rows where the search term is in the NAME column
        filtered_df = df[df['NAME'].astype(str).str.contains(search, case=False, na=False)]
    else:
        filtered_df = df

    # --- Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Items", len(filtered_df))
    
    if 'STOCK' in filtered_df.columns:
        low_stock = len(filtered_df[filtered_df['STOCK'] <= 0])
        col2.metric("Out of Stock", low_stock)
        
        if 'Purchase Rate' in filtered_df.columns:
            total_value = (filtered_df['STOCK'] * filtered_df['Purchase Rate']).sum()
            col3.metric("Stock Value", f"₹{total_value:,.0f}")

    # --- Table ---
    cols_to_show = ['NAME', 'STOCK', 'Purchase Rate', 'Last Sale Rate', 'NEW HSN 8']
    existing_cols = [c for c in cols_to_show if c in filtered_df.columns]
    
    st.dataframe(filtered_df[existing_cols], use_container_width=True, hide_index=True)

else:
    st.warning("Please check if 'SUE STOCK PRICE.csv' is uploaded to your GitHub repository.")
