#created by Rajarshi Maity
#19th June, 2023
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import yfinance as yf
from plotly.subplots import make_subplots
import folium
import plotly.express as px
from streamlit_folium import st_folium
from yahooquery import Ticker as TT
from streamlit_option_menu import option_menu
from streamlit_card import card
from googlesearch import search
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from GoogleNews import GoogleNews
from PIL import Image

# Set page layout
st.set_page_config(layout="wide")

# Set sidebar width and style
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        width: 280px;
        background-color: #f8f9fa;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        color: black;  /* Set sidebar text color to black */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set main content width and style
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 1200px;
        margin: 20px auto;
        background-color: #ffffff;
        padding: 100px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        color: black !important;  /* Set main content text color to black */
    }
    
    /* Set heading color to black and bold */
    .main .block-container h1, .main .block-container h2, .main .block-container h3, .main .block-container h4, .main .block-container h5, .main .block-container h6 {
        color: black;
        font-weight: bold;
    }
      
      
    /* Set metric header color to black */
    .main .block-container .stMetric > div:nth-child(1) {
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Create a sidebar panel for options
st.sidebar.title("Choose the Ticker")
reit_symbol = st.sidebar.text_input("Enter the REIT symbol:",value="PLD")
time_range = st.sidebar.selectbox("Choose the time range", ("1d", "5d", "1w", "1mo", "1y", "5y", "max"))

end_date = datetime.today()
if time_range == "1d":
    start_date = end_date - pd.DateOffset(days=1)
elif time_range == "5d":
    start_date = end_date - pd.DateOffset(days=5)
elif time_range == "1w":
    start_date = end_date - pd.DateOffset(weeks=1)
elif time_range == "1mo":
    start_date = end_date - pd.DateOffset(months=1)
elif time_range == "1y":
    start_date = end_date - pd.DateOffset(years=1)
elif time_range == "5y":
    start_date = end_date - pd.DateOffset(years=5)
else:
    start_date = "2010-01-01"  # Default to start from the beginning

# Yahoo Finance
reit_data = yf.download(reit_symbol, start=start_date, end=end_date)
reit_ticker = yf.Ticker(reit_symbol)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.2, row_heights=[0.7, 0.3])

# Add the stock price 
fig.add_trace(go.Candlestick(x=reit_data.index,
                             open=reit_data['Open'],
                             high=reit_data['High'],
                             low=reit_data['Low'],
                             close=reit_data['Close'],
                             name='Price'),
              row=1, col=1)

# Add the volume trace
fig.add_trace(go.Bar(x=reit_data.index,
                     y=reit_data['Volume'],
                     name='Volume'),
              row=2, col=1)

# Update layout settings
fig.update_layout(title=f"{reit_symbol} Stock Price and Volume",
                  hovermode='x',
                  legend=dict(x=0.02, y=0.95),
                  height=600)


fig.update_yaxes(title_text='Price', row=1, col=1)
fig.update_yaxes(title_text='Volume', row=2, col=1)
fig.update_xaxes(title_text="Date")


reit = yf.Ticker(reit_symbol)
reit_info = reit.info

# Display the REIT information
st.title(reit_info['longName'] + "  -  " + reit_symbol)
#st.markdown("---")
st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)


# Display plot
st.plotly_chart(fig)

# Display the REIT information
st.title("REIT Information")
st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

# Company Info
st.header("Company Info")
st.subheader("General")
col1, col2 = st.columns(2)
with col1:
    st.write("Industry:", reit_info.get('industry', 'N/A'))
    st.write("Sector:", reit_info.get('sector', 'N/A'))
    st.write("Website:", f"{reit_info.get('website', '')}")
    st.write("Company:", reit_info.get('longName', 'N/A'))
with col2:
    st.write("Address:", reit_info.get('address1', 'N/A'))
    st.write("City:", reit_info.get('city', 'N/A'))
    st.write("State:", reit_info.get('state', 'N/A'))
    st.write("Country:", reit_info.get('country', 'N/A'))

st.subheader("Description")
st.write(reit_info.get('longBusinessSummary', 'N/A'))

# Financial Data
st.header("Financial Data")
col1, col2, col3 = st.columns(3)
with col1:
    #st.write("<h3 style='color: black; '>Market Cap</h3>", unsafe_allow_html=True)
    st.markdown("<div style='background-color: 	#383838; border-radius: 10px; padding: 10px 20px; box-shadow: 2px 2px 5px 0px rgba(0,0,0,0.3); text-align: center;'>"
                "<h3 style='color: white;'>Market Cap</h3>"
                "<p style='font-size: 20px; color:white; font-weight: normal;'>"
                f"${reit_info.get('marketCap', 'N/A'):,}"
                "</div>", unsafe_allow_html=True)
