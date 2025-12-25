import streamlit as st
import pandas as pd

# The rest of your code should come AFTER the imports
@st.cache_data
def load_data():
    # ... your existing code ...
@st.cache_data
def load_data():
    try:
        # We added encoding='latin1' here to handle special characters
        df = pd.read_csv(DATA_FILENAME, encoding='latin1')
        
        # Clean column names (removes hidden spaces)
        df.columns = df.columns.str.strip()
        
        # Basic Data Cleaning
        if 'STOCK' in df.columns:
            df['STOCK'] = pd.to_numeric(df['STOCK'], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
        return None
