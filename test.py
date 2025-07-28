import streamlit as st
import pandas as pd

# Load the Excel file and clean column names
@st.cache_data
def load_data():
    df = pd.read_excel("VendorData.xlsx")
    df.columns = df.columns.str.strip()  # Clean column names (remove extra spaces)
    return df

df = load_data()

st.title("📊 Vendor Data Agent")

# Search by ID
search_id = st.number_input("Enter ID to search", min_value=0, step=1, key="search_id_input")
if st.button("Search by ID"):
    result = df[df['id'] == search_id]
    if not result.empty:
        st.success(f"Found {len(result)} record(s) for ID {search_id}")
        st.dataframe(result)
    else:
        st.warning("No data found for that ID.")

# Filter options
st.subheader("🔍 Filter Data")
country = st.selectbox("Country", ["All"] + sorted(df['Country'].unique()), key="country_filter")
product = st.selectbox("Product", ["All"] + sorted(df['Product'].unique()), key="product_filter")
segment = st.selectbox("Segment", ["All"] + sorted(df['Segment'].unique()), key="segment_filter")

filtered_df = df.copy()
if country != "All":
    filtered_df = filtered_df[filtered_df['Country'] == country]
if product != "All":
    filtered_df = filtered_df[filtered_df['Product'] == product]
if segment != "All":
    filtered_df = filtered_df[filtered_df['Segment'] == segment]

st.write(f"Showing {len(filtered_df)} records after filter")
st.dataframe(filtered_df)

# Summary
st.subheader("📈 Summary")
if st.button("Show Total Profit by Product"):
    summary = filtered_df.groupby("Product")["Profit"].sum().sort_values(ascending=False)
    st.bar_chart(summary)

# Export
if st.button("Export Filtered Data"):
    filtered_df.to_csv("filtered_vendor_data.csv", index=False)
    st.success("Exported as filtered_vendor_data.csv")
