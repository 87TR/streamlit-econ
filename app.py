import credentials

import streamlit as st

st.set_page_config(
    page_title="87tr",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': "https://87tr.com/contact",
        'Report a bug': "https://87tr.com/contact",
        'About': "@87tr"
    }
)

from streamlit_option_menu import option_menu
import yaml
import bcrypt
from pypages import show_inflation_consumerpriceindex, show_inflation_pcepriceindex, show_consumptionincome_autotrucksales, show_labormarket_unemploymentinsuranceclaims, show_labormarket_employmentsituation, show_labormarket_jobopeningslaborturnoversurvey, show_labormarket_employmentbyindustry

import pandas as pd
from datetime import datetime, timedelta
import time
import requests

st.markdown(
    """
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.16/dist/tailwind.min.css" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
        @import url('https://rsms.me/inter/inter.css');
        p {
            font-family: 'Inter', sans-serif;
            font-size: 14px !important;
            color: #111111;
        }
        h1 {
            font-family: 'Inter', sans-serif;
            font-size: 20px !important;
            color: #111111; !important;
            font-weight: 400 !important;
        }
        h2 {
            font-family: 'Inter', sans-serif;
            font-size: 16px !important;
            color: #111111; !important;
            font-weight: 400 !important;
        }
        h3 {
            font-family: 'Inter', sans-serif;
            font-size: 14px !important;
            color: #111111; !important;
            font-weight: 400 !important;
        }
        h4 {
            font-family: 'Inter', sans-serif;
            font-size: 12px !important;
            color: #111111; !important;
            font-weight: 400 !important;
        }
        h5 {
            font-family: 'Inter', sans-serif;
            font-size: 10px !important;
            color: #111111; !important;
            font-weight: 400 !important;
        }
        h6 {
            font-family: 'Inter', sans-serif;
            font-size: 8px !important;
            color: #111111; !important;
            font-weight: 400 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    .stAlert > div  {
      padding-top: 15px !important;
      padding-bottom: 20px !important;
      padding-left: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <style>
        [data-testid=stSidebar] {
            background-color: #FFFFFF10;
        }
    </style>
    """, unsafe_allow_html=True)

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

def show_login():

    error_placeholder = st.empty()
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        user_details = config['credentials']['usernames'].get(username)
        if not user_details:
            error_placeholder.error("Username not found!", icon="⚠️")
        else:
            stored_password = user_details.get('password')
            entered_password_bytes = password.encode('utf-8')
            stored_password_bytes = stored_password.encode('utf-8')
            
            if bcrypt.checkpw(entered_password_bytes, stored_password_bytes):
                st.session_state["authentication_status"] = True
                st.session_state["username"] = username
                st.session_state["name"] = user_details['name']
                
                st.session_state.page = "Overview"
                st.rerun()
            
            else:
                error_placeholder.error("Incorrect username or password!", icon="⚠️")

def sign_out():
    st.session_state["authentication_status"] = False
    st.rerun()

def clear_cache_except_auth():
    # Save the authentication variables
    auth_keys = ["authentication_status", "username", "name"]
    saved_auth = {key: st.session_state.get(key) for key in auth_keys}

    # Clear the memoized cache
    st.cache_data.clear()

    # Remove all keys except the authentication ones
    for key in list(st.session_state.keys()):
        if key not in auth_keys:
            del st.session_state[key]

    # Restore the authentication variables
    for key, value in saved_auth.items():
        if value is not None:
            st.session_state[key] = value

