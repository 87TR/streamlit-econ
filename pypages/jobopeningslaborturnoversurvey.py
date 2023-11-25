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

def fetch_data_jobopenings():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'JTSJOL': 'Total Nonfarm (Thousands)',
        'JTS1000JOL': 'Total Private (Thousands)',
        'JTS2300JOL': 'Construction (Thousands)',
        'JTS3000JOL': 'Manufacturing (Thousands)',
        'JTS4000JOL': 'Trade, Transportation, and Utilities (Thousands)',
        'JTS540099JOL': 'Professional and Business Services (Thousands)',
        'JTS6000JOL': 'Education and Health Services (Thousands)',
        'JTS7000JOL': 'Leisure and Hospitality (Thousands)',
        'JTS9000JOL': 'Government (Thousands)',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '1970-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_hires():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'JTSHIL': 'Total Nonfarm (Thousands)',
        'JTS1000HIL': 'Total Private (Thousands)',
        'JTS2300HIL': 'Construction (Thousands)',
        'JTS3000HIL': 'Manufacturing (Thousands)',
        'JTS4000HIL': 'Trade, Transportation, and Utilities (Thousands)',
        'JTS540099HIL': 'Professional and Business Services (Thousands)',
        'JTS6000HIL': 'Education and Health Services (Thousands)',
        'JTS7000HIL': 'Leisure and Hospitality (Thousands)',
        'JTS9000HIL': 'Government (Thousands)',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '1970-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_layoffsanddischarges():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'JTSLDL': 'Total Nonfarm (Thousands)',
        'JTS1000LDL': 'Total Private (Thousands)',
        'JTS9000LDL': 'Government (Thousands)',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '1970-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_quits():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'JTSQUL': 'Total Nonfarm (Thousands)',
        'JTS1000QUL': 'Total Private (Thousands)',
        'JTS2300QUL': 'Construction (Thousands)',
        'JTS3000QUL': 'Manufacturing (Thousands)',
        'JTS4000QUL': 'Trade, Transportation, and Utilities (Thousands)',
        'JTS540099QUL': 'Professional and Business Services (Thousands)',
        'JTS6000QUL': 'Education and Health Services (Thousands)',
        'JTS7000QUL': 'Leisure and Hospitality (Thousands)',
        'JTS9000QUL': 'Government (Thousands)',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '1970-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_separations():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'JTSTSL': 'Total Nonfarm (Thousands)',
        'JTS1000TSL': 'Total Private (Thousands)',
        'JTS2300TSL': 'Construction (Thousands)',
        'JTS3000TSL': 'Manufacturing (Thousands)',
        'JTS4000TSL': 'Trade, Transportation, and Utilities (Thousands)',
        'JTS540099TSL': 'Professional and Business Services (Thousands)',
        'JTS6000TSL': 'Education and Health Services (Thousands)',
        'JTS7000TSL': 'Leisure and Hospitality (Thousands)',
        'JTS9000TSL': 'Government (Thousands)',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '1970-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def fetch_data_otherseparations():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'JTSOSL': 'Total Nonfarm (Thousands)',
        'JTS1000OSL': 'Total Private (Thousands)',
        'JTS2300OSL': 'Construction (Thousands)',
        'JTS3000OSL': 'Manufacturing (Thousands)',
        'JTS4000OSL': 'Trade, Transportation, and Utilities (Thousands)',
        'JTS540099OSL': 'Professional and Business Services (Thousands)',
        'JTS6000OSL': 'Education and Health Services (Thousands)',
        'JTS7000OSL': 'Leisure and Hospitality (Thousands)',
        'JTS9000OSL': 'Government (Thousands)',
    }

    fred_data = {}

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    for series_id in series_mapping.keys():
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '1970-01-01',
            'observation_end': current_date,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            data['indicator'] = series_mapping[series_id]
            fred_data[series_id] = data['observations']

    return fred_data