with col2:
    #st.write("<h3 style='color: black;'>Total Revenue</h3>", unsafe_allow_html=True)
    #st.metric(" ", f"${reit_info.get('totalRevenue', 'N/A'):,}")
    st.markdown("<div style='background-color: #383838; border-radius: 10px; padding: 10px 20px; box-shadow: 2px 2px 5px 0px rgba(0,0,0,0.3); text-align: center;'>"
                "<h3 style='color: white;'>Total Revenue</h3>"
                "<p style='font-size: 20px; color:white; font-weight: normal;'>"
                f"${reit_info.get('totalRevenue', 'N/A'):,}"
                "</div>", unsafe_allow_html=True)
with col3:
    #st.write("<h3 style='color: black;'>Income</h3>", unsafe_allow_html=True)
    #st.metric(" ", f"${reit_info.get('netIncomeToCommon', 'N/A'):,}")
    st.markdown("<div style='background-color: #383838; border-radius: 10px; padding: 10px 20px; box-shadow: 2px 2px 5px 0px rgba(0,0,0,0.3); text-align: center;'>"
            "<h3 style='color: white;'>Net Income</h3>"
            "<p style='font-size: 20px; color:white; font-weight: normal;'>"
            f"${reit_info.get('netIncomeToCommon', 'N/A'):,}"
            "</p>"
            "</div>", unsafe_allow_html=True)


#Statistics
st.header("Statistics")
col1, col2, col3 = st.columns(3)
with col1:
    #dividend_yield = reit_info['dividendYield']
    st.markdown("<div style='background-color: lightgrey; border-radius: 10px; padding: 10px 20px; margin-bottom: 20px; box-shadow: 2px 2px 5px 0px rgba(0,0,0,0.3); text-align: center;'>"
            "<h3 style='color: black;'>Dividend Yield</h3>"
            "<p style='font-size: 20px; font-weight: normal;'>"
            f"{reit_info.get('dividendYield', 'N/A')}"
            "</p>"
            "</div>", unsafe_allow_html=True)

    st.markdown("<div style='background-color: lightgrey; border-radius: 10px; padding: 10px 20px; margin-bottom: 20px; box-shadow: 2px 2px 5px 0px rgba(0,0,0,0.3); text-align: center;'>"
            "<h3 style='color: black;'>5Yr Avg Dividend Yield</h3>"
            "<p style='font-size: 20px; font-weight: normal;'>"
            f"{reit_info.get('fiveYearAvgDividendYield', 'N/A')}"
            "</p>"
            "</div>", unsafe_allow_html=True)

with col2:
    #st.write("<h3 style='color: black;'>Trailing P/E Ratio</h3>", unsafe_allow_html=True)
    #st.metric(" ", reit_info.get('trailingPE', 'N/A'))
    st.markdown("<div style='background-color: lightgrey; border-radius: 10px; padding: 10px 20px; margin-bottom: 20px; box-shadow: 2px 2px 5px 0px rgba(0,0,0,0.3); text-align: center;'>"
            "<h3 style='color: black;'>Trailing PE Ratio</h3>"
            "<p style='font-size: 20px; font-weight: normal;'>"
            f"{reit_info.get('trailingPE', 'N/A')}"
            "</p>"
            "</div>", unsafe_allow_html=True)



    #st.write("<h3 style='color: black;'>Forward P/E Ratio</h3>", unsafe_allow_html=True)
    #st.metric(" ", reit_info.get('forwardPE', 'N/A'))
    st.markdown("<div style='background-color: lightgrey; border-radius: 10px; padding: 10px 20px; margin-bottom: 20px; box-shadow: 2px 2px 5px 0px rgba(0,0,0,0.3); text-align: center;'>"
            "<h3 style='color: black;'>Forward PE</h3>"
            "<p style='font-size: 20px; font-weight: normal;'>"
            f"{reit_info.get('forwardPE', 'N/A')}"
            "</p>"
            "</div>", unsafe_allow_html=True)
    
with col3:
    #st.write("<h3 style='color: black;'>Beta</h3>", unsafe_allow_html=True)
    #st.metric(" ", reit_info.get('beta', 'N/A'))
    st.markdown("<div style='background-color: lightgrey; border-radius: 10px; padding: 10px 20px; margin-bottom: 20px; box-shadow: 2px 2px 5px 0px rgba(0,0,0,0.3); text-align: center;'>"
            "<h3 style='color: black;'>Beta</h3>"
            "<p style='font-size: 20px; font-weight: normal;'>"
            f"{reit_info.get('beta', 'N/A')}"
            "</p>"
            "</div>", unsafe_allow_html=True)



# Page title
st.title("Geographical Diversification"+"- Vornado")
st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)




# Import the address data
df = pd.read_csv("Untitled spreadsheet - Sheet1.csv")

# Create a map centered on the first location
center_lat, center_lng = df['Latitude'].iloc[0], df['Longitude'].iloc[0]
map = folium.Map(location=[center_lat, center_lng], zoom_start=12, width=1000)

# Add markers for each property
for _, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['Property Name'],
        tooltip=row['Property Type'],
        icon=folium.Icon(color='red')
    ).add_to(map)

