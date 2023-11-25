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

def fetch_data_index():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'PCEPI': 'Personal Consumption Expenditures',
        'PCEPILFE': 'PCE Excluding Food & Energy (Core PCE)',
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

def fetch_data_relatedmetrics():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'DGDSRG3M086SBEA': 'Goods',
        'DSERRG3M086SBEA': 'Services',
        'DFXARG3M086SBEA': 'Food',
        'DNRGRG3M086SBEA': 'Energy Goods and Services',
        'DPCMRG3M086SBEA': 'Market-based PCE',
        'DPCXRG3M086SBEA': 'Market-based PCE Excluding Food and Energy (Core)',
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

def show_inflation_pcepriceindex():

    if st.session_state.get("authentication_status"):

        tab1a, tab2a, = st.tabs(["Index", "Related Metrics"])

        with tab1a:

            st.markdown("<h1><b>PCE Index</b><small><small><small> | U.S. Bureau of Economic Analysis</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="pcepriceindex_index"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_index()

                    series_mapping_sa = {
                        'PCEPI': 'Personal Consumption Expenditures',
                        'PCEPILFE': 'PCE Excluding Food & Energy (Core)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_sa[series_id]

                        df = pd.DataFrame(observations, columns=['date', 'value'])
                        df['indicator'] = indicator_name
                        df['series_id'] = series_id

                        df_pcepriceindex = df.copy()
                        df_pcepriceindex = df_pcepriceindex[['date', 'value', 'series_id', 'indicator']]
                        
                        df_pcepriceindex['date'] = pd.to_datetime(df_pcepriceindex['date'])
                        df_pcepriceindex['value'] = pd.to_numeric(df_pcepriceindex['value'], errors='coerce')
                        df_pcepriceindex.sort_values(by='date', inplace=True)

                        df_pcepriceindex['mm_change'] = df_pcepriceindex['value'].diff()
                        df_pcepriceindex['mm_change_perc'] = (df_pcepriceindex['mm_change'] / df_pcepriceindex['value'].shift(1)) * 100
                        df_pcepriceindex['mm_change_perc_decimal'] = df_pcepriceindex['mm_change_perc'].round(1)

                        df_pcepriceindex['yy_change'] = df_pcepriceindex['value'] - df_pcepriceindex['value'].shift(12)
                        df_pcepriceindex['yy_change_perc'] = (df_pcepriceindex['yy_change'] / df_pcepriceindex['value'].shift(12)) * 100
                        df_pcepriceindex['yy_change_perc_decimal'] = df_pcepriceindex['yy_change_perc'].round(1)

                        df_pcepriceindex.sort_values(by='date', inplace=True, ascending=False)
                        df_pcepriceindex['date'] = df_pcepriceindex['date'].dt.strftime('%Y-%m-%d')

                        df_pcepriceindex = df_pcepriceindex.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series_id': 'Series ID',
                            'mm_change': 'M/M Change',
                            'mm_change_perc': 'M/M Change %',
                            'yy_change': 'Y/Y Change',
                            'yy_change_perc': 'Y/Y Change %',
                        })

                        st.markdown(f'<h3><b>{indicator_name}</b> | Source: <a href="https://fred.stlouisfed.org/series/{series_id}">FRED</a></h3>', unsafe_allow_html=True)

                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_pcepriceindex).mark_line().encode(
                            x='Date:T',
                            y='Y/Y Change %:Q'
                        ).properties(
                            width=1000,
                            height=600
                        )
                        st.altair_chart(chart)

                        st.markdown("<h4><b>Change (M/M)</4></h1>", unsafe_allow_html=True)
                        bar_chart = alt.Chart(df_pcepriceindex.head(156)).mark_bar().encode(
                            x='Date:T',
                            y='M/M Change %:Q'
                        ).properties(
                            width=1000,
                            height=600
                        )
                        st.altair_chart(bar_chart)

                        df_pcepriceindex = df_pcepriceindex.sort_values(by='Date', ascending=False)
                        df_pcepriceindex = df_pcepriceindex.reset_index(drop=True)
                        df_pcepriceindex = df_pcepriceindex.head(48)
                        use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                        st.dataframe(df_pcepriceindex[['Date', 'Indicator', 'Series ID', 'Value', 'M/M Change %', 'Y/Y Change %']], use_container_width=use_container_width)

        with tab2a:

            st.markdown("<h1><b>Related Metrics</b><small><small><small> | U.S. Bureau of Economic Analysis</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="pcepriceindex_relatedmetrics"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_relatedmetrics()

                    series_mapping_sa = {
                        'DGDSRG3M086SBEA': 'Goods',
                        'DSERRG3M086SBEA': 'Services',
                        'DFXARG3M086SBEA': 'Food',
                        'DNRGRG3M086SBEA': 'Energy Goods and Services',
                        'DPCMRG3M086SBEA': 'Market-based PCE',
                        'DPCXRG3M086SBEA': 'Market-based PCE Excluding Food and Energy (Core)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_sa[series_id]

                        df = pd.DataFrame(observations, columns=['date', 'value'])
                        df['indicator'] = indicator_name
                        df['series_id'] = series_id

                        df_pcepriceindex = df.copy()
                        df_pcepriceindex = df_pcepriceindex[['date', 'value', 'series_id', 'indicator']]
                        
                        df_pcepriceindex['date'] = pd.to_datetime(df_pcepriceindex['date'])
                        df_pcepriceindex['value'] = pd.to_numeric(df_pcepriceindex['value'], errors='coerce')
                        df_pcepriceindex.sort_values(by='date', inplace=True)

                        df_pcepriceindex['mm_change'] = df_pcepriceindex['value'].diff()
                        df_pcepriceindex['mm_change_perc'] = (df_pcepriceindex['mm_change'] / df_pcepriceindex['value'].shift(1)) * 100
                        df_pcepriceindex['mm_change_perc_decimal'] = df_pcepriceindex['mm_change_perc'].round(1)

                        df_pcepriceindex['yy_change'] = df_pcepriceindex['value'] - df_pcepriceindex['value'].shift(12)
                        df_pcepriceindex['yy_change_perc'] = (df_pcepriceindex['yy_change'] / df_pcepriceindex['value'].shift(12)) * 100
                        df_pcepriceindex['yy_change_perc_decimal'] = df_pcepriceindex['yy_change_perc'].round(1)

                        df_pcepriceindex.sort_values(by='date', inplace=True, ascending=False)
                        df_pcepriceindex['date'] = df_pcepriceindex['date'].dt.strftime('%Y-%m-%d')

                        df_pcepriceindex = df_pcepriceindex.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series_id': 'Series ID',
                            'mm_change': 'M/M Change',
                            'mm_change_perc': 'M/M Change %',
                            'yy_change': 'Y/Y Change',
                            'yy_change_perc': 'Y/Y Change %',
                        })

                        st.markdown(f'<h3><b>{indicator_name}</b> | Source: <a href="https://fred.stlouisfed.org/series/{series_id}">FRED</a></h3>', unsafe_allow_html=True)

                        st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                        chart = alt.Chart(df_pcepriceindex).mark_line().encode(
                            x='Date:T',
                            y='Y/Y Change %:Q'
                        ).properties(
                            width=1000,
                            height=600
                        )
                        st.altair_chart(chart)

                        st.markdown("<h4><b>Change (M/M)</4></h1>", unsafe_allow_html=True)
                        bar_chart = alt.Chart(df_pcepriceindex.head(156)).mark_bar().encode(
                            x='Date:T',
                            y='M/M Change %:Q'
                        ).properties(
                            width=1000,
                            height=600
                        )
                        st.altair_chart(bar_chart)

                        df_pcepriceindex = df_pcepriceindex.sort_values(by='Date', ascending=False)
                        df_pcepriceindex = df_pcepriceindex.reset_index(drop=True)
                        df_pcepriceindex = df_pcepriceindex.head(48)
                        use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                        st.dataframe(df_pcepriceindex[['Date', 'Indicator', 'Series ID', 'Value', 'M/M Change %', 'Y/Y Change %']], use_container_width=use_container_width)

# Display the page
show_inflation_pcepriceindex()