import credentials

import streamlit as st
import pandas as pd
import altair as alt

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import datetime

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

authorization_fred = credentials.fred_apikey

def fetch_data_allindustries():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CES1011330001': 'Logging',
        'CES1021100001': 'Oil & Gas Extraction',
        'CES1021200001': 'Mining, Except Oil & Gas',
        'CES1021300001': 'Support Activities for Mining',
        'CES2023610001': 'Residential Building',
        'CES2023620001': 'Nonresidential Building',
        'CES2023700001': 'Heavy & Civil Engineering Construction',
        'CES2023800101': 'Residential Specialty Trade Contractors',
        'CES2023800201': 'Nonresidential Specialty Trade Contractors',
        'CES3132100001': 'Wood Products',
        'CES3132700001': 'Nonmetallic Mineral Products',
        'CES3133100001': 'Primary Metals',
        'CES3133200001': 'Fabricated Metal Products',
        'CES3133300001': 'Machinery',
        'CES3133400001': 'Computer & Electronic Products',
        'CES3133410001': 'Computer & Peripheral Equipment',
        'CES3133420001': 'Communications Equipment',
        'CES3133440001': 'Semiconductors & Electronic Components',
        'CES3133450001': 'Electronic Instruments',
        'CES3133500001': 'Electrical Equipment & Appliances',
        'CES3133600001': 'Transportation Equipment',
        'CES3133600101': 'Motor Vehicles & Parts',
        'CES3133700001': 'Furniture & Related Products',
        'CES3133900001': 'Miscellaneous Durable Goods Manufacturing',
        'CES3231100001': 'Food Manufacturing',
        'CES3231300001': 'Textile Mills',
        'CES3231400001': 'Textile Product Mills',
        'CES3231500001': 'Apparel',
        'CES3232200001': 'Paper & Paper Products',
        'CES3232300001': 'Printing & Related Support Activities',
        'CES3232400001': 'Petroleum & Coal Products',
        'CES3232500001': 'Chemicals',
        'CES3232600001': 'Plastics & Rubber Products',
        'CES3232900001': 'Miscellaneous Nondurable Goods Manufacturing',
        'CES5051100001': 'Publishing Industries, Except Internet',
        'CES5051200001': 'Motion Picture & Sound Recording Industries',
        'CES5051500001': 'Broadcasting, Except Internet',
        'CES5051700001': 'Telecommunications',
        'CES5051800001': 'Data Processing, Hosting & Related Services',
        'CES5051900001': 'Other Information Services',
        'CES5552000001': 'Finance & Insurance',
        'CES5553000001': 'Real Estate & Rental & Leasing',
        'CES6054000001': 'Professional & Technical Services',
        'CES6055000001': 'Management of Companies & Enterprises',
        'CES6056000001': 'Administrative & Waste Services',
        'CES6561000001': 'Educational Services',
        'CES6562000001': 'Health Care & Social Assistance',
        'CES7071000001': 'Arts, Entertainment & Recreation',
        'CES7072000001': 'Accommodations & Food Services',
        'CES8081100001': 'Repair & Maintenance',
        'CES8081200001': 'Personal & Laundry Services',
        'CES8081300001': 'Membership Associations & Organizations',
        'CES9091100001': 'Federal, Except U.S. Postal Service',
        'CES9091912001': 'U.S. Postal Service',
        'CES9092161101': 'State Government Education',
        'CES9092200001': 'State Government, Excluding Education',
        'CES9093161101': 'Local Government Education',
        'CES9093200001': 'Local Government, Excluding Education',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')
    one_year_ago = (datetime.date.today() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': one_year_ago,
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_mininglogging():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CES1011330001': 'Logging',
        'CES1021100001': 'Oil & Gas Extraction',
        'CES1021200001': 'Mining, Except Oil & Gas',
        'CES1021300001': 'Support Activities for Mining',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2000-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_construction():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CES2023610001': 'Residential Building',
        'CES2023620001': 'Nonresidential Building',
        'CES2023700001': 'Heavy & Civil Engineering Construction',
        'CES2023800101': 'Residential Specialty Trade Contractors',
        'CES2023800201': 'Nonresidential Specialty Trade Contractors',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2000-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_manufacturing():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CES3132100001': 'Wood Products',
        'CES3132700001': 'Nonmetallic Mineral Products',
        'CES3133100001': 'Primary Metals',
        'CES3133200001': 'Fabricated Metal Products',
        'CES3133300001': 'Machinery',
        'CES3133400001': 'Computer & Electronic Products',
        'CES3133410001': 'Computer & Peripheral Equipment',
        'CES3133420001': 'Communications Equipment',
        'CES3133440001': 'Semiconductors & Electronic Components',
        'CES3133450001': 'Electronic Instruments',
        'CES3133500001': 'Electrical Equipment & Appliances',
        'CES3133600001': 'Transportation Equipment',
        'CES3133600101': 'Motor Vehicles & Parts',
        'CES3133700001': 'Furniture & Related Products',
        'CES3133900001': 'Miscellaneous Durable Goods Manufacturing',
        'CES3231100001': 'Food Manufacturing',
        'CES3231300001': 'Textile Mills',
        'CES3231400001': 'Textile Product Mills',
        'CES3231500001': 'Apparel',
        'CES3232200001': 'Paper & Paper Products',
        'CES3232300001': 'Printing & Related Support Activities',
        'CES3232400001': 'Petroleum & Coal Products',
        'CES3232500001': 'Chemicals',
        'CES3232600001': 'Plastics & Rubber Products',
        'CES3232900001': 'Miscellaneous Nondurable Goods Manufacturing',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2000-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_tradetransportationutilities():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'USWTRADE': 'Wholesale Trade',
        'USTRADE': 'Retail Trade',
        'CES4300000001': 'Transportation & Warehousing',
        'CES4422000001': 'Utilities',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2000-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_information():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CES5051100001': 'Publishing Industries, Except Internet',
        'CES5051200001': 'Motion Picture & Sound Recording Industries',
        'CES5051500001': 'Broadcasting, Except Internet',
        'CES5051700001': 'Telecommunications',
        'CES5051800001': 'Data Processing, Hosting & Related Services',
        'CES5051900001': 'Other Information Services',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2000-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_financialactivities():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CES5552000001': 'Finance & Insurance',
        'CES5553000001': 'Real Estate & Rental & Leasing',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2000-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_professionalbusinessservices():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CES6054000001': 'Professional & Technical Services',
        'CES6055000001': 'Management of Companies & Enterprises',
        'CES6056000001': 'Administrative & Waste Services',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2000-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_educationhealthservices():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CES6561000001': 'Educational Services',
        'CES6562000001': 'Health Care & Social Assistance',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2000-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_leisurehospitality():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CES7071000001': 'Arts, Entertainment & Recreation',
        'CES7072000001': 'Accommodations & Food Services',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2000-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_otherservices():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CES8081100001': 'Repair & Maintenance',
        'CES8081200001': 'Personal & Laundry Services',
        'CES8081300001': 'Membership Associations & Organizations',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2000-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_federalgovernment():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CES9091100001': 'Federal, Except U.S. Postal Service',
        'CES9091912001': 'U.S. Postal Service',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2000-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_stategovernment():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CES9092161101': 'State Government Education',
        'CES9092200001': 'State Government, Excluding Education',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2000-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_localgovernment():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CES9093161101': 'Local Government Education',
        'CES9093200001': 'Local Government, Excluding Education',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2000-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def show_labormarket_employmentbyindustry():

    if st.session_state.get("authentication_status"):

        tab1a, tab2a, tab3a, tab4a = st.tabs(["Employment by Industry", "Goods", "Services", "Government"])

        with tab1a:

            st.markdown("<h1><b>Employment by Industry</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="employmentbyindustry_allindustries"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_allindustries()

                    series_mapping = {
                        'CES1011330001': 'Logging',
                        'CES1021100001': 'Oil & Gas Extraction',
                        'CES1021200001': 'Mining, Except Oil & Gas',
                        'CES1021300001': 'Support Activities for Mining',
                        'CES2023610001': 'Residential Building',
                        'CES2023620001': 'Nonresidential Building',
                        'CES2023700001': 'Heavy & Civil Engineering Construction',
                        'CES2023800101': 'Residential Specialty Trade Contractors',
                        'CES2023800201': 'Nonresidential Specialty Trade Contractors',
                        'CES3132100001': 'Wood Products',
                        'CES3132700001': 'Nonmetallic Mineral Products',
                        'CES3133100001': 'Primary Metals',
                        'CES3133200001': 'Fabricated Metal Products',
                        'CES3133300001': 'Machinery',
                        'CES3133400001': 'Computer & Electronic Products',
                        'CES3133410001': 'Computer & Peripheral Equipment',
                        'CES3133420001': 'Communications Equipment',
                        'CES3133440001': 'Semiconductors & Electronic Components',
                        'CES3133450001': 'Electronic Instruments',
                        'CES3133500001': 'Electrical Equipment & Appliances',
                        'CES3133600001': 'Transportation Equipment',
                        'CES3133600101': 'Motor Vehicles & Parts',
                        'CES3133700001': 'Furniture & Related Products',
                        'CES3133900001': 'Miscellaneous Durable Goods Manufacturing',
                        'CES3231100001': 'Food Manufacturing',
                        'CES3231300001': 'Textile Mills',
                        'CES3231400001': 'Textile Product Mills',
                        'CES3231500001': 'Apparel',
                        'CES3232200001': 'Paper & Paper Products',
                        'CES3232300001': 'Printing & Related Support Activities',
                        'CES3232400001': 'Petroleum & Coal Products',
                        'CES3232500001': 'Chemicals',
                        'CES3232600001': 'Plastics & Rubber Products',
                        'CES3232900001': 'Miscellaneous Nondurable Goods Manufacturing',
                        'CES5051100001': 'Publishing Industries, Except Internet',
                        'CES5051200001': 'Motion Picture & Sound Recording Industries',
                        'CES5051500001': 'Broadcasting, Except Internet',
                        'CES5051700001': 'Telecommunications',
                        'CES5051800001': 'Data Processing, Hosting & Related Services',
                        'CES5051900001': 'Other Information Services',
                        'CES5552000001': 'Finance & Insurance',
                        'CES5553000001': 'Real Estate & Rental & Leasing',
                        'CES6054000001': 'Professional & Technical Services',
                        'CES6055000001': 'Management of Companies & Enterprises',
                        'CES6056000001': 'Administrative & Waste Services',
                        'CES6561000001': 'Educational Services',
                        'CES6562000001': 'Health Care & Social Assistance',
                        'CES7071000001': 'Arts, Entertainment & Recreation',
                        'CES7072000001': 'Accommodations & Food Services',
                        'CES8081100001': 'Repair & Maintenance',
                        'CES8081200001': 'Personal & Laundry Services',
                        'CES8081300001': 'Membership Associations & Organizations',
                        'CES9091100001': 'Federal, Except U.S. Postal Service',
                        'CES9091912001': 'U.S. Postal Service',
                        'CES9092161101': 'State Government Education',
                        'CES9092200001': 'State Government, Excluding Education',
                        'CES9093161101': 'Local Government Education',
                        'CES9093200001': 'Local Government, Excluding Education',
                    }

                    combined_df = pd.DataFrame()

                    for series_id, observations in fred_data.items():
                        temp_df = pd.DataFrame(observations)
                        temp_df['date'] = pd.to_datetime(temp_df['date'])
                        temp_df.set_index('date', inplace=True)
                        temp_df.rename(columns={'value': series_mapping[series_id]}, inplace=True)

                        if combined_df.empty:
                            combined_df = temp_df
                        else:
                            combined_df = combined_df.join(temp_df[series_mapping[series_id]], how='outer')

                    combined_df.reset_index(inplace=True)

                    df = combined_df.copy()
                    df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

                    df_melted = df.melt(id_vars=['date'], var_name='series', value_name='value')

                    df_melted = df_melted.rename(columns={
                        'date': 'Date',
                        'value': 'Value',
                        'indicator': 'Indicator',
                        'series': 'Series',
                        'series_id': 'Series ID'
                    })

                    df_transposed = df_melted.pivot(index='Series', columns='Date', values='Value')
                    df_transposed = df_transposed.sort_index(axis=1, ascending=False)
                    df_transposed.columns = df_transposed.columns.strftime('%Y-%m-%d')

                    df_transposed = df_transposed.apply(pd.to_numeric, errors='coerce')
                    numeric_columns = df_transposed.columns[df_transposed.dtypes == 'float64']
                    df_transposed[numeric_columns] = df_transposed[numeric_columns].applymap(lambda x: f'{x:,.0f}' if pd.notnull(x) else x)
                    st.dataframe(df_transposed)

                    st.markdown("<h4><b>Years, Seasonally Adjusted</h4></b>", unsafe_allow_html=True)
                    last_period_data = df_melted[df_melted['Date'] == df_melted['Date'].max()]
                    chart = alt.Chart(last_period_data).mark_bar().encode(
                        x=alt.X('Series:N', title='Series'),
                        y=alt.Y('Value:Q', title='Value'),
                        color='Series:N'
                    ).properties(
                        width=1000,
                        height=600,
                    )
                    st.altair_chart(chart, use_container_width=True)

        with tab2a:
            st.markdown("<h1><b>Goods Producing</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            with st.expander(f'Mining & Logging'):

                if st.button("Fetch Data", key="employmentbyindustry_mininglogging"):
                    with st.spinner("Fetching data..."):
                        fred_data = fetch_data_mininglogging()
                              
                        series_mapping = {
                            'CES1011330001': 'Logging',
                            'CES1021100001': 'Oil & Gas Extraction',
                            'CES1021200001': 'Mining, Except Oil & Gas',
                            'CES1021300001': 'Support Activities for Mining',
                        }
                                                
                        combined_df = pd.DataFrame()

                        for series_id, observations in fred_data.items():
                            temp_df = pd.DataFrame(observations)
                            temp_df['date'] = pd.to_datetime(temp_df['date'])
                            temp_df.set_index('date', inplace=True)
                            temp_df.rename(columns={'value': series_mapping[series_id]}, inplace=True)
                            
                            if combined_df.empty:
                                combined_df = temp_df
                            else:
                                combined_df = combined_df.join(temp_df[series_mapping[series_id]], how='outer')

                        combined_df.reset_index(inplace=True)
                        
                        df = combined_df.copy()
                        df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

                        df_melted = df.melt(id_vars=['date'], var_name='series', value_name='value')

                        df_melted = df_melted.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series': 'Series',
                            'series_id': 'Series ID'
                        })
                        
                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_melted).mark_line().encode(
                            x='Date:T',
                            y=alt.Y('Value:Q'),
                            color='Series:N'
                        ).properties(
                            width=1000,
                            height=600,
                        ).configure_legend(
                            orient='bottom',
                            labelLimit=0
                        )
                        st.altair_chart(chart, use_container_width=True)

            with st.expander(f'Construction'):

                if st.button("Fetch Data", key="employmentbyindustry_construction"):
                    with st.spinner("Fetching data..."):
                        fred_data = fetch_data_construction()

                        series_mapping = {
                            'CES2023610001': 'Residential Building',
                            'CES2023620001': 'Nonresidential Building',
                            'CES2023700001': 'Heavy & Civil Engineering Construction',
                            'CES2023800101': 'Residential Specialty Trade Contractors',
                            'CES2023800201': 'Nonresidential Specialty Trade Contractors',
                        }
                                                
                        combined_df = pd.DataFrame()

                        for series_id, observations in fred_data.items():
                            temp_df = pd.DataFrame(observations)
                            temp_df['date'] = pd.to_datetime(temp_df['date'])
                            temp_df.set_index('date', inplace=True)
                            temp_df.rename(columns={'value': series_mapping[series_id]}, inplace=True)
                            
                            if combined_df.empty:
                                combined_df = temp_df
                            else:
                                combined_df = combined_df.join(temp_df[series_mapping[series_id]], how='outer')

                        combined_df.reset_index(inplace=True)
                        
                        df = combined_df.copy()
                        df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

                        df_melted = df.melt(id_vars=['date'], var_name='series', value_name='value')

                        df_melted = df_melted.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series': 'Series',
                            'series_id': 'Series ID'
                        })
                        
                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_melted).mark_line().encode(
                            x='Date:T',
                            y=alt.Y('Value:Q'),
                            color='Series:N'
                        ).properties(
                            width=1000,
                            height=600,
                        ).configure_legend(
                            orient='bottom',
                            labelLimit=0
                        )
                        st.altair_chart(chart, use_container_width=True)

            with st.expander(f'Manufacturing'):

                if st.button("Fetch Data", key="employmentbyindustry_manufacturing"):
                    with st.spinner("Fetching data..."):
                        fred_data = fetch_data_manufacturing()

                        series_mapping = {
                            'CES3132100001': 'Wood Products',
                            'CES3132700001': 'Nonmetallic Mineral Products',
                            'CES3133100001': 'Primary Metals',
                            'CES3133200001': 'Fabricated Metal Products',
                            'CES3133300001': 'Machinery',
                            'CES3133400001': 'Computer & Electronic Products',
                            'CES3133410001': 'Computer & Peripheral Equipment',
                            'CES3133420001': 'Communications Equipment',
                            'CES3133440001': 'Semiconductors & Electronic Components',
                            'CES3133450001': 'Electronic Instruments',
                            'CES3133500001': 'Electrical Equipment & Appliances',
                            'CES3133600001': 'Transportation Equipment',
                            'CES3133600101': 'Motor Vehicles & Parts',
                            'CES3133700001': 'Furniture & Related Products',
                            'CES3133900001': 'Miscellaneous Durable Goods Manufacturing',
                            'CES3231100001': 'Food Manufacturing',
                            'CES3231300001': 'Textile Mills',
                            'CES3231400001': 'Textile Product Mills',
                            'CES3231500001': 'Apparel',
                            'CES3232200001': 'Paper & Paper Products',
                            'CES3232300001': 'Printing & Related Support Activities',
                            'CES3232400001': 'Petroleum & Coal Products',
                            'CES3232500001': 'Chemicals',
                            'CES3232600001': 'Plastics & Rubber Products',
                            'CES3232900001': 'Miscellaneous Nondurable Goods Manufacturing',
                        }
                                                
                        combined_df = pd.DataFrame()

                        for series_id, observations in fred_data.items():
                            temp_df = pd.DataFrame(observations)
                            temp_df['date'] = pd.to_datetime(temp_df['date'])
                            temp_df.set_index('date', inplace=True)
                            temp_df.rename(columns={'value': series_mapping[series_id]}, inplace=True)
                            
                            if combined_df.empty:
                                combined_df = temp_df
                            else:
                                combined_df = combined_df.join(temp_df[series_mapping[series_id]], how='outer')

                        combined_df.reset_index(inplace=True)
                        
                        df = combined_df.copy()
                        df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

                        df_melted = df.melt(id_vars=['date'], var_name='series', value_name='value')

                        df_melted = df_melted.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series': 'Series',
                            'series_id': 'Series ID'
                        })
                        
                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_melted).mark_line().encode(
                            x='Date:T',
                            y=alt.Y('Value:Q'),
                            color='Series:N'
                        ).properties(
                            width=1000,
                            height=600,
                        ).configure_legend(
                            orient='bottom',
                            labelLimit=0
                        )
                        st.altair_chart(chart, use_container_width=True)

        with tab3a:
            st.markdown("<h1><b>Private Service Providing</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            with st.expander(f'Trade, Transportation & Utilities'):

                if st.button("Fetch Data", key="employmentbyindustry_tradetransportationutilities"):
                    with st.spinner("Fetching data..."):
                        fred_data = fetch_data_tradetransportationutilities()

                        series_mapping = {
                            'USWTRADE': 'Wholesale Trade',
                            'USTRADE': 'Retail Trade',
                            'CES4300000001': 'Transportation & Warehousing',
                            'CES4422000001': 'Utilities',
                        }
                                                
                        combined_df = pd.DataFrame()

                        for series_id, observations in fred_data.items():
                            temp_df = pd.DataFrame(observations)
                            temp_df['date'] = pd.to_datetime(temp_df['date'])
                            temp_df.set_index('date', inplace=True)
                            temp_df.rename(columns={'value': series_mapping[series_id]}, inplace=True)
                            
                            if combined_df.empty:
                                combined_df = temp_df
                            else:
                                combined_df = combined_df.join(temp_df[series_mapping[series_id]], how='outer')

                        combined_df.reset_index(inplace=True)
                        
                        df = combined_df.copy()
                        df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

                        df_melted = df.melt(id_vars=['date'], var_name='series', value_name='value')

                        df_melted = df_melted.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series': 'Series',
                            'series_id': 'Series ID'
                        })
                        
                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_melted).mark_line().encode(
                            x='Date:T',
                            y=alt.Y('Value:Q'),
                            color='Series:N'
                        ).properties(
                            width=1000,
                            height=600,
                        ).configure_legend(
                            orient='bottom',
                            labelLimit=0
                        )
                        st.altair_chart(chart, use_container_width=True)

            with st.expander(f'Information'):

                if st.button("Fetch Data", key="employmentbyindustry_information"):
                    with st.spinner("Fetching data..."):
                        fred_data = fetch_data_information()

                        series_mapping = {
                            'CES5051100001': 'Publishing Industries, Except Internet',
                            'CES5051200001': 'Motion Picture & Sound Recording Industries',
                            'CES5051500001': 'Broadcasting, Except Internet',
                            'CES5051700001': 'Telecommunications',
                            'CES5051800001': 'Data Processing, Hosting & Related Services',
                            'CES5051900001': 'Other Information Services',
                        }
                                                
                        combined_df = pd.DataFrame()

                        for series_id, observations in fred_data.items():
                            temp_df = pd.DataFrame(observations)
                            temp_df['date'] = pd.to_datetime(temp_df['date'])
                            temp_df.set_index('date', inplace=True)
                            temp_df.rename(columns={'value': series_mapping[series_id]}, inplace=True)
                            
                            if combined_df.empty:
                                combined_df = temp_df
                            else:
                                combined_df = combined_df.join(temp_df[series_mapping[series_id]], how='outer')

                        combined_df.reset_index(inplace=True)
                        
                        df = combined_df.copy()
                        df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

                        df_melted = df.melt(id_vars=['date'], var_name='series', value_name='value')

                        df_melted = df_melted.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series': 'Series',
                            'series_id': 'Series ID'
                        })
                        
                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_melted).mark_line().encode(
                            x='Date:T',
                            y=alt.Y('Value:Q'),
                            color='Series:N'
                        ).properties(
                            width=1000,
                            height=600,
                        ).configure_legend(
                            orient='bottom',
                            labelLimit=0
                        )
                        st.altair_chart(chart, use_container_width=True)

            with st.expander(f'Financial Activities'):

                if st.button("Fetch Data", key="employmentbyindustry_financialactivities"):
                    with st.spinner("Fetching data..."):
                        fred_data = fetch_data_financialactivities()

                        series_mapping = {
                            'CES5552000001': 'Finance & Insurance',
                            'CES5553000001': 'Real Estate & Rental & Leasing',
                        }
                                                
                        combined_df = pd.DataFrame()

                        for series_id, observations in fred_data.items():
                            temp_df = pd.DataFrame(observations)
                            temp_df['date'] = pd.to_datetime(temp_df['date'])
                            temp_df.set_index('date', inplace=True)
                            temp_df.rename(columns={'value': series_mapping[series_id]}, inplace=True)
                            
                            if combined_df.empty:
                                combined_df = temp_df
                            else:
                                combined_df = combined_df.join(temp_df[series_mapping[series_id]], how='outer')

                        combined_df.reset_index(inplace=True)
                        
                        df = combined_df.copy()
                        df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

                        df_melted = df.melt(id_vars=['date'], var_name='series', value_name='value')

                        df_melted = df_melted.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series': 'Series',
                            'series_id': 'Series ID'
                        })
                        
                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_melted).mark_line().encode(
                            x='Date:T',
                            y=alt.Y('Value:Q'),
                            color='Series:N'
                        ).properties(
                            width=1000,
                            height=600,
                        ).configure_legend(
                            orient='bottom',
                            labelLimit=0
                        )
                        st.altair_chart(chart, use_container_width=True)

            with st.expander(f'Professional & Business Services'):

                if st.button("Fetch Data", key="employmentbyindustry_professionalbusinessservices"):
                    with st.spinner("Fetching data..."):
                        fred_data = fetch_data_professionalbusinessservices()

                        series_mapping = {
                            'CES6054000001': 'Professional & Technical Services',
                            'CES6055000001': 'Management of Companies & Enterprises',
                            'CES6056000001': 'Administrative & Waste Services',
                        }
                                                
                        combined_df = pd.DataFrame()

                        for series_id, observations in fred_data.items():
                            temp_df = pd.DataFrame(observations)
                            temp_df['date'] = pd.to_datetime(temp_df['date'])
                            temp_df.set_index('date', inplace=True)
                            temp_df.rename(columns={'value': series_mapping[series_id]}, inplace=True)
                            
                            if combined_df.empty:
                                combined_df = temp_df
                            else:
                                combined_df = combined_df.join(temp_df[series_mapping[series_id]], how='outer')

                        combined_df.reset_index(inplace=True)
                        
                        df = combined_df.copy()
                        df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

                        df_melted = df.melt(id_vars=['date'], var_name='series', value_name='value')

                        df_melted = df_melted.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series': 'Series',
                            'series_id': 'Series ID'
                        })
                        
                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_melted).mark_line().encode(
                            x='Date:T',
                            y=alt.Y('Value:Q'),
                            color='Series:N'
                        ).properties(
                            width=1000,
                            height=600,
                        ).configure_legend(
                            orient='bottom',
                            labelLimit=0
                        )
                        st.altair_chart(chart, use_container_width=True)

            with st.expander(f'Education & Health Services'):

                if st.button("Fetch Data", key="employmentbyindustry_educationhealthservices"):
                    with st.spinner("Fetching data..."):
                        fred_data = fetch_data_educationhealthservices()

                        series_mapping = {
                            'CES6561000001': 'Educational Services',
                            'CES6562000001': 'Health Care & Social Assistance',
                        }
                                                
                        combined_df = pd.DataFrame()

                        for series_id, observations in fred_data.items():
                            temp_df = pd.DataFrame(observations)
                            temp_df['date'] = pd.to_datetime(temp_df['date'])
                            temp_df.set_index('date', inplace=True)
                            temp_df.rename(columns={'value': series_mapping[series_id]}, inplace=True)
                            
                            if combined_df.empty:
                                combined_df = temp_df
                            else:
                                combined_df = combined_df.join(temp_df[series_mapping[series_id]], how='outer')

                        combined_df.reset_index(inplace=True)
                        
                        df = combined_df.copy()
                        df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

                        df_melted = df.melt(id_vars=['date'], var_name='series', value_name='value')

                        df_melted = df_melted.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series': 'Series',
                            'series_id': 'Series ID'
                        })
                        
                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_melted).mark_line().encode(
                            x='Date:T',
                            y=alt.Y('Value:Q'),
                            color='Series:N'
                        ).properties(
                            width=1000,
                            height=600,
                        ).configure_legend(
                            orient='bottom',
                            labelLimit=0
                        )
                        st.altair_chart(chart, use_container_width=True)

            with st.expander(f'Leisure & Hospitality'):

                if st.button("Fetch Data", key="employmentbyindustry_leisurehospitality"):
                    with st.spinner("Fetching data..."):
                        fred_data = fetch_data_leisurehospitality()

                        series_mapping = {
                            'CES7071000001': 'Arts, Entertainment & Recreation',
                            'CES7072000001': 'Accommodations & Food Services',
                        }
                                                
                        combined_df = pd.DataFrame()

                        for series_id, observations in fred_data.items():
                            temp_df = pd.DataFrame(observations)
                            temp_df['date'] = pd.to_datetime(temp_df['date'])
                            temp_df.set_index('date', inplace=True)
                            temp_df.rename(columns={'value': series_mapping[series_id]}, inplace=True)
                            
                            if combined_df.empty:
                                combined_df = temp_df
                            else:
                                combined_df = combined_df.join(temp_df[series_mapping[series_id]], how='outer')

                        combined_df.reset_index(inplace=True)
                        
                        df = combined_df.copy()
                        df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

                        df_melted = df.melt(id_vars=['date'], var_name='series', value_name='value')

                        df_melted = df_melted.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series': 'Series',
                            'series_id': 'Series ID'
                        })
                        
                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_melted).mark_line().encode(
                            x='Date:T',
                            y=alt.Y('Value:Q'),
                            color='Series:N'
                        ).properties(
                            width=1000,
                            height=600,
                        ).configure_legend(
                            orient='bottom',
                            labelLimit=0
                        )
                        st.altair_chart(chart, use_container_width=True)

            with st.expander(f'Other Services'):

                if st.button("Fetch Data", key="employmentbyindustry_otherservices"):
                    with st.spinner("Fetching data..."):
                        fred_data = fetch_data_otherservices()

                        series_mapping = {
                            'CES8081100001': 'Repair & Maintenance',
                            'CES8081200001': 'Personal & Laundry Services',
                            'CES8081300001': 'Membership Associations & Organizations',
                        }
                                                
                        combined_df = pd.DataFrame()

                        for series_id, observations in fred_data.items():
                            temp_df = pd.DataFrame(observations)
                            temp_df['date'] = pd.to_datetime(temp_df['date'])
                            temp_df.set_index('date', inplace=True)
                            temp_df.rename(columns={'value': series_mapping[series_id]}, inplace=True)
                            
                            if combined_df.empty:
                                combined_df = temp_df
                            else:
                                combined_df = combined_df.join(temp_df[series_mapping[series_id]], how='outer')

                        combined_df.reset_index(inplace=True)
                        
                        df = combined_df.copy()
                        df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

                        df_melted = df.melt(id_vars=['date'], var_name='series', value_name='value')

                        df_melted = df_melted.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series': 'Series',
                            'series_id': 'Series ID'
                        })
                        
                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_melted).mark_line().encode(
                            x='Date:T',
                            y=alt.Y('Value:Q'),
                            color='Series:N'
                        ).properties(
                            width=1000,
                            height=600,
                        ).configure_legend(
                            orient='bottom',
                            labelLimit=0
                        )
                        st.altair_chart(chart, use_container_width=True)

        with tab4a:
            st.markdown("<h1><b>Government</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            with st.expander(f'Federal'):


                if st.button("Fetch Data", key="employmentbyindustry_federal"):
                    with st.spinner("Fetching data..."):
                        fred_data = fetch_data_federalgovernment()

                        series_mapping = {
                            'CES9091100001': 'Federal, Except U.S. Postal Service',
                            'CES9091912001': 'U.S. Postal Service',
                        }
                                                
                        combined_df = pd.DataFrame()

                        for series_id, observations in fred_data.items():
                            temp_df = pd.DataFrame(observations)
                            temp_df['date'] = pd.to_datetime(temp_df['date'])
                            temp_df.set_index('date', inplace=True)
                            temp_df.rename(columns={'value': series_mapping[series_id]}, inplace=True)
                            
                            if combined_df.empty:
                                combined_df = temp_df
                            else:
                                combined_df = combined_df.join(temp_df[series_mapping[series_id]], how='outer')

                        combined_df.reset_index(inplace=True)
                        
                        df = combined_df.copy()
                        df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

                        df_melted = df.melt(id_vars=['date'], var_name='series', value_name='value')

                        df_melted = df_melted.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series': 'Series',
                            'series_id': 'Series ID'
                        })
                        
                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_melted).mark_line().encode(
                            x='Date:T',
                            y=alt.Y('Value:Q'),
                            color='Series:N'
                        ).properties(
                            width=1000,
                            height=600,
                        ).configure_legend(
                            orient='bottom',
                            labelLimit=0
                        )
                        st.altair_chart(chart, use_container_width=True)

            with st.expander(f'State Government'):

                if st.button("Fetch Data", key="employmentbyindustry_stategovernment"):
                    with st.spinner("Fetching data..."):
                        fred_data = fetch_data_stategovernment()

                        series_mapping = {
                            'CES9092161101': 'State Government Education',
                            'CES9092200001': 'State Government, Excluding Education',
                        }
                                                
                        combined_df = pd.DataFrame()

                        for series_id, observations in fred_data.items():
                            temp_df = pd.DataFrame(observations)
                            temp_df['date'] = pd.to_datetime(temp_df['date'])
                            temp_df.set_index('date', inplace=True)
                            temp_df.rename(columns={'value': series_mapping[series_id]}, inplace=True)
                            
                            if combined_df.empty:
                                combined_df = temp_df
                            else:
                                combined_df = combined_df.join(temp_df[series_mapping[series_id]], how='outer')

                        combined_df.reset_index(inplace=True)
                        
                        df = combined_df.copy()
                        df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

                        df_melted = df.melt(id_vars=['date'], var_name='series', value_name='value')

                        df_melted = df_melted.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series': 'Series',
                            'series_id': 'Series ID'
                        })
                        
                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_melted).mark_line().encode(
                            x='Date:T',
                            y=alt.Y('Value:Q'),
                            color='Series:N'
                        ).properties(
                            width=1000,
                            height=600,
                        ).configure_legend(
                            orient='bottom',
                            labelLimit=0
                        )
                        st.altair_chart(chart, use_container_width=True)

            with st.expander(f'Local Government'):

                if st.button("Fetch Data", key="employmentbyindustry_localgovernment"):
                    with st.spinner("Fetching data..."):
                        fred_data = fetch_data_localgovernment()
                    
                        series_mapping = {
                            'CES9093161101': 'Local Government Education',
                            'CES9093200001': 'Local Government, Excluding Education',
                        }
                                                
                        combined_df = pd.DataFrame()

                        for series_id, observations in fred_data.items():
                            temp_df = pd.DataFrame(observations)
                            temp_df['date'] = pd.to_datetime(temp_df['date'])
                            temp_df.set_index('date', inplace=True)
                            temp_df.rename(columns={'value': series_mapping[series_id]}, inplace=True)
                            
                            if combined_df.empty:
                                combined_df = temp_df
                            else:
                                combined_df = combined_df.join(temp_df[series_mapping[series_id]], how='outer')

                        combined_df.reset_index(inplace=True)
                        
                        df = combined_df.copy()
                        df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

                        df_melted = df.melt(id_vars=['date'], var_name='series', value_name='value')

                        df_melted = df_melted.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series': 'Series',
                            'series_id': 'Series ID'
                        })
                        
                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_melted).mark_line().encode(
                            x='Date:T',
                            y=alt.Y('Value:Q'),
                            color='Series:N'
                        ).properties(
                            width=1000,
                            height=600,
                        ).configure_legend(
                            orient='bottom',
                            labelLimit=0
                        )
                        st.altair_chart(chart, use_container_width=True)

# Display the page
show_labormarket_employmentbyindustry()