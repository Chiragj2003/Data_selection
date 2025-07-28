import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

# --- Database Configuration ---
DB_URL = (
    "postgresql://neondb_owner:npg_98qZtiaRWBKN@"
    "ep-ancient-morning-a1t0645z-pooler.ap-southeast-1.aws.neon.tech/"
    "neondb?sslmode=require&channel_binding=require"
)

# --- Load data from NeonDB PostgreSQL ---
@st.cache_data
def load_data():
    engine = create_engine(DB_URL)

    try:
        # Use quoted table name for case-sensitive PostgreSQL access
        df = pd.read_sql('SELECT * FROM "VendorData"', engine)
        df.columns = df.columns.str.strip()
        if 'id' in df.columns:
            df['id'] = df['id'].astype(str).str.strip()
        return df
    except ProgrammingError as e:
        st.error("❌ Error: Table 'VendorData' not found in database. Please check table name and casing.")
        st.stop()

# --- Main Application ---
st.title("📊 Vendor Data Agent")

# --- Load data ---
df = load_data()

# --- Search by ID ---
search_id = st.text_input("🔎 Enter ID to search", key="search_id_input")

if st.button("Search by ID"):
    result = df[df['id'] == search_id.strip()]
    if not result.empty:
        st.success(f"✅ Found {len(result)} record(s) for ID {search_id}")
        st.dataframe(result)
    else:
        st.warning("⚠️ No data found for that ID.")

# --- Filter Section ---
st.subheader("🔍 Filter Data")

country_options = ["All"] + sorted(df['Country'].dropna().unique()) if 'Country' in df.columns else []
product_options = ["All"] + sorted(df['Product'].dropna().unique()) if 'Product' in df.columns else []
segment_options = ["All"] + sorted(df['Segment'].dropna().unique()) if 'Segment' in df.columns else []

country = st.selectbox("Country", country_options, key="country_filter")
product = st.selectbox("Product", product_options, key="product_filter")
segment = st.selectbox("Segment", segment_options, key="segment_filter")

# --- Apply Filters ---
filtered_df = df.copy()
if country != "All":
    filtered_df = filtered_df[filtered_df['Country'] == country]
if product != "All":
    filtered_df = filtered_df[filtered_df['Product'] == product]
if segment != "All":
    filtered_df = filtered_df[filtered_df['Segment'] == segment]

# --- Display Filtered Data ---
st.write(f"Showing {len(filtered_df)} record(s) after filtering:")
st.dataframe(filtered_df)

# --- Export Filtered Data ---
if st.button("Export Filtered Data"):
    filtered_df.to_csv("filtered_vendor_data.csv", index=False)
    st.success("✅ Exported as 'filtered_vendor_data.csv'")
