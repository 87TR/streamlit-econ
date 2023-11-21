import credentials

import streamlit as st
import pandas as pd
import altair as alt

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import datetime

#Connect to tailwind
st.markdown(
    """
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.16/dist/tailwind.min.css" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

# Include the Inter font stylesheet 
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

authorization_fred = credentials.fred_apikey

def fetch_data():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CPIAUCSL': 'All items',
        'CUSR0000SAF11': 'Food at home',
        'CUSR0000SEFV': 'Food away from home',
        'CPIHOSSL': 'Housing',
        'CUSR0000SAH1': 'Shelter',
        'CUSR0000SEHA': 'Rent of primary residence',
        'CUSR0000SEHB': 'Lodging away from home',
        'CUSR0000SEHC': "Owners' equivalent rent of residences",
        'CUSR0000SEHC01': "Owners' equivalent rent of primary residence",
        'CUSR0000SAH2': 'Fuels and utilities',
        'CUSR0000SAH21': 'Household energy',
        'CPIAPPSL': 'Apparel',
        'CPITRNSL': 'Transportation',
        'CUSR0000SETA01': 'New vehicles',
        'CUSR0000SETA02': 'Used cars and trucks',
        'CUSR0000SETC': 'Motor vehicle parts and equipment',
        'CUSR0000SETD': 'Motor vehicle maintenance and repair',
        'CUSR0000SETG': 'Public transportation',
        'CUSR0000SETG01': 'Airline fare',
        'CPIMEDSL': 'Medical care',
        'CUSR0000SEMC': 'Professional services',
        'CUSR0000SEMC04': 'Services by other medical professionals',
        'CPIRECSL': 'Recreation',
        'CPIEDUSL': 'Education and communication',
        'CUSR0000SEEE01': 'Personal computers and peripheral equipment',
        'CPIOGSSL': 'Other goods and services',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2020-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data

    return fred_data

@st.cache_data
def fetch_button_data(selected_id):
    endpoint = 'https://api.stlouisfed.org/fred/series/observations'
    
    params = {
        'series_id': selected_id,
        'api_key': authorization_fred,
        'file_type': 'json'
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['observations'])
        
        df['series_id'] = selected_id

        return df
    else:
        st.error(f"Error: {response.status_code}")
        return pd.DataFrame()

def show_inflation_consumerpriceindex():

    if st.session_state.get("authentication_status"):
        
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
        
        tab1a, tab2a, tab3a, tab4a = st.tabs(["Weights", "Indicators", "Search", "Links"])

        with tab1a:
                st.markdown(f"<h1><b>CPI: Weights<b></h1>", unsafe_allow_html=True)
                
                st.markdown(f"<h2><u>Food: ±13.4%</u></h2>", unsafe_allow_html=True)
                st.markdown(f"<h3>Food at home: ±8.6%</h3>", unsafe_allow_html=True)
                st.markdown(f"<h3>Food away from home: ±4.8%</h3>", unsafe_allow_html=True)
                st.markdown(f"<h2><u>Energy: ±7.2%</u></h2>", unsafe_allow_html=True)
                st.markdown(f"<h3>Energy commodities: ±3.9%</h3>", unsafe_allow_html=True)
                st.markdown(f"<h3>Energy services: ±3.3%</h3>", unsafe_allow_html=True)
                st.markdown(f"<h2><u>All items less food and energy: ±79.4</u></h2>", unsafe_allow_html=True)
                st.markdown(f"<h3>Commodities less food and energy commodities: ±21.0</h3>", unsafe_allow_html=True)
                st.markdown(f"<h3>Services less energy services: ±58.4*</h3>", unsafe_allow_html=True)
                st.markdown(f"<h4><i>*Shelter: ±34.9; Medical care services: ±6.324; Transportation services: ±5.9</i></h3>", unsafe_allow_html=True)

        with tab2a:

            st.markdown(f"<h1><b>CPI: Indicators</b></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="cpi_indicators"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data()
                    st.success("Data fetched successfully!")

                for series_id, data in fred_data.items():
                    # st.subheader(series_id)
                    observations = data['observations']

                    indicator_name = data['indicator']
                    yy_changes = []

                    for i, observation in enumerate(observations[-6:], start=-6):
                        date = datetime.datetime.strptime(observation['date'], '%Y-%m-%d').strftime('%B %Y')
                        value = float(observation['value'])

                        yy_change_value = float(observations[i - 12]['value']) if i - 12 >= -len(observations) else float(observations[0]['value'])
                        yy_change = value - yy_change_value
                        yy_change_perc = (yy_change / yy_change_value) * 100
                        yy_change_perc_decimal = round(yy_change_perc, 1)

                        if yy_change_perc_decimal < -2:
                            color = 'orange'
                        elif -2 <= yy_change_perc_decimal <= 2:
                            color = 'green'
                        else:
                            color = 'red'

                        yy_change_text = f"{date}: <b><u><font color='{color}'>{yy_change_perc_decimal}%</font></u></b>"
                        yy_changes.append(yy_change_text)

                    yy_changes_text = "; ".join(yy_changes)

                    st.markdown(f"<h3><b>{indicator_name}</b></h3>", unsafe_allow_html=True)
                    st.markdown(f"<h4>{yy_changes_text}</h4>", unsafe_allow_html=True)

        with tab3a:

            st.markdown(f"<h1><b>CPI: Search</b></h1>", unsafe_allow_html=True)

            use_container_width = st.checkbox("Use container width", value=True, key="use_container_width_consumerpriceindex")

            if st.button("Clear [Consumer Price Index] Data"):
                for key in list(st.session_state.keys()):
                    if key.startswith('df_'):
                        del st.session_state[key]

                fetch_button_data.clear()

            categories = list(json_menu.keys())
            selected_category = st.selectbox("Select a Category", categories)

            if selected_category:
                subcategories = [item["title"] for item in json_menu[selected_category]]
                selected_subcategory = st.selectbox(f"Select a Subcategory in {selected_category}", subcategories)

                if st.button('Fetch Data', key="cpi_search"):
                    if selected_subcategory:
                        selected_id = next(item["id"] for item in json_menu[selected_category] if item["title"] == selected_subcategory)
                        df_consumerpriceindex = fetch_button_data(selected_id)
                        if not df_consumerpriceindex.empty:
                            
                            st.session_state['df_consumerpriceindex'] = df_consumerpriceindex
                        
                            df_consumerpriceindex = df_consumerpriceindex.copy()
                            df_consumerpriceindex = df_consumerpriceindex[['date', 'value', 'series_id']]
                            
                            df_consumerpriceindex['date'] = pd.to_datetime(df_consumerpriceindex['date'])
                            df_consumerpriceindex['value'] = pd.to_numeric(df_consumerpriceindex['value'], errors='coerce')
                            df_consumerpriceindex.sort_values(by='date', inplace=True)

                            df_consumerpriceindex['mm_change'] = df_consumerpriceindex['value'].diff()
                            df_consumerpriceindex['mm_change_perc'] = (df_consumerpriceindex['mm_change'] / df_consumerpriceindex['value'].shift(1)) * 100
                            df_consumerpriceindex['mm_change_perc_decimal'] = df_consumerpriceindex['mm_change_perc'].round(1)

                            df_consumerpriceindex['yy_change'] = df_consumerpriceindex['value'] - df_consumerpriceindex['value'].shift(12)
                            df_consumerpriceindex['yy_change_perc'] = (df_consumerpriceindex['yy_change'] / df_consumerpriceindex['value'].shift(12)) * 100
                            df_consumerpriceindex['yy_change_perc_decimal'] = df_consumerpriceindex['yy_change_perc'].round(1)

                            df_consumerpriceindex['3m_annualized_mm_change_perc'] = df_consumerpriceindex['mm_change_perc'].rolling(window=3).sum() * 4
                            df_consumerpriceindex['4m_annualized_mm_change_perc'] = df_consumerpriceindex['mm_change_perc'].rolling(window=4).sum() * 3
                            df_consumerpriceindex['6m_annualized_mm_change_perc'] = df_consumerpriceindex['mm_change_perc'].rolling(window=6).sum() * 2
                            df_consumerpriceindex['12m_annualized_mm_change_perc'] = df_consumerpriceindex['mm_change_perc'].rolling(window=12).sum() * 1

                            df_consumerpriceindex['3m_annualized_vs_yy'] = df_consumerpriceindex['3m_annualized_mm_change_perc'] - df_consumerpriceindex['yy_change_perc'] 
                            df_consumerpriceindex['4m_annualized_vs_yy'] = df_consumerpriceindex['4m_annualized_mm_change_perc'] - df_consumerpriceindex['yy_change_perc'] 
                            df_consumerpriceindex['6m_annualized_vs_yy'] = df_consumerpriceindex['6m_annualized_mm_change_perc'] - df_consumerpriceindex['yy_change_perc'] 
                            df_consumerpriceindex['12m_annualized_vs_yy'] = df_consumerpriceindex['12m_annualized_mm_change_perc'] - df_consumerpriceindex['yy_change_perc'] 
                            
                            df_consumerpriceindex.sort_values(by='date', inplace=True, ascending=False)
                            df_consumerpriceindex['date'] = df_consumerpriceindex['date'].dt.strftime('%Y-%m-%d')

                            st.session_state['df_consumerpriceindex'] = df_consumerpriceindex

                        else:
                            st.error("No data fetched.")

                if 'df_consumerpriceindex' in st.session_state:

                    df_consumerpriceindex = st.session_state['df_consumerpriceindex']

                    st.markdown(f"<h1><b>Data Observations:</b></h1>", unsafe_allow_html=True)
                    st.markdown(f"<h4>* Data Seasonally Adjusted</h4>", unsafe_allow_html=True)
                    df_consumerpriceindexdisplay = df_consumerpriceindex.head(48)
                    df_consumerpriceindexdisplay = df_consumerpriceindexdisplay.reset_index(drop=True)
                    st.dataframe(df_consumerpriceindexdisplay, use_container_width=use_container_width)

                    chart_sets = {
                        'set1': {
                            'columns': ['mm_change', 'mm_change_perc'],
                            'line_value': 0,
                            'title': 'Monthly Change'
                        },
                        'set2': {
                            'columns': ['yy_change', 'yy_change_perc'],
                            'line_value': 2,
                            'title': 'Yearly Change'
                        },
                        'set3': {
                            'columns': [
                                '3m_annualized_mm_change_perc', '4m_annualized_mm_change_perc',
                                '6m_annualized_mm_change_perc', '12m_annualized_mm_change_perc'
                            ],
                            'line_value': 3,
                            'title': 'Annualized Change'
                        }
                    }
                    
                    column_title_mapping = {
                        'mm_change': 'M/M Change',
                        'mm_change_perc': 'M/M Change %',
                        'yy_change': 'Y/Y Change',
                        'yy_change_perc': 'Y/Y Change %',
                        '3m_annualized_mm_change_perc': '3-Month Annualized M/M Change %',
                        '4m_annualized_mm_change_perc': '4-Month Annualized M/M Change %',
                        '6m_annualized_mm_change_perc': '6-Month Annualized M/M Change %',
                        '12m_annualized_mm_change_perc': '12-Month Annualized M/M Change %'
                    }

                    st.markdown(f"<h1><b>Data Visualization:</b></h1>", unsafe_allow_html=True)

                    for set_name, chart_info in chart_sets.items():
                        charts = []
                        
                        for column in chart_info['columns']:

                            descriptive_title = column_title_mapping.get(column, column)

                            chart = alt.Chart(df_consumerpriceindex).mark_line(strokeWidth=1).encode(
                                x=alt.X('date:T', axis=alt.Axis(format='%Y-%m-%d')),
                                y=alt.Y(f'{column}:Q', title=descriptive_title)
                            ).properties(
                                title=f'{descriptive_title}',
                                width=1000,
                                height=600
                            )

                            line_value = chart_info['line_value']
                            line = alt.Chart(pd.DataFrame({'zero': [line_value]})).mark_rule(color='red', strokeDash=[2, 2]).encode(
                                y='zero:Q'
                            )
                            
                            combined_chart = chart + line
                            charts.append(combined_chart)
                        
                        final_chart = alt.concat(*charts, columns=1).resolve_scale(y='independent')
                        
                        category_title = chart_info['title']
                        st.markdown(f"<h3><u>{category_title}</u></h3>", unsafe_allow_html=True)
                        st.altair_chart(final_chart, use_container_width=True)

        with tab4a:
            st.markdown(f"<h1><b>CPI: Links</b></h1>", unsafe_allow_html=True)
            st.markdown(f"<h3>Table 1. Consumer Price Index for All Urban Consumers (CPI-U): U.S. city average, by expenditure category <a href='https://www.bls.gov/web/cpi/cpipress1.xlsx'>(XLSX)</a></h3>", unsafe_allow_html=True)
            st.markdown(f"<h3>Table 2. Consumer Price Index for All Urban Consumers (CPI-U): U.S. city average, by detailed expenditure category <a href='https://www.bls.gov/web/cpi/cpipress2.xlsx'>(XLSX)</a></h3>", unsafe_allow_html=True)
            st.markdown(f"<h3>Table 3. Consumer Price Index for All Urban Consumers (CPI-U): U.S. city average, special aggregate indexes <a href='https://www.bls.gov/web/cpi/cpipress3.xlsx'>(XLSX)</a></h3>", unsafe_allow_html=True)
            st.markdown(f"<h3>Table 4. Consumer Price Index for All Urban Consumers (CPI-U): Selected areas, all items index <a href='https://www.bls.gov/web/cpi/cpipress4.xlsx'>(XLSX)</a></h3>", unsafe_allow_html=True)
            st.markdown(f"<h3>Table 5. Chained Consumer Price Index for All Urban Consumers (C-CPI-U) and the Consumer Price Index for All Urban Consumers (CPI-U): U.S. city average, all items index <a href='https://www.bls.gov/web/cpi/cpipress5.xlsx'>(XLSX)</a></h3>", unsafe_allow_html=True)
            st.markdown(f"<h3>Table 6. Consumer Price Index for All Urban Consumers (CPI-U): U.S. city average, by expenditure category, 1-month analysis table <a href='https://www.bls.gov/web/cpi/cpipress6.xlsx'>(XLSX)</a></h3>", unsafe_allow_html=True)
            st.markdown(f"<h3>Table 7. Consumer Price Index for All Urban Consumers (CPI-U): U.S. city average, by expenditure category, 12-month analysis table <a href='https://www.bls.gov/web/cpi/cpipress7.xlsx'>(XLSX)</a></h3>", unsafe_allow_html=True)

# Display the page
show_inflation_consumerpriceindex()