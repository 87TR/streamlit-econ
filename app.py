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
from pypages import show_page1, show_page2, show_page3, show_page4, show_page5, show_page6, show_page7, show_page8

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

def main():
    if st.session_state.get("authentication_status"):

        with st.sidebar:

            st.image("https://www.87tr.com/branding/logo/logo.png", width=100)
        
            welcome_message = f"<h2 style='padding-top: 5px; padding-bottom: 5px;'><b>Welcome, {st.session_state['username']}!</b></h2>"
            st.markdown(welcome_message, unsafe_allow_html=True)
            st.markdown("<h5><b>Internal Use Only:</b> This application is exclusively for the use of 87TR employees. Access by any unauthorized personnel is strictly prohibited. If you are not a designated employee, please close this application immediately.</h5>", unsafe_allow_html=True)

            menu = ["Overview", "Inflation", "Page 2", "Page 3", "Page 4", "Page 5", "Page 6", "Page 7", "Page 8"]
            choice = st.sidebar.radio("Choose a Page:", menu)
            
            st.markdown("""---""")
            st.markdown("<h5><b>Data Source:</b> The data provided is exclusively owned by FactSet Research Systems Inc. and is provided for use under the terms of a licensing agreement.</h5>", unsafe_allow_html=True)
            st.markdown("<h5><b>Disclaimer:</b> The information provided here is for informational purposes and should not be used as a basis for investment decisions. This is not professional advice.</h5>", unsafe_allow_html=True)

            if st.button("Sign Out"):
                sign_out()

            st.markdown("<br>", unsafe_allow_html=True)

        def show_overview_page():
        
            response = requests.get('https://api64.ipify.org?format=json')
            if response.status_code == 200:
                ip_data = response.json()
                public_ip = ip_data['ip']
            else:
                public_ip = "Error: Unable to retrieve IP address"

            st.markdown("<h1><b>Data App Information:</b></h1>", unsafe_allow_html=True)
            st.markdown(f"<h3><b>Software Name:</b> Economy.py</h>", unsafe_allow_html=True)
            st.markdown(f"<h3><b>Public IP:</b> {public_ip}</h3>", unsafe_allow_html=True)

            st.markdown(f"<h3><b>Code Commit:</h3>", unsafe_allow_html=True)

            tab1_cc, tab2_cc, tab3_cc, tab4_cc, tab5_cc, tab6_cc, tab7_cc, tab8_cc = st.tabs(["Inflation", "Page 2", "Page 3", "Page 4", "Page 5", "Page 6", "Page 7","Page 8"])

            with tab1_cc:
                st.header("Page 1")
                code1 = '''
                json_menu = {
                  "Overall Consumer Prices": [
                    {"title": "All Items in U.S. City Average", "id": "CPIAUCSL"},
                  ],
                  "Core Consumer Prices (excluding Food and Energy)": [
                    {"title": "All Items Less Food and Energy in U.S. City Average", "id": "CPILFESL"},
                    {"title": "All Items Less Medical Care in U.S. City Average", "id": "CUSR0000SA0L5"},
                    {"title": "All Items Less Food in U.S. City Average", "id": "CPIULFSL"},
                    {"title": "Commodities Less Food and Energy Commodities in U.S. City Average", "id": "CUSR0000SACL1E"},
                    {"title": "All Items Less Energy in U.S. City Average", "id": "CPILEGSL"},
                    {"title": "Nondurables Less Food and Apparel in U.S. City Average", "id": "CUSR0000SANL13"},
                    {"title": "Nondurables Less Food, Beverages, and Apparel in U.S. City Average", "id": "CUSR0000SANL113"},
                    {"title": "Nondurables Less Food and Beverages in U.S. City Average", "id": "CUSR0000SANL11"},
                    {"title": "Nondurables Less Food in U.S. City Average", "id": "CUSR0000SANL1"},
                    {"title": "Commodities Less Food and Beverages in U.S. City Average", "id": "CUSR0000SACL11"},
                    {"title": "Commodities Less Food in U.S. City Average", "id": "CUSR0000SACL1"},
                  ],
                  "Healthcare and Medical Services": [
                    {"title": "Hospital and Related Services in U.S. City Average", "id": "CUSR0000SEMD"},
                    {"title": "Medical Care in U.S. City Average", "id": "CPIMEDSL"},
                    {"title": "Medical Care Services in U.S. City Average", "id": "CUSR0000SAM2"},
                    {"title": "Medical Care Commodities in U.S. City Average", "id": "CUSR0000SAM1"},
                    {"title": "Services by Other Medical Professionals in U.S. City Average", "id": "CUSR0000SEMC04"},
                  ],
                  "Transportation and Vehicles": [
                    {"title": "Transportation Services in U.S. City Average", "id": "CUSR0000SAS4"},
                    {"title": "Used Cars and Trucks in U.S. City Average", "id": "CUSR0000SETA02"},
                    {"title": "New Vehicles in U.S. City Average", "id": "CUSR0000SETA01"},
                    {"title": "Airline Fares in U.S. City Average", "id": "CUSR0000SETG01"},
                    {"title": "Transportation in U.S. City Average", "id": "CPITRNSL"},
                    {"title": "Motor Vehicle Maintenance and Repair in U.S. City Average", "id": "CUSR0000SETD"},
                    {"title": "New and Used Motor Vehicles in U.S. City Average", "id": "CUSR0000SETA"},
                    {"title": "Public Transportation in U.S. City Average", "id": "CUSR0000SETG"},
                    {"title": "Private Transportation in U.S. City Average", "id": "CUSR0000SAT1"},
                  ],
                  "Energy and Utilities": [
                    {"title": "Energy Commodities in U.S. City Average", "id": "CUSR0000SACE"},
                    {"title": "Motor Fuel in U.S. City Average", "id": "CUSR0000SETB"},
                    {"title": "Energy in U.S. City Average", "id": "CPIENGSL"},
                    {"title": "Electricity in U.S. City Average", "id": "CUSR0000SEHF01"},
                    {"title": "Gasoline (All Types) in U.S. City Average", "id": "CUSR0000SETB01"},
                    {"title": "Household Energy in U.S. City Average", "id": "CUSR0000SAH21"},
                    {"title": "Water and Sewer and Trash Collection Services in U.S. City Average", "id": "CUSR0000SEHG"},
                    {"title": "Fuels and Utilities in U.S. City Average", "id": "CUSR0000SAH2"},
                    {"title": "Fuel Oil and Other Fuels in U.S. City Average", "id": "CUSR0000SEHE"},
                    {"title": "Utility (Piped) Gas Service in U.S. City Average", "id": "CUSR0000SEHF02"},
                    {"title": "Energy Services in U.S. City Average", "id": "CUSR0000SEHF"},  
                  ],
                  "Food and Beverages": [
                    {"title": "Dairy and Related Products in U.S. City Average", "id": "CUSR0000SEFJ"},
                    {"title": "Food in U.S. City Average", "id": "CPIUFDSL"},
                    {"title": "Food at Home in U.S. City Average", "id": "CUSR0000SAF11"},
                    {"title": "Food Away from Home in U.S. City Average", "id": "CUSR0000SEFV"},
                    {"title": "Food and Beverages in U.S. City Average", "id": "CPIFABSL"},
                    {"title": "Alcoholic Beverages at Home in U.S. City Average", "id": "CUSR0000SEFW"},
                    {"title": "Sugar and Sweets in U.S. City Average", "id": "CUSR0000SEFR"},
                    {"title": "Pet Food in U.S. City Average", "id": "CUSR0000SS61031"},
                    {"title": "Meats, Poultry, Fish, and Eggs in U.S. City Average", "id": "CUSR0000SAF112"},
                    {"title": "Fruits and Vegetables in U.S. City Average", "id": "CUSR0000SAF113"},
                    {"title": "Alcoholic Beverages in U.S. City Average", "id": "CUSR0000SAF116"},
                    {"title": "Nonalcoholic Beverages and Beverage Materials in U.S. City Average", "id": "CUSR0000SAF114"},
                    {"title": "Alcoholic Beverages Away from Home in U.S. City Average", "id": "CUSR0000SEFX"},
                    {"title": "Fats and Oils in U.S. City Average", "id": "CUSR0000SEFS"},
                    {"title": "Other Foods in U.S. City Average", "id": "CUSR0000SEFT"},
                    {"title": "Other Food Away from Home in U.S. City Average", "id": "CUSR0000SEFV05"},
                    {"title": "Alcoholic Beverages Away from Home in U.S. City Average", "id": "CUSR0000SEFX"},
                    {"title": "Fats and Oils in U.S. City Average", "id": "CUSR0000SEFS"},
                    {"title": "Other Foods in U.S. City Average", "id": "CUSR0000SEFT"},
                    {"title": "Other Food Away from Home in U.S. City Average", "id": "CUSR0000SEFV05"},
                  ],
                  "Housing and Shelter": [
                    {"title": "Shelter in U.S. City Average", "id": "CUSR0000SAH1"},
                    {"title": "Rent of Primary Residence in U.S. City Average", "id": "CUSR0000SEHA"},
                    {"title": "Owners' Equivalent Rent of Residences in U.S. City Average", "id": "CUSR0000SEHC"},
                    {"title": "Housing in U.S. City Average", "id": "CPIHOSSL"},
                    {"title": "Rent of Shelter in U.S. City Average", "id": "CUSR0000SAS2RS"},
                    {"title": "Lodging Away from Home in U.S. City Average", "id": "CUSR0000SEHB"},
                    {"title": "Owners' Equivalent Rent of Primary Residence in U.S. City Average", "id": "CUSR0000SEHC01"},
                    {"title": "Household Furnishings and Operations in U.S. City Average", "id": "CUSR0000SAH3"},
                  ],
                  "Apparel and Footwear": [
                    {"title": "Apparel in U.S. City Average", "id": "CPIAPPSL"},
                    {"title": "Footwear in U.S. City Average", "id": "CUSR0000SEAE"},
                    {"title": "Women's and Girls' Apparel in U.S. City Average", "id": "CUSR0000SAA2"},
                    {"title": "Men's and Boys' Apparel in U.S. City Average", "id": "CUSR0000SAA1"},
                    {"title": "Infants' and Toddlers' Apparel in U.S. City Average", "id": "CUSR0000SEAF"},
                    {"title": "Apparel Less Footwear in U.S. City Average", "id": "CUSR0000SA311"},
                  ],
                  "Education and Communication": [
                    {"title": "Education in U.S. City Average", "id": "CUSR0000SAE1"},
                    {"title": "Education and Communication in U.S. City Average", "id": "CPIEDUSL"},
                    {"title": "Tuition, Other School Fees, and Childcare in U.S. City Average", "id": "CUSR0000SEEB"},
                    {"title": "Information Technology, Hardware and Services in U.S. City Average", "id": "CUSR0000SEEE"},
                    {"title": "Communication in U.S. City Average", "id": "CUSR0000SAE2"},
                    {"title": "Computers, Peripherals, and Smart Home Assistants in U.S. City Average", "id": "CUSR0000SEEE01"},
                    {"title": "Cable, Satellite, and Live Streaming Television Service in U.S. City Average", "id": "CUSR0000SERA02"},
                    {"title": "Educational Books and Supplies in U.S. City Average", "id": "CUSR0000SEEA"},
                    {"title": "Information and Information Processing in U.S. City Average", "id": "CUSR0000SAE21"},
                  ],
                  "Recreation and Leisure": [
                    {"title": "Club Membership for Shopping Clubs, Fraternal, or Other Organizations, or Participant Sports Fees in U.S. City Average", "id": "CUSR0000SERF01"},
                    {"title": "Admission to Movies, Theaters, and Concerts in U.S. City Average", "id": "CUSR0000SS62031"},
                    {"title": "Recreation in U.S. City Average", "id": "CPIRECSL"},
                    {"title": "Video and Audio in U.S. City Average", "id": "CUSR0000SERA"},
                    {"title": "Video and Audio Products in U.S. City Average", "id": "CUSR0000SERAC"},
                    {"title": "Music Instruments and Accessories in U.S. City Average", "id": "CUSR0000SERE03"},
                    {"title": "Fees for Lessons or Instructions in U.S. City Average", "id": "CUSR0000SERF03"},
                  ],
                  "Services": [
                    {"title": "Services Less Energy Services in U.S. City Average", "id": "CUSR0000SASLE"},
                    {"title": "Services in U.S. City Average", "id": "CUSR0000SAS"},
                    {"title": "Professional Services in U.S. City Average", "id": "CUSR0000SEMC"},
                    {"title": "Personal Care in U.S. City Average", "id": "CUSR0000SAG1"},
                    {"title": "Services Less Rent of Shelter in U.S. City Average", "id": "CUSR0000SASL2RS"},
                    {"title": "Laundry and Dry Cleaning Services in U.S. City Average", "id": "CUSR0000SEGD03"},
                    {"title": "Other Services in U.S. City Average", "id": "CUSR0000SAS367"},
                    {"title": "Services Less Medical Care Services in U.S. City Average", "id": "CUSR0000SASL5"},
                  ],
                  "Durables and Non-Durables": [
                    {"title": "Durables in U.S. City Average", "id": "CUSR0000SAD"},
                    {"title": "Nondurables in U.S. City Average", "id": "CUSR0000SAN"},
                    {"title": "Motor Vehicle Parts and Equipment in U.S. City Average", "id": "CUSR0000SETC"},
                    {"title": "Tobacco and Smoking Products in U.S. City Average", "id": "CUSR0000SEGA"},
                    {"title": "Toys in U.S. City Average", "id": "CUSR0000SERE01"},  
                  ],
                  "Miscellaneous Goods and Services": [
                    {"title": "Miscellaneous Personal Services in U.S. City Average", "id": "CUSR0000SEGD"},
                    {"title": "Commodities in U.S. City Average", "id": "CUSR0000SAC"},
                    {"title": "Other Goods and Services in U.S. City Average", "id": "CPIOGSSL"},
                  ]
                }
                '''
                st.code(code1, language="python")

            with tab2_cc:
               st.header("Page 2")

            with tab3_cc:
               st.header("Page 3")

            with tab4_cc:
               st.header("Page 4")

            with tab5_cc:
               st.header("Page 5")

            with tab6_cc:
               st.header("Page 6")

            with tab7_cc:
               st.header("Page 7")

            with tab8_cc:
               st.header("Page 8")

        if choice == "Overview":
            show_overview_page()
        elif choice == "Inflation":
            show_page1()
        elif choice == "Page 2": 
            show_page2()
        elif choice == "Page 3": 
            show_page3()
        elif choice == "Page 4": 
            show_page4()
        elif choice == "Page 5": 
            show_page5()
        elif choice == "Page 6":
            show_page6()
        elif choice == "Page 7": 
            show_page7()
        elif choice == "Page 8": 
            show_page8()

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
            st.markdown("<h3 style='padding-top: 5px; padding-bottom: 5px;'>If you are a new employee and need access to this data application, please connect with the 87TR Support Desk for assistance.</h3>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()