import streamlit as st
import pandas as pd
import sqlite3

# Page Configuration
st.set_page_config(page_title="RetailMart Insights Dashboard", layout="wide")
st.title("📊 RetailMart Executive Sales Dashboard")
st.markdown("Real-time operational metrics fetched from `retail_mart.db`")

# Connect to database
conn = sqlite3.connect('retail_mart.db')

# 1. Fetch Key Performance Indicators (KPIs)
df_all = pd.read_sql_query("SELECT * FROM retail_sales", conn)
total_revenue = df_all['total_revenue'].sum()
total_transactions = len(df_all)
avg_transaction = df_all['total_revenue'].mean()

# Display KPIs in 3 clean columns
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"INR {total_revenue:,.2f}")
col2.metric("Total Transactions", f"{total_transactions}")
col3.metric("Average Basket Value", f"INR {avg_transaction:,.2f}")

st.markdown("---")

# 2. Charts Section
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("🏙️ Total Revenue Generated Per City")
    city_df = pd.read_sql_query(
        "SELECT city, SUM(total_revenue) as Revenue FROM retail_sales GROUP BY city ORDER BY Revenue DESC", conn
    )
    st.bar_chart(data=city_df, x="city", y="Revenue")

with right_col:
    st.subheader("📦 Top Best-Selling Products")
    prod_df = pd.read_sql_query(
        "SELECT product_name, SUM(quantity) as Quantity FROM retail_sales GROUP BY product_name", conn
    )
    st.bar_chart(data=prod_df, x="product_name", y="Quantity")

# 3. Raw Data View
st.subheader("📋 Look Inside the Database Records")
st.dataframe(df_all)

conn.close()