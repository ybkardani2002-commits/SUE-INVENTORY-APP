import streamlit as st
import pandas as pd

# 1. SETTINGS - Make sure this matches your file name on GitHub exactly!
# If your file is "sue master stock.csv", keep it like this.
DATA_FILENAME = "SUE STOCK PRICE.csv"

@st.cache_data
def load_data():
    try:
        # 'latin1' encoding handles the special characters from Excel
        df = pd.read_csv(DATA_FILENAME, encoding='latin1')
        
        # Clean up column names (removes extra spaces)
        df.columns = df.columns.str.strip()
        
        # Convert STOCK and Prices to numbers, handling errors
        if 'STOCK' in df.columns:
            df['STOCK'] = pd.to_numeric(df['STOCK'], errors='coerce').fillna(0)
        if 'Purchase Rate' in df.columns:
            df['Purchase Rate'] = pd.to_numeric(df['Purchase Rate'], errors='coerce').fillna(0)
        if 'Last Sale Rate' in df.columns:
            df['Last Sale Rate'] = pd.to_numeric(df['Last Sale Rate'], errors='coerce').fillna(0)
            
        return df
    except FileNotFoundError:
        st.error(f"❌ File not found: {DATA_FILENAME}. Please check the name on GitHub.")
        return None
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None

# --- APP INTERFACE ---
st.set_page_config(page_title="SUE Inventory", layout="wide")
st.title("📊 Shree Umiya Electricals")
st.markdown("### Stock & Price Management System")

df = load_data()

if df is not None:
    # --- Sidebar Filters ---
    st.sidebar.header("Filter Results")
    search = st.sidebar.text_input("🔍 Search Item Name")
    
    if 'Category' in df.columns:
        categories = ["All"] + sorted(df['Category'].dropna().unique().tolist())
        cat_filter = st.sidebar.selectbox("Category", categories)
    else:
        cat_filter = "All"

    # --- Apply Filters ---
    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df['NAME'].str.contains(search, case=False, na=False)]
    if cat_filter != "All":
        filtered_df = filtered_df[filtered_df['Category'] == cat_filter]

    # --- Metrics ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Items", len(filtered_df))
    
    if 'STOCK' in filtered_df.columns:
        low_stock = len(filtered_df[filtered_df['STOCK'] <= 0])
        c2.metric("Out of Stock", low_stock)
        
        stock_value = (filtered_df['STOCK'] * filtered_df['Purchase Rate']).sum()
        c3.metric("Stock Value (Purchase)", f"₹{stock_value:,.2f}")

    # --- Data Table ---
    cols_to_show = ['NAME', 'STOCK', 'Purchase Rate', 'Last Sale Rate', 'NEW HSN 8']
    # Only show columns that actually exist in your file
    existing_cols = [c for c in cols_to_show if c in filtered_df.columns]
    
    st.dataframe(filtered_df[existing_cols], use_container_width=True)

else:
    st.warning("Please verify that your CSV file is uploaded to GitHub and the name is correct.")