def main():
    if st.session_state.get("authentication_status"):

        with st.sidebar:

            st.image("https://www.87tr.com/branding/logo/logo.png", width=100)

            welcome_message = f"<h2 style='padding-top: 5px; padding-bottom: 5px;'><b>Welcome, {st.session_state['username']}!</b></h2>"
            st.markdown(welcome_message, unsafe_allow_html=True)
            st.markdown("<h5><b>Internal Use Only:</b> This application is exclusively for the use of 87TR employees. Access by any unauthorized personnel is strictly prohibited. If you are not a designated employee, please close this application immediately.</h5>", unsafe_allow_html=True)

            menu_data = {
                "87TR's Data App": [],
                #"Government Finance": [
                    #"Balance of Payments",
                    #"Credit Ratings",
                    #"Debt Issuance"
                #],
                "Consumption & Income": [
                    "Auto & Truck Sales",
                    #"Personal Consumption Expenditures",
                    #"Personal Income",
                    #"Retail Inventories",
                    #"Retail Inventory Sales Ratio",
                    #"Retail Sales"
                ],
                #"Energy": [
                    #"Weekly Natural Gas Storage",
                    #"Weekly Petroleum Supply"
                #],
                #"Flow of Funds": [
                    #"Balance Sheet Tables",
                    #"Debt & Borrowing Tables",
                    #"Flows Tables Summary",
                    #"Flows Tables by Instrument",
                    #"Flows Tables by Sector",
                    #"Level Tables Summary",
                    #"Level Tables by Instrument",
                    #Level Tables by Sector",
                    #"Supplementary Tables"
                #],
                #"Foreign Trade": [
                    #"Bilateral Trade",
                    #"International Trade"
                #],
                #"Housing & Construction": [
                    #"Case-Shiller Home Price",
                    #"Construction Put in Place",
                    #"Housing Market",
                    #"Housing Vacancy Rates"
                #],
                #"Industry": [
                    #"Capacity Utilization",
                    #"Industrial Capacity",
                    #"Industrial Production",
                    #"Rail Traffic",
                    #"Shipments, Inventories & Orders"
                #],
                "Inflation": [
                    "Consumer Price Index",
                    "PCE Price Indices",
                    #"Employment Cost Index",
                    #"Import & Export Prices",
                    #"Producer Prices"
                ],
                "Labor Market": [
                    "Employment Situation",
                    "Employment by Industry",
                    "Job Openings Labor Turnover Survey",
                    #"Productivity & Costs",
                    "Unemployment Insurance Claims"
                ],
                #"Leading Indicators & Surveys": [
                    #"Business Cycle Indicators",
                    #"Consumer Confidence",
                    #"Institute for Supply Management"
                #],
                #"National Accounts": [
                    #"Domestic Product & Income",
                    #"Foreign Transactions",
                    #"GDP",
                    #"Personal Income & Outlays",
                    #"Receipts & Expenditures",
                    #"Saving & Investment"
                #]
            }

            menu = list(menu_data.keys())
            choice = st.sidebar.radio("Choose a Page:", menu)

            sub_menu = menu_data.get(choice, [])
            if sub_menu:
                sub_choice = st.sidebar.radio(f"Choose an Option:", sub_menu)

            if st.button('Clear Cache'):
                clear_cache_except_auth()

            st.markdown("""---""")
            st.markdown("<h5><b>Data Source:</b> The data used in this application is sourced from Federal Reserve Economic Data (FRED), provided by the Federal Reserve Bank of St. Louis, and is subject to their terms and conditions.</h5>", unsafe_allow_html=True)
            st.markdown("<h5><b>Disclaimer:</b> The information provided here is for informational purposes and should not be used as a basis for investment decisions. This is not professional advice.</h5>", unsafe_allow_html=True)

            if st.button("Sign Out"):
                sign_out()

            st.markdown("<br>", unsafe_allow_html=True)

        def show_overview():
        
            response = requests.get('https://api64.ipify.org?format=json')
            if response.status_code == 200:
                ip_data = response.json()
                public_ip = ip_data['ip']
            else:
                public_ip = "Error: Unable to retrieve IP address"

            st.markdown("<h1><b>Data App Information:</b></h1>", unsafe_allow_html=True)
            st.markdown(f"<h3><b>Software Name:</b> app.py</h>", unsafe_allow_html=True)
            st.markdown(f"<h3><b>Public IP:</b> {public_ip}</h3>", unsafe_allow_html=True)

        if choice == "87TR's Data App":
            show_overview()
        elif sub_choice == "Consumer Price Index":
            show_inflation_consumerpriceindex()
        elif sub_choice == "PCE Price Indices":
            show_inflation_pcepriceindex()
        elif sub_choice == "Auto & Truck Sales": 
            show_consumptionincome_autotrucksales()
        elif sub_choice == "Unemployment Insurance Claims": 
            show_labormarket_unemploymentinsuranceclaims()
        elif sub_choice == "Employment Situation": 
            show_labormarket_employmentsituation()
        elif sub_choice == "Job Openings Labor Turnover Survey": 
            show_labormarket_jobopeningslaborturnoversurvey()
        elif sub_choice == "Employment by Industry": 
            show_labormarket_employmentbyindustry()
    else:
        centered_col = st.columns([1, 1, 1])
        with centered_col[1]: 

            st.image("https://www.87tr.com/branding/logo/logo.png", width=50)
            st.markdown("<h3 style='padding-top: 5px; padding-bottom: 5px;'>[Economy]</h3>", unsafe_allow_html=True)
            st.markdown("<h1 style='padding-top: 5px; padding-bottom: 5px;'><b>Welcome to 87TR's Data App</b></h1>", unsafe_allow_html=True)
            st.markdown("<h3 style='padding-top: 5px; padding-bottom: 5px;'>The application specializes in tracking and analyzing a wide range of economic indicators, providing users with valuable insights into the financial landscape. It offers tools to access and interpret data related to government finance, balance of payments, consumption and income, energy, flow of funds, foreign trade, fund statistics, housing and construction, industry, inflation, labor market, leading indicators, money, banking, credit, and national accounts. This comprehensive platform empowers users to make informed decisions based on real-time economic data.</h3>", unsafe_allow_html=True)
            st.markdown("""<div style="padding-top: 20px; padding-bottom: 20px;"><hr></div>""", unsafe_allow_html=True)

            show_login()

            st.markdown("""<div style="padding-top: 20px; padding-bottom: 20px;"><hr></div>""", unsafe_allow_html=True)
            st.markdown("<h3 style='padding-top: 5px; padding-bottom: 5px;'>If you are a new employee and need access to this data application, please connect with 87TR's Support Desk for assistance.</h3>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()