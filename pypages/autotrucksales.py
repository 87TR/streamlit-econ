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

def fetch_data():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'TOTALSA': 'Total Vehicles',
        'LAUTOSA': 'Unit Auto Sales',
        'LTRUCKSA': 'Light Trucks',
        'HTRUCKSSAAR': 'Heavy Trucks',
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

def show_consumptionincome_autotrucksales():

    if st.session_state.get("authentication_status"):

        tab1a, = st.tabs(["Seasonally Adjusted"])

        with tab1a:

            st.markdown("<h1><b>Auto & Truck Sales</b><small><small><small> | U.S. Bureau of Economic Analysis</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="autotrucksales_seasonallyadjusted"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data()

                    series_mapping = {
                        'TOTALSA': 'Total Vehicles',
                        'LAUTOSA': 'Unit Auto Sales',
                        'LTRUCKSA': 'Light Trucks',
                        'HTRUCKSSAAR': 'Heavy Trucks',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping[series_id]

                        # Extract only the required columns
                        df = pd.DataFrame(observations, columns=['date', 'value'])
                        df['indicator'] = indicator_name
                        df['series_id'] = series_id

                        st.markdown(f"<h3><b>{indicator_name}</b></h3>", unsafe_allow_html=True)

                        chart = alt.Chart(df).mark_line().encode(
                            x='date:T',
                            y='value:Q'
                        ).properties(
                            width=1000,
                            height=600
                        )

                        st.altair_chart(chart)

                        use_container_width = st.checkbox(f"Use container width ({indicator_name})", value=True, key=f"use_container_width_{series_id}")
                        df = df.head(48)
                        df = df.reset_index(drop=True)
                        st.dataframe(df[['date', 'value', 'indicator', 'series_id']], use_container_width=use_container_width)
                        
# Display the page
show_consumptionincome_autotrucksales()