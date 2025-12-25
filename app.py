import streamlit as st
import pandas as pd

# 1. SETTINGS
DATA_FILENAME = "SUE STOCK PRICE.csv"

@st.cache_data
def load_data():
    try:
        # Load file with high-compatibility settings
        df = pd.read_csv(DATA_FILENAME, encoding='latin1', engine='python', on_bad_lines='skip')
        
        # List of possible names for the product column
        target_cols = ['NAME', 'PARTICULARS', 'ITEM NAME', 'ITEM', 'DESCRIPTION', 'PRODUCT']
        
        # Function to check if a row/header contains any of our target names
        def find_header_in_list(col_list):
            col_list_clean = [str(c).strip().upper() for c in col_list]
            for target in target_cols:
                if target in col_list_clean:
                    return True, target
            return False, None

        # Check if the current header is correct
        is_found, found_name = find_header_in_list(df.columns)

        # If not found, search the first 25 rows for a header
        if not is_found:
            for i in range(min(len(df), 25)):
                row_values = df.iloc[i].values
                is_found, found_name = find_header_in_list(row_values)
                if is_found:
                    df.columns = row_values
                    df = df.iloc[i+1:].reset_index(drop=True)
                    break

        # Final Cleanup of column names
        df.columns = [str(c).strip() for c in df.columns]
        
        # Standardize the Name column to 'NAME'
        for target in target_cols:
            matching_col = next((c for c in df.columns if c.strip().upper() == target), None)
            if matching_col:
                df = df.rename(columns={matching_col: 'NAME'})
                break

        # Remove empty rows or footer rows
        if 'NAME' in df.columns:
            df = df[df['NAME'].notna()]
            df['NAME'] = df['NAME'].astype(str)
        
        # Convert numbers (Stock, Rate, etc.)
        num_cols = ['STOCK', 'Purchase Rate', 'Last Sale Rate', 'Quantity', 'Rate', 'MRP']
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            # Handle common variations
            if col == 'Quantity' and 'STOCK' not in df.columns:
                df = df.rename(columns={'Quantity': 'STOCK'})
            if col == 'Rate' and 'Last Sale Rate' not in df.columns:
                df = df.rename(columns={'Rate': 'Last Sale Rate'})

        return df
    except Exception as e:
        st.error(f"❌ Error Reading File: {e}")
        return None

# --- APP INTERFACE ---
st.set_page_config(page_title="SUE Inventory", layout="wide")
st.title("📊 Shree Umiya Electricals")

df = load_data()

if df is not None and not df.empty:
    if 'NAME' in df.columns:
        search = st.text_input("🔍 Search Item Name (e.g. Pump, Motor, Cable)")

        filtered_df = df[df['NAME'].str.contains(search, case=False, na=False)] if search else df

        # Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Items Found", len(filtered_df))
        
        if 'STOCK' in filtered_df.columns:
            out_of_stock = len(filtered_df[filtered_df['STOCK'] <= 0])
            c2.metric("Out of Stock", out_of_stock)
            
            if 'Purchase Rate' in filtered_df.columns:
                total_val = (filtered_df['STOCK'] * filtered_df['Purchase Rate']).sum()
                c3.metric("Stock Value", f"₹{total_val:,.0f}")

        # Table Display
        main_cols = ['NAME', 'STOCK', 'Purchase Rate', 'Last Sale Rate', 'NEW HSN 8']
        available_cols = [c for c in main_cols if c in filtered_df.columns]
        st.dataframe(filtered_df[available_cols], use_container_width=True, hide_index=True)
    else:
        st.error("⚠️ Could not identify the Product Name column.")
        st.write("Please check your Excel file. The product list should have a heading like 'NAME', 'Item Name', or 'Particulars'.")
        st.write("Current columns found:", list(df.columns))
else:
    st.info("Loading your 'SUE STOCK PRICE.csv' file from GitHub...")
