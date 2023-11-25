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

def fetch_data_rates():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'UNRATE': '16  Years & Over',
        'LNS14000024': '20 Years & Over',
        'LNS14000048': '25 Years & Over',
        'LNS14024230': '55 Years & Over',
        'LNS14100000': 'Full-Time Workers',
        'LNS14200000': 'Part-Time Workers',
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

def fetch_data_status():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'CLF16OV': 'Civilian Labor Force (Thousands)',
        'CE16OV': 'Employed (Thousands)',
        'UNEMPLOY': 'Unemployed (Thousands)',
        'LNS15000000': 'Not in Labor Force (Thousands)',
        'CIVPART': 'Participation Rate (Perc.)',
        'EMRATIO': 'Employment-Population Ratio',
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

def fetch_data_reason():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'LNS13023621': 'Job Losers (Thousands)',
        'LNS13023705': 'Job Leavers (Thousands)',
        'LNS13023557': 'Reentrants (Thousands)',
        'LNS13023569': 'New Entrants (Thousands)',
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

def fetch_data_duration():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'UEMPLT5': 'Less than 5 Weeks (Thousands)',
        'UEMP5TO14': '5 Weeks to 14 Weeks (Thousands)',
        'UEMP15T26': '15 Weeks to 26 Weeks (Thousands)',
        'UEMP27OV': '27 Weeks & over (Thousands)',
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

def fetch_data_parttime():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'LNS12032194': 'Part Time for Economic Reasons (Thousands)',
        'LNS12032195': 'Slack Work or Business Conditions (Thousands)',
        'LNS12032196': 'Could Only Find Part-Time Work (Thousands)',
        'LNS12005977': 'Part Time for Noneconomic Reasons (Thousands)',
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

def fetch_data_industry():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'PAYEMS': 'Total Private (Thousands)',
        'USPRIV': 'Goods Producing (Thousands)',
        'USGOOD': 'Mining & Logging (Thousands)',
        'CEU1000000001': 'Construction (Thousands)',
        'USCONS': 'Manufacturing (Thousands)',
        'MANEMP': 'Durable Goods (Thousands)',
        'DMANEMP': 'Motor Vehicles & Parts (Thousands)',
        'CES3133600101': 'Nondurable Goods (Thousands)',
        'NDMANEMP': 'Private Service-Providing (Thousands)',
        'CES0800000001': 'Wholesale Trade (Thousands)',
        'USWTRADE': 'Retail Trade (Thousands)',
        'USTRADE': 'Transportation & Warehousing (Thousands)',
        'CES4300000001': 'Information (Thousands)',
        'USINFO': 'Financial Activities (Thousands)',
        'USFIRE': 'Professional & Business Services (Thousands)',
        'USPBS': 'Temporary Help Services (Thousands)',
        'TEMPHELPS': 'Education & Health Services (Thousands)',
        'USEHS': 'Health Care & Social Assistance (Thousands)',
        'CES6562000001': 'Leisure & Hospitality (Thousands)',
        'USLAH': 'Other Services (Thousands)',
        'USSERV': 'Government (Thousands)',
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

