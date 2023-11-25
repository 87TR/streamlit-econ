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

def fetch_data_sa():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'TOTALSA': 'Total Vehicles SA',
        'LAUTOSA': 'Unit Auto Sales SA',
        'LTRUCKSA': 'Light Trucks SA',
        'HTRUCKSSAAR': 'Heavy Trucks SA',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '1990-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_nsa():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'TOTALNSA': 'Total Vehicles NSA',
        'LAUTONSA': 'Unit Auto Sales NSA',
        'LTRUCKNSA': 'Light Trucks NSA',
        'HTRUCKSNSA': 'Heavy Trucks NSA',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '1990-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def show_consumptionincome_autotrucksales():

    if st.session_state.get("authentication_status"):

        tab1a, tab2a,= st.tabs(["Seasonally Adjusted", "Not Seasonally Adjusted"])

        with tab1a:

            st.markdown("<h1><b>Auto & Truck Sales (SA)</b><small><small><small> | U.S. Bureau of Economic Analysis</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="autotrucksales_seasonallyadjusted"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_sa()

                    series_mapping_sa = {
                        'TOTALSA': 'Total Vehicles (Millions of Units)',
                        'LAUTOSA': 'Unit Auto Sales (Millions of Units)',
                        'LTRUCKSA': 'Light Trucks (Millions of Units)',
                        'HTRUCKSSAAR': 'Heavy Trucks (Millions of Units)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_sa[series_id]

                        df = pd.DataFrame(observations, columns=['date', 'value'])
                        df['indicator'] = indicator_name
                        df['series_id'] = series_id

                        df = df.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series_id': 'Series ID'
                        })

                        st.markdown(f'<h3><b>{indicator_name}</b> | Source: <a href="https://fred.stlouisfed.org/series/{series_id}">FRED</a></h3>', unsafe_allow_html=True)

                        st.markdown("<h4><b>Years</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df).mark_line().encode(
                            x='Date:T',
                            y='Value:Q'
                        ).properties(
                            width=1000,
                            height=600
                        )
                        st.altair_chart(chart)

                        df = df.sort_values(by='Date', ascending=False)
                        df = df.reset_index(drop=True)
                        df = df.head(48)
                        use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                        st.dataframe(df[['Date', 'Value', 'Indicator', 'Series ID']], use_container_width=use_container_width)

        with tab2a:

            st.markdown("<h1><b>Auto & Truck Sales (NSA)</b><small><small><small> | U.S. Bureau of Economic Analysis</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="autotrucksales_notseasonallyadjusted"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_nsa()

                    series_mapping_nsa = {
                        'TOTALNSA': 'Total Vehicles (Thousands of Units)',
                        'LAUTONSA': 'Unit Auto Sales (Thousands of Units)',
                        'LTRUCKNSA': 'Light Trucks (Thousands of Units)',
                        'HTRUCKSNSA': 'Heavy Trucks (Thousands of Units)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_nsa[series_id]

                        df = pd.DataFrame(observations, columns=['date', 'value'])
                        df['indicator'] = indicator_name
                        df['series_id'] = series_id

                        df = df.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series_id': 'Series ID'
                        })

                        st.markdown(f'<h3><b>{indicator_name}</b> | Source: <a href="https://fred.stlouisfed.org/series/{series_id}">FRED</a></h3>', unsafe_allow_html=True)

                        st.markdown("<h4><b>Years</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df).mark_line().encode(
                            x='Date:T',
                            y='Value:Q'
                        ).properties(
                            width=1000,
                            height=600
                        )

                        st.altair_chart(chart)

                        df = df.sort_values(by='Date', ascending=False)
                        df = df.reset_index(drop=True)
                        df = df.head(48)
                        use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                        st.dataframe(df[['Date', 'Value', 'Indicator', 'Series ID']], use_container_width=use_container_width)
            
# Display the page
show_consumptionincome_autotrucksales()