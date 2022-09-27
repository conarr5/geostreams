
import pandas as pd
import plotly.express as px
import streamlit as st
import openpyxl as op

df = pd.read_excel(
    io = "Dashboard_Data.xlsx",
    engine = "openpyxl",
    sheet_name = "data",
    skiprows = 0,
    usecols = "A:E",
    nrows = 500
)

st.set_page_config(page_title = "Info Dashboard",
                   page_icon = ":bar_chart:")

# --------- SIDEBAR --------- #

st.sidebar.header("Please filter here:")
country = st.sidebar.multiselect(
    "Select Country:",
    options = df["Country"].unique(),
    default = "USA"
)

sector = st.sidebar.multiselect(
    "Select Sector:",
    options = df["Sector"].unique(),
    default = "Agriculture"
)

df_selection = df.query(
    "Country == @country & Sector == @sector"
)

#df = df.astype(str)
#st.dataframe(df_selection)

# --------- MAINPAGE --------- #

st.markdown("<h1 style='text-align: center; color: black;'>- Information Dashboard -</h1>", unsafe_allow_html=True)
st.markdown("##")

# KPI's
total_emissions = int((df_selection["Total_GHG_Emissions"]).sum())

st.markdown("<h2 style='text-align: center; color: grey;'>Selected 2019 CO2 Emission Total (tonnes):</h2>", unsafe_allow_html=True)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    ""
with middle_column:
    st.subheader(f"{total_emissions:,}")
with right_column:
    ""


st.markdown("---")


# Emission Bar chart
emission_by_country = (
    df_selection.groupby(by=["Country"]).sum()[["Total_GHG_Emissions"]].sort_values(by="Total_GHG_Emissions")
)
fig_emissions = px.bar(
    emission_by_country,
    x = "Total_GHG_Emissions",
    y = emission_by_country.index,
    orientation = "h",
    title = "<b>2019 Emissions by Country</b>",
    color_discrete_sequence = ["#339933"] * len(emission_by_country),
    template = "plotly_white"
)
fig_emissions.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False))
)
st.plotly_chart(fig_emissions)


st.markdown("---")


# Emission Pie Chart
emission_by_sector = (
    df_selection.groupby(by=["Sector"]).sum()[["Total_GHG_Emissions"]].sort_values(by="Total_GHG_Emissions")
)
fig_sector = px.pie(
    emission_by_sector,
    hole = 0.9,
    names = emission_by_sector.index,
    values= "Total_GHG_Emissions",
    title = "<b>2019 Emissions by Sector</b>"
)
st.plotly_chart(fig_sector)



# Hide streamlit style
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)