def fetch_data_hoursearnings():
    api_key = authorization_fred
    base_url = 'https://api.stlouisfed.org/fred/series/observations'

    series_mapping = {
        'AWHAETP': 'Average Weekly Hours',
        'CES0500000003': 'Average Hourly Earnings ($)',
        'CES0500000011': 'Average Weekly Earnings ($)',
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

def show_labormarket_employmentsituation():

    if st.session_state.get("authentication_status"):

        tab1a, tab2a, tab3a, tab4a, tab5a, tab6a, tab7a = st.tabs(["Rates", "Status", "Reason", "Duration", "Part Time", "Industry", "Hours & Earnings"])

        with tab1a:
            st.markdown("<h1><b>Unemployment Rates</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="employmentsituation_rates"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_rates()

                    series_mapping_rates = {
                        'UNRATE': '16  Years & Over',
                        'LNS14000024': '20 Years & Over',
                        'LNS14000048': '25 Years & Over',
                        'LNS14024230': '55 Years & Over',
                        'LNS14100000': 'Full-Time Workers',
                        'LNS14200000': 'Part-Time Workers',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_rates[series_id]

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

                            st.markdown("<h4><b>Last 3 Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
                            line_chart_last_36_months = alt.Chart(df.tail(36)).mark_line().encode(
                                x='Date:T',
                                y='Value:Q'
                            ).properties(
                                width=1000,
                                height=600
                            )
                            st.altair_chart(line_chart_last_36_months)

                            df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

                            st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
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
                            df = df.head(156)
                            use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                            st.dataframe(df[['Date', 'Value', 'Indicator', 'Series ID']], use_container_width=use_container_width)

        with tab2a:
            st.markdown("<h1><b>Employment Status</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="employmentsituation_status"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_status()

                    series_mapping_status = {
                        'CLF16OV': 'Civilian Labor Force (Thousands)',
                        'CE16OV': 'Employed (Thousands)',
                        'UNEMPLOY': 'Unemployed (Thousands)',
                        'LNS15000000': 'Not in Labor Force (Thousands)',
                        'CIVPART': 'Participation Rate (Perc.)',
                        'EMRATIO': 'Employment-Population Ratio',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_status[series_id]

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

                            st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
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
                            df = df.head(156)
                            use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                            st.dataframe(df[['Date', 'Value', 'Indicator', 'Series ID']], use_container_width=use_container_width)

        with tab3a:
            st.markdown("<h1><b>Reason for Unemployment</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="employmentsituation_reason"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_reason()

                    series_mapping_reason = {
                        'LNS13023621': 'Job Losers (Thousands)',
                        'LNS13023705': 'Job Leavers (Thousands)',
                        'LNS13023557': 'Reentrants (Thousands)',
                        'LNS13023569': 'New Entrants (Thousands)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_reason[series_id]

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

                            st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
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
                            df = df.head(156)
                            use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                            st.dataframe(df[['Date', 'Value', 'Indicator', 'Series ID']], use_container_width=use_container_width)

        with tab4a:
            st.markdown("<h1><b>Duration of Unemployment</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="employmentsituation_duration"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_duration()

                    series_mapping_duration = {
                        'UEMPLT5': 'Less than 5 Weeks (Thousands)',
                        'UEMP5TO14': '5 Weeks to 14 Weeks (Thousands)',
                        'UEMP15T26': '15 Weeks to 26 Weeks (Thousands)',
                        'UEMP27OV': '27 Weeks & over (Thousands)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_duration[series_id]

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

                            st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
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
                            df = df.head(156)
                            use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                            st.dataframe(df[['Date', 'Value', 'Indicator', 'Series ID']], use_container_width=use_container_width)

        with tab5a:
            st.markdown("<h1><b>Employed Persons at Work Part Time</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="employmentsituation_parttime"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_parttime()

                    series_mapping_parttime = {
                        'LNS12032194': 'Part Time for Economic Reasons (Thousands)',
                        'LNS12032195': 'Slack Work or Business Conditions (Thousands)',
                        'LNS12032196': 'Could Only Find Part-Time Work (Thousands)',
                        'LNS12005977': 'Part Time for Noneconomic Reasons (Thousands)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_parttime[series_id]

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

                            st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
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
                            df = df.head(156)
                            use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                            st.dataframe(df[['Date', 'Value', 'Indicator', 'Series ID']], use_container_width=use_container_width)

        with tab6a:
            st.markdown("<h1><b>Employment by Industry</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="employmentsituation_industry"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_industry()

                    series_mapping_industry = {
                        'PAYEMS': 'Total Private (Thousands)',
                        'USPRIV': 'Goods Producing (Thousands)',
                        'USGOOD': 'Mining & Logging (Thousands)',
                        'CEU1000000001': 'Construction (Thousands)',
                        'USCONS': 'Manufacturing (Thousands)',
                        'MANEMP': 'Durable Goods (Thousands)',
                        'DMANEMP': 'Motor Vehicles & Parts (Thousands)',
                        'CES3133600101': 'Nondurable Goods (Thousands)',
                        'NDMANEMP': 'Private Service-Providing (Thousands)',
                        'CES0800000001': 'Wholesale Trade (Thousands)',
                        'USWTRADE': 'Retail Trade (Thousands)',
                        'USTRADE': 'Transportation & Warehousing (Thousands)',
                        'CES4300000001': 'Information (Thousands)',
                        'USINFO': 'Financial Activities (Thousands)',
                        'USFIRE': 'Professional & Business Services (Thousands)',
                        'USPBS': 'Temporary Help Services (Thousands)',
                        'TEMPHELPS': 'Education & Health Services (Thousands)',
                        'USEHS': 'Health Care & Social Assistance (Thousands)',
                        'CES6562000001': 'Leisure & Hospitality (Thousands)',
                        'USLAH': 'Other Services (Thousands)',
                        'USSERV': 'Government (Thousands)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_industry[series_id]

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

        with tab7a:
            st.markdown("<h1><b>Hours & Earnings</b><small><small><small> | U.S. Bureau of Labor Statistics</small></small></small></h1>", unsafe_allow_html=True)

            if st.button("Fetch Data", key="employmentsituation_hoursearnings"):
                with st.spinner("Fetching data..."):
                    fred_data = fetch_data_hoursearnings()

                    series_mapping_hoursearnings = {
                        'AWHAETP': 'Average Weekly Hours',
                        'CES0500000003': 'Average Hourly Earnings ($)',
                        'CES0500000011': 'Average Weekly Earnings ($)',
                    }

                    for series_id, observations in fred_data.items():
                        indicator_name = series_mapping_hoursearnings[series_id]

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

                            st.markdown("<h4><b>Years, Seasonally Adjusted</4></h1>", unsafe_allow_html=True)
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
                            df = df.head(156)
                            use_container_width = st.checkbox(f"Use container width", value=True, key=f"use_container_width_{series_id}")
                            st.dataframe(df[['Date', 'Value', 'Indicator', 'Series ID']], use_container_width=use_container_width)

# Display the page
show_labormarket_employmentsituation()