# Display the map using Streamlit
st_data = st_folium(map, width=1000, height=500)


# Page title
st.title("Top 10 Tenants - Vornado")
st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
st.write("Data is incomplete. Only the data for Vornado is available currently. We will be updating our dataset soon.")

# Import the top 10 tenants data
df_top10 = pd.read_csv("Top10Tenants - Sheet1.csv")

# Convert Square Footage to numeric
df_top10['Square Footage'] = df_top10['Square Footage'].str.replace(',', '').astype(int)

# Calculate the sizes for the treemap
sizes = df_top10['Square Footage'].values

colors = px.colors.qualitative.Dark24[:len(df_top10)]

# Create the treemap figure
fig = go.Figure(go.Treemap(
    labels=df_top10['Tenant'],
    parents=["" for _ in df_top10['Tenant']],
    values=df_top10['Square Footage'],
    marker=dict(colors=colors),
    texttemplate='%{label}',
    textposition="middle center"
))

# Update the layout
fig.update_layout(margin=dict(t=10, l=0, r=0, b=0))

# Display the interactive plot using Streamlit
st.plotly_chart(fig)

# Create a sidebar panel for options
st.sidebar.title("Financial Data")
data_option = st.sidebar.selectbox("Choose the table to display", (
    "Company Officers",
    "Earning History",
    "Grading History",
    "Insider Holders",
    "Insider Transactions",
    "Institution Ownership",
    "Recommendation Trend",
    "SEC Filings",
    "Fund Ownership",
    "Major Holders",
    "Earnings Trend",
    "Balance Sheet",
    "Cash Flow",
    "Income Statement"
))

# Retrieve data based on the selected option
ticker = TT(reit_symbol)

if data_option == "Company Officers":
    data = ticker.company_officers
elif data_option == "Earning History":
    data = ticker.earning_history
elif data_option == "Grading History":
    data = ticker.grading_history
elif data_option == "Insider Holders":
    data = ticker.insider_holders
elif data_option == "Insider Transactions":
    data = ticker.insider_transactions
elif data_option == "Institution Ownership":
    data = ticker.institution_ownership
elif data_option == "Recommendation Trend":
    data = ticker.recommendation_trend
elif data_option == "SEC Filings":
    data = ticker.sec_filings
elif data_option == "Fund Ownership":
    data = ticker.fund_ownership
elif data_option == "Major Holders":
    data = ticker.major_holders
elif data_option == "Earnings Trend":
    data = ticker.earnings_trend
elif data_option == "Balance Sheet":
    data = ticker.balance_sheet()
elif data_option == "Cash Flow":
    data = ticker.cash_flow()
elif data_option == "Income Statement":
    data = ticker.income_statement()

# Page title
st.title("Financial Data - "+reit_info['longName'] + "  -  " + reit_symbol)
st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)



# Display the data

gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
    data,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=False,
    enable_enterprise_modules=True,
    height=350, 
    width='100%',
    reload_data=False
)

data = grid_response['data']
selected = grid_response['selected_rows'] 
df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

AgGrid(df)


# Page title
st.title("Related News")
st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

data=reit.news
# Set column width
col_width = 400

for item in data:
    st.subheader(item["title"])
    if "thumbnail" in item:
        st.image(item["thumbnail"]["resolutions"][0]["url"], caption=item["publisher"], width=col_width)
    st.write(item["publisher"])
    st.write(f"Read more: [{item['title']}]({item['link']})")
    st.write("Related Tickers:", ", ".join(item["relatedTickers"]))
    st.write("---")

#social media
st.sidebar.write("---")
st.sidebar.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center; height: 30px; background-color: lightgray; border-radius: 10px; margin-bottom: 10px;">
        <p style="font-size: 16px; color: black; font-weight: bold; margin: 0;">Connect with me</p>
    </div>
    """,
    unsafe_allow_html=True
)


st.sidebar.markdown(
    """
    <div style="display: flex; justify-content: center; flex-direction: row; align-items: center;">
        <a href="https://github.com/rajarshimaity3235" target="_blank">
            <img src="https://img.icons8.com/material-rounded/30/ffffff/github.png" alt="GitHub" style="margin-right: 20px; margin-top: 10px;margin-bottom: 10px;" />
        </a>
        <a href="https://www.linkedin.com/in/rajarshi-maity/" target="_blank">
            <img src="https://img.icons8.com/material-rounded/30/ffffff/linkedin.png" alt="LinkedIn" style="margin-right: 20px; margin-top: 10px;margin-bottom: 10px;" />
        </a>
        <a href="mailto:rajarshimaity3235@gmail.com" target="_blank">
            <img src="https://img.icons8.com/material-rounded/30/ffffff/email.png" alt="Email" style="margin-right: 20px; margin-top: 10px;margin-bottom: 10px;" />
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# copyright message
st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <p style="font-size: 12px; color: gray;">
            © 2023 Rajarshi Maity. All rights reserved. This content is for educational purposes only.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
