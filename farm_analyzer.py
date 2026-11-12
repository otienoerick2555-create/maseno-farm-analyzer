import streamlit as st
import pandas as pd

st.set_page_config(page_title="Farm Yield Analyzer", page_icon="🌾", layout="wide")
st.title("🌾 Agricultural Yield Analyzer")
st.write("A data science tool for tracking farmer productivity and crop yields.")

try:
    df = pd.read_csv("farm_data.csv")
    
    st.sidebar.header("Filter Data")
    selected_crop = st.sidebar.selectbox("Select a Crop:", ["All"] + list(df['Crop'].unique()))
    
    if selected_crop != "All":
        filtered_df = df[df['Crop'] == selected_crop]
    else:
        filtered_df = df

    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    total_acres = filtered_df['Acres_Planted'].sum()
    total_yield = filtered_df['Yield_Kg'].sum()
    avg_yield_per_acre = total_yield / total_acres if total_acres > 0 else 0
    
    col1.metric("Total Acres Planted", f"{total_acres:,.1f} Acres")
    col2.metric("Total Yield", f"{total_yield:,.0f} Kg")
    col3.metric("Avg Yield per Acre", f"{avg_yield_per_acre:,.1f} Kg/Acre")

    st.divider()

    st.subheader("Yield by Farmer")
    farmer_yield = filtered_df.groupby('Farmer_Name')['Yield_Kg'].sum().sort_values(ascending=False)
    st.bar_chart(farmer_yield)

    st.divider()

    st.subheader("Raw Survey Data")
    st.dataframe(filtered_df, use_container_width=True)

except FileNotFoundError:
    st.error("Error: Could not find 'farm_data.csv'. Make sure it is uploaded.")
