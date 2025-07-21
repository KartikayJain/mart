import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page configuration for a wide layout
st.set_page_config(layout="wide")

# Load the dataset
# Ensure the 'Mart.csv' file is in the same directory as your script.
try:
    df = pd.read_csv('Mart.csv')
except FileNotFoundError:
    st.error("The 'Mart.csv' file was not found. Please make sure it's in the correct directory.")
    st.stop() # Stop the app if the file is not found

# --- UI Elements ---

# Display the main title for the dashboard
st.title("K-Mart Dashboard")

# Create a multiselect dropdown for categories
# This allows the user to select one or more categories to view.
selected_categories = st.multiselect(
    'Please select a category',
    options=df['category'].unique(),
    default=df['category'].unique() # By default, all categories are selected
)

# --- Data Filtering and Chart Generation ---

# Check if the user has selected any categories
if not selected_categories:
    st.warning("Please select at least one category to see the charts.")
else:
    # Filter the DataFrame based on the user's selection
    filtered_df = df[df['category'].isin(selected_categories)]

    # Create three columns to display the charts side-by-side
    col1, col2, col3 = st.columns(3)

    # --- Chart 1: Sales by Subcategory (Bar Chart) ---
    with col1:
        st.subheader("Sales by Subcategory")
        fig_sales = px.bar(
            filtered_df,
            x='subcategory',
            y='sales',
            text_auto='.2s', # Format text on bars
            color_discrete_sequence=['#FF4B4B'] # Use a red color
        )
        fig_sales.update_traces(textposition='outside')
        fig_sales.update_layout(
            yaxis_title='Total Sales',
            xaxis_title='Subcategory',
            uniformtext_minsize=8,
            uniformtext_mode='hide'
        )
        # Use container_width to make the chart responsive to the column size
        st.plotly_chart(fig_sales, use_container_width=True)

    # --- Chart 2: Profit by Subcategory (Pie Chart) ---
    with col2:
        st.subheader("Profit by Subcategory")
        fig_profit = px.pie(
            filtered_df,
            values='profit',
            names='subcategory',
            hole=0.3 # Create a donut chart effect
        )
        fig_profit.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_profit, use_container_width=True)

    # --- Chart 3: Discount Distribution (Sunburst Chart) ---
    with col3:
        st.subheader("Discount Distribution")
        fig_discount = px.sunburst(
            filtered_df,
            path=["category", "subcategory"],
            values='discount'
        )
        st.plotly_chart(fig_discount, use_container_width=True)