def show_labormarket_jobopeningslaborturnoversurvey():

    if st.session_state.get("authentication_status"):

        tab1a, tab2a, tab3a, tab4a, tab5a, tab6a = st.tabs(["Job Openings", "Hires", "Layoffs and Discharges", "Quits", "Separations", "Other Separations"])

        with tab1a:
            st.markdown("<h1><b>Job Openings</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="jobopeninglaborturnoversurvey_jobopenings"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_jobopenings()

                    series_mapping_jobopenings = {
                        'JTSJOL': 'Total Nonfarm (Thousands)',
                        'JTS1000JOL': 'Total Private (Thousands)',
                        'JTS2300JOL': 'Construction (Thousands)',
                        'JTS3000JOL': 'Manufacturing (Thousands)',
                        'JTS4000JOL': 'Trade, Transportation, and Utilities (Thousands)',
                        'JTS540099JOL': 'Professional and Business Services (Thousands)',
                        'JTS6000JOL': 'Education and Health Services (Thousands)',
                        'JTS7000JOL': 'Leisure and Hospitality (Thousands)',
                        'JTS9000JOL': 'Government (Thousands)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_jobopenings[series_id]

                        df = pd.DataFrame(observations, columns=['date', 'value'])
                        df['indicator'] = indicator_name
                        df['series_id'] = series_id

                        df = df.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series_id': 'Series ID'
                        })

                        with st.expander(f'{indicator_name}'):

                            st.markdown(f'<h3><b>{indicator_name}</b> | Source: <a href="https://fred.stlouisfed.org/series/{series_id}">FRED</a></h3>', unsafe_allow_html=True)

                            df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
                            df['Change'] = df['Value'] - df['Value'].shift(1)
                            df['Change (%)'] = (df['Value'] - df['Value'].shift(1)) / df['Value'].shift(1) * 100
                            df['Change (%)'] = df['Change (%)'].round(2)

                            st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                            chart = alt.Chart(df).mark_line().encode(
                                x='Date:T',
                                y='Value:Q'
                            ).properties(
                                width=1000,
                                height=600
                            )
                            st.altair_chart(chart)

                            st.markdown("<h4><b>Change (W/W)</4></h1>", unsafe_allow_html=True)
                            bar_chart = alt.Chart(df.tail(156)).mark_bar().encode(
                                x='Date:T',
                                y='Change:Q'
                            ).properties(
                                width=1000,
                                height=600
                            )
                            st.altair_chart(bar_chart)

                            df = df.sort_values(by='Date', ascending=False)
                            df = df.reset_index(drop=True)
                            df = df.head(156)
                            use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                            st.dataframe(df[['Date', 'Value', 'Change', 'Change (%)', 'Indicator', 'Series ID']], use_container_width=use_container_width)

        with tab2a:
            st.markdown("<h1><b>Hires</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="jobopeninglaborturnoversurvey_hires"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_hires()

                    series_mapping_hires = {
                        'JTSHIL': 'Total Nonfarm (Thousands)',
                        'JTS1000HIL': 'Total Private (Thousands)',
                        'JTS2300HIL': 'Construction (Thousands)',
                        'JTS3000HIL': 'Manufacturing (Thousands)',
                        'JTS4000HIL': 'Trade, Transportation, and Utilities (Thousands)',
                        'JTS540099HIL': 'Professional and Business Services (Thousands)',
                        'JTS6000HIL': 'Education and Health Services (Thousands)',
                        'JTS7000HIL': 'Leisure and Hospitality (Thousands)',
                        'JTS9000HIL': 'Government (Thousands)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_hires[series_id]

                        df = pd.DataFrame(observations, columns=['date', 'value'])
                        df['indicator'] = indicator_name
                        df['series_id'] = series_id

                        df = df.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series_id': 'Series ID'
                        })

                        with st.expander(f'{indicator_name}'):

                            st.markdown(f'<h3><b>{indicator_name}</b> | Source: <a href="https://fred.stlouisfed.org/series/{series_id}">FRED</a></h3>', unsafe_allow_html=True)

                            df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
                            df['Change'] = df['Value'] - df['Value'].shift(1)
                            df['Change (%)'] = (df['Value'] - df['Value'].shift(1)) / df['Value'].shift(1) * 100
                            df['Change (%)'] = df['Change (%)'].round(2)

                            st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                            chart = alt.Chart(df).mark_line().encode(
                                x='Date:T',
                                y='Value:Q'
                            ).properties(
                                width=1000,
                                height=600
                            )
                            st.altair_chart(chart)

                            st.markdown("<h4><b>Change (W/W)</4></h1>", unsafe_allow_html=True)
                            bar_chart = alt.Chart(df.tail(156)).mark_bar().encode(
                                x='Date:T',
                                y='Change:Q'
                            ).properties(
                                width=1000,
                                height=600
                            )
                            st.altair_chart(bar_chart)
                            
                            df = df.sort_values(by='Date', ascending=False)
                            df = df.reset_index(drop=True)
                            df = df.head(156)
                            use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                            st.dataframe(df[['Date', 'Value', 'Change', 'Change (%)', 'Indicator', 'Series ID']], use_container_width=use_container_width)

        with tab3a:
            st.markdown("<h1><b>Layoffs and Discharges</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="jobopeninglaborturnoversurvey_layoffsanddischarges"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_layoffsanddischarges()

                    series_mapping_layoffsanddischarges = {
                        'JTSLDL': 'Total Nonfarm (Thousands)',
                        'JTS1000LDL': 'Total Private (Thousands)',
                        'JTS9000LDL': 'Government (Thousands)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_layoffsanddischarges[series_id]

                        df = pd.DataFrame(observations, columns=['date', 'value'])
                        df['indicator'] = indicator_name
                        df['series_id'] = series_id

                        df = df.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series_id': 'Series ID'
                        })

                        with st.expander(f'{indicator_name}'):

                            st.markdown(f'<h3><b>{indicator_name}</b> | Source: <a href="https://fred.stlouisfed.org/series/{series_id}">FRED</a></h3>', unsafe_allow_html=True)

                            df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
                            df['Change'] = df['Value'] - df['Value'].shift(1)
                            df['Change (%)'] = (df['Value'] - df['Value'].shift(1)) / df['Value'].shift(1) * 100
                            df['Change (%)'] = df['Change (%)'].round(2)

                            st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                            chart = alt.Chart(df).mark_line().encode(
                                x='Date:T',
                                y='Value:Q'
                            ).properties(
                                width=1000,
                                height=600
                            )
                            st.altair_chart(chart)

                            st.markdown("<h4><b>Change (W/W)</4></h1>", unsafe_allow_html=True)
                            bar_chart = alt.Chart(df.tail(156)).mark_bar().encode(
                                x='Date:T',
                                y='Change:Q'
                            ).properties(
                                width=1000,
                                height=600
                            )
                            st.altair_chart(bar_chart)
                            
                            df = df.sort_values(by='Date', ascending=False)
                            df = df.reset_index(drop=True)
                            df = df.head(156)
                            use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                            st.dataframe(df[['Date', 'Value', 'Change', 'Change (%)', 'Indicator', 'Series ID']], use_container_width=use_container_width)
        
        with tab4a:
            st.markdown("<h1><b>Quits</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="jobopeninglaborturnoversurvey_quits"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_quits()

                    series_mapping_quits = {
                        'JTSQUL': 'Total Nonfarm (Thousands)',
                        'JTS1000QUL': 'Total Private (Thousands)',
                        'JTS2300QUL': 'Construction (Thousands)',
                        'JTS3000QUL': 'Manufacturing (Thousands)',
                        'JTS4000QUL': 'Trade, Transportation, and Utilities (Thousands)',
                        'JTS540099QUL': 'Professional and Business Services (Thousands)',
                        'JTS6000QUL': 'Education and Health Services (Thousands)',
                        'JTS7000QUL': 'Leisure and Hospitality (Thousands)',
                        'JTS9000QUL': 'Government (Thousands)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_quits[series_id]

                        df = pd.DataFrame(observations, columns=['date', 'value'])
                        df['indicator'] = indicator_name
                        df['series_id'] = series_id

                        df = df.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series_id': 'Series ID'
                        })

                        with st.expander(f'{indicator_name}'):

                            st.markdown(f'<h3><b>{indicator_name}</b> | Source: <a href="https://fred.stlouisfed.org/series/{series_id}">FRED</a></h3>', unsafe_allow_html=True)

                            df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
                            df['Change'] = df['Value'] - df['Value'].shift(1)
                            df['Change (%)'] = (df['Value'] - df['Value'].shift(1)) / df['Value'].shift(1) * 100
                            df['Change (%)'] = df['Change (%)'].round(2)

                            st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                            chart = alt.Chart(df).mark_line().encode(
                                x='Date:T',
                                y='Value:Q'
                            ).properties(
                                width=1000,
                                height=600
                            )
                            st.altair_chart(chart)

                            st.markdown("<h4><b>Change (W/W)</4></h1>", unsafe_allow_html=True)
                            bar_chart = alt.Chart(df.tail(156)).mark_bar().encode(
                                x='Date:T',
                                y='Change:Q'
                            ).properties(
                                width=1000,
                                height=600
                            )
                            st.altair_chart(bar_chart)
                            
                            df = df.sort_values(by='Date', ascending=False)
                            df = df.reset_index(drop=True)
                            df = df.head(156)
                            use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                            st.dataframe(df[['Date', 'Value', 'Change', 'Change (%)', 'Indicator', 'Series ID']], use_container_width=use_container_width)

        with tab5a:
            st.markdown("<h1><b>Separations</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="jobopeninglaborturnoversurvey_separations"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_separations()

                    series_mapping_separations = {
                        'JTSTSL': 'Total Nonfarm (Thousands)',
                        'JTS1000TSL': 'Total Private (Thousands)',
                        'JTS2300TSL': 'Construction (Thousands)',
                        'JTS3000TSL': 'Manufacturing (Thousands)',
                        'JTS4000TSL': 'Trade, Transportation, and Utilities (Thousands)',
                        'JTS540099TSL': 'Professional and Business Services (Thousands)',
                        'JTS6000TSL': 'Education and Health Services (Thousands)',
                        'JTS7000TSL': 'Leisure and Hospitality (Thousands)',
                        'JTS9000TSL': 'Government (Thousands)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_separations[series_id]

                        df = pd.DataFrame(observations, columns=['date', 'value'])
                        df['indicator'] = indicator_name
                        df['series_id'] = series_id

                        df = df.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series_id': 'Series ID'
                        })

                        with st.expander(f'{indicator_name}'):

                            st.markdown(f'<h3><b>{indicator_name}</b> | Source: <a href="https://fred.stlouisfed.org/series/{series_id}">FRED</a></h3>', unsafe_allow_html=True)

                            df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
                            df['Change'] = df['Value'] - df['Value'].shift(1)
                            df['Change (%)'] = (df['Value'] - df['Value'].shift(1)) / df['Value'].shift(1) * 100
                            df['Change (%)'] = df['Change (%)'].round(2)

                            st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                            chart = alt.Chart(df).mark_line().encode(
                                x='Date:T',
                                y='Value:Q'
                            ).properties(
                                width=1000,
                                height=600
                            )
                            st.altair_chart(chart)

                            st.markdown("<h4><b>Change (W/W)</4></h1>", unsafe_allow_html=True)
                            bar_chart = alt.Chart(df.tail(156)).mark_bar().encode(
                                x='Date:T',
                                y='Change:Q'
                            ).properties(
                                width=1000,
                                height=600
                            )
                            st.altair_chart(bar_chart)
                            
                            df = df.sort_values(by='Date', ascending=False)
                            df = df.reset_index(drop=True)
                            df = df.head(156)
                            use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                            st.dataframe(df[['Date', 'Value', 'Change', 'Change (%)', 'Indicator', 'Series ID']], use_container_width=use_container_width)

        with tab6a:
            st.markdown("<h1><b>Other Separations</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="jobopeninglaborturnoversurvey_otherseparations"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_otherseparations()

                    series_mapping_otherseparations = {
                        'JTSOSL': 'Total Nonfarm (Thousands)',
                        'JTS1000OSL': 'Total Private (Thousands)',
                        'JTS2300OSL': 'Construction (Thousands)',
                        'JTS3000OSL': 'Manufacturing (Thousands)',
                        'JTS4000OSL': 'Trade, Transportation, and Utilities (Thousands)',
                        'JTS540099OSL': 'Professional and Business Services (Thousands)',
                        'JTS6000OSL': 'Education and Health Services (Thousands)',
                        'JTS7000OSL': 'Leisure and Hospitality (Thousands)',
                        'JTS9000OSL': 'Government (Thousands)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_otherseparations[series_id]

                        df = pd.DataFrame(observations, columns=['date', 'value'])
                        df['indicator'] = indicator_name
                        df['series_id'] = series_id

                        df = df.rename(columns={
                            'date': 'Date',
                            'value': 'Value',
                            'indicator': 'Indicator',
                            'series_id': 'Series ID'
                        })

                        with st.expander(f'{indicator_name}'):

                            st.markdown(f'<h3><b>{indicator_name}</b> | Source: <a href="https://fred.stlouisfed.org/series/{series_id}">FRED</a></h3>', unsafe_allow_html=True)

                            df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
                            df['Change'] = df['Value'] - df['Value'].shift(1)
                            df['Change (%)'] = (df['Value'] - df['Value'].shift(1)) / df['Value'].shift(1) * 100
                            df['Change (%)'] = df['Change (%)'].round(2)

                            st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                            chart = alt.Chart(df).mark_line().encode(
                                x='Date:T',
                                y='Value:Q'
                            ).properties(
                                width=1000,
                                height=600
                            )
                            st.altair_chart(chart)

                            st.markdown("<h4><b>Change (W/W)</4></h1>", unsafe_allow_html=True)
                            bar_chart = alt.Chart(df.tail(156)).mark_bar().encode(
                                x='Date:T',
                                y='Change:Q'
                            ).properties(
                                width=1000,
                                height=600
                            )
                            st.altair_chart(bar_chart)
                            
                            df = df.sort_values(by='Date', ascending=False)
                            df = df.reset_index(drop=True)
                            df = df.head(156)
                            use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                            st.dataframe(df[['Date', 'Value', 'Change', 'Change (%)', 'Indicator', 'Series ID']], use_container_width=use_container_width)

# Display the page
show_labormarket_jobopeningslaborturnoversurvey()