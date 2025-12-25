import streamlit as st
import pandas as pd

# 1. SETTINGS
DATA_FILENAME = "SUE STOCK PRICE.csv"

@st.cache_data
def load_data():
    try:
        # Load the file using the robust Python engine
        df = pd.read_csv(DATA_FILENAME, encoding='latin1', engine='python', on_bad_lines='skip')
        
        # --- ROBUST HEADER DETECTION ---
        # If 'NAME' isn't a column, the table might start further down
        if 'NAME' not in [str(c).strip().upper() for c in df.columns]:
            # Look through the first 20 rows to find where the actual data starts
            for i in range(min(len(df), 20)):
                row_values = [str(val).strip().upper() for val in df.iloc[i].values]
                if 'NAME' in row_values or 'PARTICULARS' in row_values:
                    # Found the header! Reset the dataframe from this point
                    df.columns = df.iloc[i]
                    df = df.iloc[i+1:].reset_index(drop=True)
                    break

        # Clean up column names (strip spaces and make uppercase for matching)
        df.columns = [str(c).strip() for c in df.columns]
        
        # If the column is called 'Particulars' (common in Tally exports), rename it to 'NAME'
        if 'Particulars' in df.columns and 'NAME' not in df.columns:
            df = df.rename(columns={'Particulars': 'NAME'})

        # Remove any rows where NAME is empty (removes footer rows)
        if 'NAME' in df.columns:
            df = df[df['NAME'].notna()]
        
        # Convert numbers correctly
        for col in ['STOCK', 'Purchase Rate', 'Last Sale Rate', 'Quantity', 'Rate']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # If the file uses 'Quantity' instead of 'STOCK', rename it
        if 'Quantity' in df.columns and 'STOCK' not in df.columns:
            df = df.rename(columns={'Quantity': 'STOCK'})
        if 'Rate' in df.columns and 'Last Sale Rate' not in df.columns:
            df = df.rename(columns={'Rate': 'Last Sale Rate'})

        return df
    except Exception as e:
        st.error(f"❌ Data Error: {e}")
        return None

# --- APP LAYOUT ---
st.set_page_config(page_title="SUE Inventory", layout="wide")
st.title("📊 Shree Umiya Electricals")

df = load_data()

if df is not None and not df.empty:
    # Check if we actually found the NAME column
    if 'NAME' in df.columns:
        search = st.text_input("🔍 Search Item Name (e.g. Pump, Motor, Cable)")

        if search:
            filtered_df = df[df['NAME'].astype(str).str.contains(search, case=False, na=False)]
        else:
            filtered_df = df

        # Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Items Found", len(filtered_df))
        
        if 'STOCK' in filtered_df.columns:
            c2.metric("Out of Stock", len(filtered_df[filtered_df['STOCK'] <= 0]))
            
            if 'Purchase Rate' in filtered_df.columns:
                val = (filtered_df['STOCK'] * filtered_df['Purchase Rate']).sum()
                c3.metric("Stock Value", f"₹{val:,.0f}")

        # Final Table
        show_cols = ['NAME', 'STOCK', 'Purchase Rate', 'Last Sale Rate', 'NEW HSN 8']
        existing = [c for c in show_cols if c in filtered_df.columns]
        st.dataframe(filtered_df[existing], use_container_width=True, hide_index=True)
    else:
        st.error("Could not find a 'NAME' or 'Particulars' column in your file.")
        st.write("Columns found in your file:", list(df.columns))
else:
    st.info("Please verify your CSV file content and filename on GitHub.")
