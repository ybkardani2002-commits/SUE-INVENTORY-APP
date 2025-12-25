import streamlit as st
import pandas as pd

# 1. SETTINGS - Filename updated as requested
DATA_FILENAME = "SUE STOCK PRICE.csv"

@st.cache_data
def load_data():
    try:
        # Loading with 'latin1' to handle special characters and skipping bad rows
        df = pd.read_csv(DATA_FILENAME, encoding='latin1', on_bad_lines='skip')
        
        # Clean up column names
        df.columns = [str(c).strip() for c in df.columns]
        
        # Convert numeric columns safely
        cols_to_fix = ['STOCK', 'Purchase Rate', 'Last Sale Rate', 'MRP', 'Margin']
        for col in cols_to_fix:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    except FileNotFoundError:
        st.error(f"❌ Could not find the file: {DATA_FILENAME}")
        st.info("Please ensure your file on GitHub is named exactly 'SUE STOCK PRICE.csv' (case sensitive).")
        return None
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None

# --- APP LAYOUT ---
st.set_page_config(page_title="SUE Inventory", layout="wide")
st.title("📊 Shree Umiya Electricals")

df = load_data()

if df is not None:
    # --- Search Bar ---
    search = st.text_input("🔍 Search by Item Name or HSN Code")

    # --- Filtering Logic ---
    if search:
        # Search in Name and HSN column
        mask = df['NAME'].astype(str).str.contains(search, case=False, na=False)
        if 'NEW HSN 8' in df.columns:
            mask |= df['NEW HSN 8'].astype(str).str.contains(search, case=False, na=False)
        filtered_df = df[mask]
    else:
        filtered_df = df

    # --- Metrics Section ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Items", len(filtered_df))
    
    if 'STOCK' in filtered_df.columns:
        out_of_stock = len(filtered_df[filtered_df['STOCK'] <= 0])
        c2.metric("Out of Stock", out_of_stock)
        
        if 'Purchase Rate' in filtered_df.columns:
            total_val = (filtered_df['STOCK'] * filtered_df['Purchase Rate']).sum()
            c3.metric("Stock Value", f"₹{total_val:,.0f}")

    # --- Data Display ---
    # Define columns to show (only if they exist in the file)
    display_cols = ['NAME', 'STOCK', 'Purchase Rate', 'Last Sale Rate', 'NEW HSN 8', 'Margin']
    existing_cols = [c for c in display_cols if c in filtered_df.columns]
    
    st.dataframe(filtered_df[existing_cols], use_container_width=True, hide_index=True)

else:
    st.warning("Waiting for data... Please check your GitHub filename.")import streamlit as st
import pandas as pd

# 1. SETTINGS - Filename updated as requested
DATA_FILENAME = "SUE STOCK PRICE.csv"

@st.cache_data
def load_data():
    try:
        # Loading with 'latin1' to handle special characters and skipping bad rows
        df = pd.read_csv(DATA_FILENAME, encoding='latin1', on_bad_lines='skip')
        
        # Clean up column names
        df.columns = [str(c).strip() for c in df.columns]
        
        # Convert numeric columns safely
        cols_to_fix = ['STOCK', 'Purchase Rate', 'Last Sale Rate', 'MRP', 'Margin']
        for col in cols_to_fix:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    except FileNotFoundError:
        st.error(f"❌ Could not find the file: {DATA_FILENAME}")
        st.info("Please ensure your file on GitHub is named exactly 'SUE STOCK PRICE.csv' (case sensitive).")
        return None
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None

# --- APP LAYOUT ---
st.set_page_config(page_title="SUE Inventory", layout="wide")
st.title("📊 Shree Umiya Electricals")

df = load_data()

if df is not None:
    # --- Search Bar ---
    search = st.text_input("🔍 Search by Item Name or HSN Code")

    # --- Filtering Logic ---
    if search:
        # Search in Name and HSN column
        mask = df['NAME'].astype(str).str.contains(search, case=False, na=False)
        if 'NEW HSN 8' in df.columns:
            mask |= df['NEW HSN 8'].astype(str).str.contains(search, case=False, na=False)
        filtered_df = df[mask]
    else:
        filtered_df = df

    # --- Metrics Section ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Items", len(filtered_df))
    
    if 'STOCK' in filtered_df.columns:
        out_of_stock = len(filtered_df[filtered_df['STOCK'] <= 0])
        c2.metric("Out of Stock", out_of_stock)
        
        if 'Purchase Rate' in filtered_df.columns:
            total_val = (filtered_df['STOCK'] * filtered_df['Purchase Rate']).sum()
            c3.metric("Stock Value", f"₹{total_val:,.0f}")

    # --- Data Display ---
    # Define columns to show (only if they exist in the file)
    display_cols = ['NAME', 'STOCK', 'Purchase Rate', 'Last Sale Rate', 'NEW HSN 8', 'Margin']
    existing_cols = [c for c in display_cols if c in filtered_df.columns]
    
    st.dataframe(filtered_df[existing_cols], use_container_width=True, hide_index=True)

else:
    st.warning("Waiting for data... Please check your GitHub filename.")
