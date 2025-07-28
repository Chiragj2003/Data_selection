import streamlit as st
import pandas as pd
import pyodbc

# --- Load data from SQL Server ---
@st.cache_data
def load_data():
    # Connect to SQL Server
    conn = pyodbc.connect(
        r'DRIVER={SQL Server};SERVER=OMEN\SQLEXPRESS;DATABASE=VendorDB;Trusted_Connection=yes;'
    )
    query = "SELECT * FROM VendorData"
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Clean column names and values
    df.columns = df.columns.str.strip()
    if 'id' in df.columns:
        df['id'] = df['id'].astype(str).str.strip()
    return df

# --- Load and prepare data ---
df = load_data()

st.title("📊 Vendor Data Agent")

# --- Search by ID ---
search_id = st.text_input("🔎 Enter ID to search", key="search_id_input")  # use text_input for flexibility

if st.button("Search by ID"):
    result = df[df['id'] == search_id.strip()]
    if not result.empty:
        st.success(f"✅ Found {len(result)} record(s) for ID {search_id}")
        st.dataframe(result)
    else:
        st.warning("⚠️ No data found for that ID.")

# --- Filter options ---
st.subheader("🔍 Filter Data")

# Handle missing columns safely
country_options = ["All"] + sorted(df['Country'].dropna().unique()) if 'Country' in df.columns else []
product_options = ["All"] + sorted(df['Product'].dropna().unique()) if 'Product' in df.columns else []
segment_options = ["All"] + sorted(df['Segment'].dropna().unique()) if 'Segment' in df.columns else []

country = st.selectbox("Country", country_options, key="country_filter")
product = st.selectbox("Product", product_options, key="product_filter")
segment = st.selectbox("Segment", segment_options, key="segment_filter")

# Apply filters
filtered_df = df.copy()
if country != "All" and 'Country' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Country'] == country]
if product != "All" and 'Product' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Product'] == product]
if segment != "All" and 'Segment' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Segment'] == segment]

# Display filtered data
st.write(f"Showing {len(filtered_df)} record(s) after filtering:")
st.dataframe(filtered_df)

# --- Summary Chart ---
st.subheader("📈 Summary")

# --- Export to CSV ---
if st.button("Export Filtered Data"):
    filtered_df.to_csv("filtered_vendor_data.csv", index=False)
    st.success("✅ Exported as 'filtered_vendor_data.csv'")
