import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard")

df=pd.read_csv("nsalesdata.csv")
st.sidebar.header("Please Filter Here:")
country=st.sidebar.multiselect(
    "Select the Country:",
    options=df["COUNTRY"].unique(),
    default=df["COUNTRY"].unique()
)
city=st.sidebar.multiselect(
    "Select the City:",
    options=df["CITY"].unique(),
    default=df["CITY"].unique()
)
postalcode=st.sidebar.multiselect(
    "Select the Postal Code:",
    options=df["POSTALCODE"].unique(),
    default=df["POSTALCODE"].unique()
)

df_selection=df.query(
    "CITY==@city & COUNTRY==@country & POSTALCODE==@postalcode"
)
st.title("Sales Dashboard")
st.markdown("##")

total_sales=int(df_selection["SALES"].sum())
average_rating=round(df_selection["QUANTITYORDERED"].mean(),1)
average_sales_by_transaction=round(df_selection["SALES"].mean(),2)

left_column,middle_column,right_column=st.columns(3)
with left_column:
    st.subheader("Total Sales")
    st.subheader(f"US $ {total_sales:}")

with right_column:
    st.subheader("Average Sales Per Transcation:")
    st.subheader(f"US $ {average_sales_by_transaction}")
sales_by_product_line=(df_selection.groupby(by=["PRODUCTLINE"]).sum()[["SALES"]])

fig_product_sales=px.bar(
    sales_by_product_line,
    x="SALES",
    y=sales_by_product_line.index,
    title="Sales by Product Line",
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)
st.plotly_chart(fig_product_sales)
