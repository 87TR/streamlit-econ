import credentials

import streamlit as st
import pandas as pd
import altair as alt

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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

def show_moneybankingcredit_h41():

    if st.session_state.get("authentication_status"):
        
        st.markdown("<h1><b>Federal Reserve Balance Sheet: Factors Affecting Reserve Balances (H.4.1)</b></h1>", unsafe_allow_html=True)

        tab_assets, tab_securitiesheldoutright, tab_treasurysecurities, tab_loans, tab_treasurygeneralaccount, tab_rarra, tab_usdliquidityswaps, tab_someholdings = st.tabs(["Assets", "Securities Held Outright", "Treasury Securities", "Loans", "Treasury General Account", "RA/RRA", "USD Liquidity Swaps", "SOMA Holdings"])

################################################
        with tab_assets:
            
            if st.button("Fetch Data", key="Assets"):

                # Query to retrieve rows
                conn = st.connection("postgresql", type="sql")
                query = f"SELECT * FROM h41_h41_observations WHERE tr87_series_name LIKE '%RESPPAL_N.WW%' OR tr87_series_name LIKE '%RESPPAL_XCH1_N.WW%' OR tr87_series_name LIKE '%RESPPAL_XCH52_N.WW%' ORDER BY tr87_series_name ASC;"
                df_RESPPAL = conn.query(query, ttl="60m")
                
                columns = {
                    'tr87_series_name': 'Series Name',
                    'tr87_time_period': 'Time Period',
                    'tr87_observation_value': 'Observation Value'
                }

                # Use the rename() method to change the column names
                df_RESPPAL = df_RESPPAL.rename(columns=columns)
                st.session_state.df_RESPPAL = df_RESPPAL

                # Check if 'df_RESPPAL' exists in session state
                if 'df_RESPPAL' not in st.session_state:
                    with st.spinner('Loading data...'):
                        df_RESPPAL = st.session_state.df_RESPPAL
                else:
                    df_RESPPAL = st.session_state.df_RESPPAL

                ########################

                #create chart
                color_palette = {
                    'domain': ['RESPPAL_N.WW', 'RESPPAL_XCH1_N.WW', 'RESPPAL_XCH52_N.WW'],
                    'range': ['#0074e4', '#D3D3D3', '#333333']
                }

                series_name_mapping = {
                    'RESPPAL_N.WW': 'RESPPAL',
                    'RESPPAL_XCH1_N.WW': 'Change (1W)',
                    'RESPPAL_XCH52_N.WW': 'Change (52W)'
                }

                # Create a new column 'New Series Name' with the mapped names
                df_RESPPAL.loc[:, 'Series Name'] = df_RESPPAL['Series Name'].map(series_name_mapping)

                # Create chart with custom series names in legend
                time_series_chart = alt.Chart(df_RESPPAL).mark_line().encode(
                    x='Time Period:T',
                    y='Observation Value:Q',
                    color=alt.Color('Series Name:N', scale=alt.Scale(domain=list(series_name_mapping.values()), range=color_palette['range'])),
                    tooltip=[
                        'Series Name:N',
                        alt.Tooltip('Time Period:T', format='%Y-%m-%d'),
                        alt.Tooltip('Observation Value:Q', format=',')
                    ]
                ).interactive().properties(
                    title="RESPPAL: Since 31 December 2012",
                    width=1200,
                    height=600
                )

                st.altair_chart(time_series_chart)
               
                #display table
                df_RESPPAL_filter = df_RESPPAL[df_RESPPAL['Series Name'] == 'RESPPAL']
                df_RESPPAL_filter.loc[:, 'Observation Value'] = pd.to_numeric(df_RESPPAL_filter['Observation Value'], errors='coerce')
                df_RESPPAL_filter_sorted = df_RESPPAL_filter.sort_values(by=['Series Name', 'Time Period'])
                latest_readings = df_RESPPAL_filter_sorted.groupby('Series Name').tail(100).reset_index(drop=True)
                latest_readings = latest_readings.sort_values(by=['Time Period', 'Series Name'], ascending=[False, False])
                latest_readings['Observation Value'] = latest_readings['Observation Value'].apply(lambda x: '{:,.0f}'.format(x))
                latest_readings = latest_readings.reset_index(drop=True)

                st.checkbox("Use container width", value=True, key="use_container_width_latest_readings")
                st.dataframe(latest_readings, use_container_width=st.session_state.use_container_width_latest_readings)
                
                st.markdown("<br>", unsafe_allow_html=True)

                ########################

                df_RESPPAL_10NOV2021 = df_RESPPAL[(df_RESPPAL['Series Name'] == 'RESPPAL') & (df_RESPPAL['Time Period'] >= '2021-11-10')].copy()
                df_RESPPAL_10NOV2021["Observation Value"] = pd.to_numeric(df_RESPPAL_10NOV2021["Observation Value"], errors='coerce')
                df_RESPPAL_10NOV2021["Since 10 Nov 2021 ($)"] = df_RESPPAL_10NOV2021["Observation Value"] - 8534292
                df_RESPPAL_10NOV2021["Since 10 Nov 2021 (%)"] = (df_RESPPAL_10NOV2021["Since 10 Nov 2021 ($)"] / 8534292 * 100).round(2)

                # chart
                base_chart = alt.Chart(df_RESPPAL_10NOV2021).encode(
                    x='Time Period:T'
                )
                line_since_10_nov_dollars = base_chart.mark_line().encode(
                    y='Since 10 Nov 2021 ($):Q',
                    color=alt.value('#0074e4')
                )
                line_since_10_nov_percent = base_chart.mark_line().encode(
                    y='Since 10 Nov 2021 (%):Q',
                    color=alt.value('#333333')
                )
                chart = alt.layer(line_since_10_nov_dollars, line_since_10_nov_percent).resolve_scale(
                    y='independent'
                )
                chart = chart.properties(
                    title='RESPPAL: Since 10 November 2021',
                    width=1200,
                    height=600
                )

                # Display the chart
                st.altair_chart(chart, use_container_width=True)

                # Display dataframe
                df_RESPPAL_10NOV2021['Observation Value'] = df_RESPPAL_10NOV2021['Observation Value'].apply(lambda x: '{:,.0f}'.format(x))
                df_RESPPAL_10NOV2021['Since 10 Nov 2021 ($)'] = df_RESPPAL_10NOV2021['Since 10 Nov 2021 ($)'].apply(lambda x: '{:,.0f}'.format(x))
                df_RESPPAL_10NOV2021.sort_values(by='Time Period', ascending=False, inplace=True)

                #st.checkbox("Use container width", value=True, key="use_container_width_df_RESPPAL_10NOV2021")
                #st.dataframe(df_RESPPAL_10NOV2021, use_container_width=st.session_state.use_container_width_df_RESPPAL_10NOV2021)

                ########################

                df_RESPPAL_1JUN2022 = df_RESPPAL[(df_RESPPAL['Series Name'] == 'RESPPAL') & (df_RESPPAL['Time Period'] >= '2022-06-01')].copy()
                df_RESPPAL_1JUN2022["Observation Value"] = pd.to_numeric(df_RESPPAL_1JUN2022["Observation Value"], errors='coerce')
                df_RESPPAL_1JUN2022["Since 1 Jun 2022 ($)"] = df_RESPPAL_1JUN2022["Observation Value"] - 8813876
                df_RESPPAL_1JUN2022["Since 1 Jun 2022 (%)"] = (df_RESPPAL_1JUN2022["Since 1 Jun 2022 ($)"] / 8813876 * 100).round(2)        

                # chart
                base_chart = alt.Chart(df_RESPPAL_1JUN2022).encode(
                    x='Time Period:T'
                )
                line_since_1_jun_dollars = base_chart.mark_line().encode(
                    y='Since 1 Jun 2022 ($):Q',
                    color=alt.value('#0074e4')
                )
                line_since_1_jun_percent = base_chart.mark_line().encode(
                    y='Since 1 Jun 2022 (%):Q',
                    color=alt.value('#333333')
                )
                chart = alt.layer(line_since_1_jun_dollars, line_since_1_jun_percent).resolve_scale(
                    y='independent'
                )
                chart = chart.properties(
                    title='RESPPAL: Since 1 June 2022',
                    width=1200,
                    height=600
                )

                # Display the chart
                st.altair_chart(chart, use_container_width=True)

                # Display dataframe
                df_RESPPAL_1JUN2022['Observation Value'] = df_RESPPAL_1JUN2022['Observation Value'].apply(lambda x: '{:,.0f}'.format(x))
                df_RESPPAL_1JUN2022['Since 1 Jun 2022 ($)'] = df_RESPPAL_1JUN2022['Since 1 Jun 2022 ($)'].apply(lambda x: '{:,.0f}'.format(x))
                df_RESPPAL_1JUN2022.sort_values(by='Time Period', ascending=False, inplace=True)

                #st.checkbox("Use container width", value=True, key="use_container_width_df_RESPPAL_1JUN2022")
                #st.dataframe(df_RESPPAL_1JUN2022, use_container_width=st.session_state.use_container_width_df_RESPPAL_1JUN2022)

                ########################

                df_RESPPAL_4MAR2020 = df_RESPPAL[(df_RESPPAL['Series Name'] == 'RESPPAL') & (df_RESPPAL['Time Period'] >= '2020-03-04')].copy()
                df_RESPPAL_4MAR2020["Observation Value"] = pd.to_numeric(df_RESPPAL_4MAR2020["Observation Value"], errors='coerce')
                df_RESPPAL_4MAR2020["Since 4 Mar 2020 ($)"] = df_RESPPAL_4MAR2020["Observation Value"] - 4182798
                df_RESPPAL_4MAR2020["Since 4 Mar 2020 (%)"] = (df_RESPPAL_4MAR2020["Since 4 Mar 2020 ($)"] / 4182798 * 100).round(2)        
                
                # chart
                base_chart = alt.Chart(df_RESPPAL_4MAR2020).encode(
                    x='Time Period:T'
                )
                line_since_4_mar_dollars = base_chart.mark_line().encode(
                    y='Since 4 Mar 2020 ($):Q',
                    color=alt.value('#0074e4')
                )
                line_since_4_mar_percent = base_chart.mark_line().encode(
                    y='Since 4 Mar 2020 (%):Q', 
                    color=alt.value('#333333')
                )
                chart = alt.layer(line_since_4_mar_dollars, line_since_4_mar_percent).resolve_scale(
                    y='independent'
                )
                chart = chart.properties(
                    title='RESPPAL: Since 4 March 2020',
                    width=1200,
                    height=600
                )

                # Display the chart
                st.altair_chart(chart, use_container_width=True)

                # Display dataframe
                df_RESPPAL_4MAR2020['Observation Value'] = df_RESPPAL_4MAR2020['Observation Value'].apply(lambda x: '{:,.0f}'.format(x))
                df_RESPPAL_4MAR2020['Since 4 Mar 2020 ($)'] = df_RESPPAL_4MAR2020['Since 4 Mar 2020 ($)'].apply(lambda x: '{:,.0f}'.format(x))
                df_RESPPAL_4MAR2020.sort_values(by='Time Period', ascending=False, inplace=True)
                
                #st.checkbox("Use container width", value=True, key="use_container_width_df_RESPPAL_4MAR2020")
                #st.dataframe(df_RESPPAL_4MAR2020, use_container_width=st.session_state.use_container_width_df_RESPPAL_4MAR2020)

################################################
        with tab_securitiesheldoutright: 

            if st.button("Fetch Data", key="securitiesheldoutright"):

                # Query to retrieve rows
                conn = st.connection("postgresql", type="sql")
                query = f"SELECT * FROM h41_h41_observations WHERE tr87_series_name LIKE '%RESPPALGUO_N.WW%' OR tr87_series_name LIKE '%RESPPALGUO_XCH1_N.WW%' OR tr87_series_name LIKE '%RESPPALGUO_XCH52_N.WW%' OR tr87_series_name LIKE '%RESPPALGASMO_N.WW%' OR tr87_series_name LIKE '%RESPPALGASMO_XCH1_N.WW%' OR tr87_series_name LIKE '%RESPPALGASMO_XCH52_N.WW%' OR tr87_series_name LIKE '%RESPPALGAO_N.WW%' OR tr87_series_name LIKE '%RESPPALGAO_XCH1_N.WW%' OR tr87_series_name LIKE '%RESPPALGAO_XCH52_N.WW%' ORDER BY tr87_series_name ASC;"
                df_SecuritiesHeldOutright = conn.query(query, ttl="60m")
                
                columns = {
                    'tr87_series_name': 'Series Name',
                    'tr87_time_period': 'Time Period',
                    'tr87_observation_value': 'Observation Value'
                }

                # Use the rename() method to change the column names
                df_SecuritiesHeldOutright = df_SecuritiesHeldOutright.rename(columns=columns)
                st.session_state.df_SecuritiesHeldOutright = df_SecuritiesHeldOutright

                # Check if 'df_SecuritiesHeldOutright' exists in session state
                if 'df_SecuritiesHeldOutright' not in st.session_state:
                    with st.spinner('Loading data...'):
                        df_SecuritiesHeldOutright = st.session_state.df_SecuritiesHeldOutright
                else:
                    df_SecuritiesHeldOutright = st.session_state.df_SecuritiesHeldOutright

                ########################

                # Create 'df_ustreasurysecurities'
                df_ustreasurysecurities = df_SecuritiesHeldOutright[
                    (df_SecuritiesHeldOutright['Series Name'] == 'RESPPALGUO_N.WW') | 
                    (df_SecuritiesHeldOutright['Series Name'] == 'RESPPALGUO_XCH1_N.WW') | 
                    (df_SecuritiesHeldOutright['Series Name'] == 'RESPPALGUO_XCH52_N.WW')
                ]

                #create chart
                color_palette = {
                    'domain': ['RESPPALGUO_N.WW', 'RESPPALGUO_XCH1_N.WW', 'RESPPALGUO_XCH52_N.WW'],
                    'range': ['#0074e4', '#D3D3D3', '#333333']
                }

                series_name_mapping = {
                    'RESPPALGUO_N.WW': 'RESPPALGUO',
                    'RESPPALGUO_XCH1_N.WW': 'Change (1W)',
                    'RESPPALGUO_XCH52_N.WW': 'Change (52W)'
                }

                # Create a new column 'New Series Name' with the mapped names
                df_ustreasurysecurities.loc[:, 'Series Name'] = df_ustreasurysecurities['Series Name'].map(series_name_mapping)

                # Create chart with custom series names in legend
                time_series_chart_ustreasurysecurities = alt.Chart(df_ustreasurysecurities).mark_line().encode(
                    x='Time Period:T',
                    y='Observation Value:Q',
                    color=alt.Color('Series Name:N', scale=alt.Scale(domain=list(series_name_mapping.values()), range=color_palette['range'])),
                    tooltip=[
                        'Series Name:N',
                        alt.Tooltip('Time Period:T', format='%Y-%m-%d'),
                        alt.Tooltip('Observation Value:Q', format=',')
                    ]
                ).interactive().properties(
                    title="RESPPALGUO: U.S. Treasury securities",
                    width=1200,
                    height=600
                )

                st.altair_chart(time_series_chart_ustreasurysecurities)

                ########################

                # Create 'df_mortgagebackedsecurities'
                df_mortgagebackedsecurities = df_SecuritiesHeldOutright[
                    (df_SecuritiesHeldOutright['Series Name'] == 'RESPPALGASMO_N.WW') | 
                    (df_SecuritiesHeldOutright['Series Name'] == 'RESPPALGASMO_XCH1_N.WW') | 
                    (df_SecuritiesHeldOutright['Series Name'] == 'RESPPALGASMO_XCH52_N.WW')
                ]

                #create chart
                color_palette = {
                    'domain': ['RESPPALGASMO_N.WW', 'RESPPALGASMO_XCH1_N.WW', 'RESPPALGASMO_XCH52_N.WW'],
                    'range': ['#0074e4', '#D3D3D3', '#333333']
                }

                series_name_mapping = {
                    'RESPPALGASMO_N.WW': 'RESPPALGASMO',
                    'RESPPALGASMO_XCH1_N.WW': 'Change (1W)',
                    'RESPPALGASMO_XCH52_N.WW': 'Change (52W)'
                }

                # Create a new column 'New Series Name' with the mapped names
                df_mortgagebackedsecurities.loc[:, 'Series Name'] = df_mortgagebackedsecurities['Series Name'].map(series_name_mapping)

                # Create chart with custom series names in legend
                time_series_chart_mortgagebackedsecurities = alt.Chart(df_mortgagebackedsecurities).mark_line().encode(
                    x='Time Period:T',
                    y='Observation Value:Q',
                    color=alt.Color('Series Name:N', scale=alt.Scale(domain=list(series_name_mapping.values()), range=color_palette['range'])),
                    tooltip=[
                        'Series Name:N',
                        alt.Tooltip('Time Period:T', format='%Y-%m-%d'),
                        alt.Tooltip('Observation Value:Q', format=',')
                    ]
                ).interactive().properties(
                    title="RESPPALGASMO: Mortgage-backed securities",
                    width=1200,
                    height=600
                )

                st.altair_chart(time_series_chart_mortgagebackedsecurities)

                ########################

                # Create 'df_federalagencydebtsecurities'
                df_federalagencydebtsecurities = df_SecuritiesHeldOutright[
                    (df_SecuritiesHeldOutright['Series Name'] == 'RESPPALGAO_N.WW') | 
                    (df_SecuritiesHeldOutright['Series Name'] == 'RESPPALGAO_XCH1_N.WW') | 
                    (df_SecuritiesHeldOutright['Series Name'] == 'RESPPALGAO_XCH52_N.WW')
                ]

                #create chart
                color_palette = {
                    'domain': ['RESPPALGAO_N.WW', 'RESPPALGAO_XCH1_N.WW', 'RESPPALGAO_XCH52_N.WW'],
                    'range': ['#0074e4', '#D3D3D3', '#333333']
                }

                series_name_mapping = {
                    'RESPPALGAO_N.WW': 'RESPPALGAO',
                    'RESPPALGAO_XCH1_N.WW': 'Change (1W)',
                    'RESPPALGAO_XCH52_N.WW': 'Change (52W)'
                }

                # Create a new column 'New Series Name' with the mapped names
                df_federalagencydebtsecurities.loc[:, 'Series Name'] = df_federalagencydebtsecurities['Series Name'].map(series_name_mapping)

                # Create chart with custom series names in legend
                time_series_chart_mortgagebackedsecurities = alt.Chart(df_federalagencydebtsecurities).mark_line().encode(
                    x='Time Period:T',
                    y='Observation Value:Q',
                    color=alt.Color('Series Name:N', scale=alt.Scale(domain=list(series_name_mapping.values()), range=color_palette['range'])),
                    tooltip=[
                        'Series Name:N',
                        alt.Tooltip('Time Period:T', format='%Y-%m-%d'),
                        alt.Tooltip('Observation Value:Q', format=',')
                    ]
                ).interactive().properties(
                    title="RESPPALGAO: Federal agency debt securities",
                    width=1200,
                    height=600
                )

                st.altair_chart(time_series_chart_mortgagebackedsecurities)

################################################
        with tab_treasurysecurities:

            if st.button("Fetch Data", key="treasurysecurities"):

                # Query to retrieve rows
                conn = st.connection("postgresql", type="sql")
                query = f"SELECT * FROM h41_h41_observations WHERE tr87_series_name LIKE '%RESPPALGUOB_N.WW%' OR tr87_series_name LIKE '%RESPPALGUOB_XCH1_N.WW%' OR tr87_series_name LIKE '%RESPPALGUOB_XCH52_N.WW%' OR tr87_series_name LIKE '%RESPPALGUOMN_N.WW%' OR tr87_series_name LIKE '%RESPPALGUOMN_XCH1_N.WW%' OR tr87_series_name LIKE '%RESPPALGUOMN_XCH52_N.WW%' OR tr87_series_name LIKE '%RESPPALGUOMI_N.WW%' OR tr87_series_name LIKE '%RESPPALGUOMI_XCH1_N.WW%' OR tr87_series_name LIKE '%RESPPALGUOMI_XCH52_N.WW%' OR tr87_series_name LIKE '%RESPPALGUOMC_N.WW%' OR tr87_series_name LIKE '%RESPPALGUOMC_XCH1_N.WW%' OR tr87_series_name LIKE '%RESPPALGUOMC_XCH52_N.WW%' ORDER BY tr87_series_name ASC;"    
                df_USTreasurySecurities = conn.query(query, ttl="60m")
                
                columns = {
                    'tr87_series_name': 'Series Name',
                    'tr87_time_period': 'Time Period',
                    'tr87_observation_value': 'Observation Value'
                }

                # Use the rename() method to change the column names
                df_USTreasurySecurities = df_USTreasurySecurities.rename(columns=columns)
                st.session_state.df_USTreasurySecurities = df_USTreasurySecurities

                # Check if 'df_USTreasurySecurities' exists in session state
                if 'df_USTreasurySecurities' not in st.session_state:
                    with st.spinner('Loading data...'):
                        df_USTreasurySecurities = st.session_state.df_USTreasurySecurities
                else:
                    df_USTreasurySecurities = st.session_state.df_USTreasurySecurities

                ########################

                # Create 'df_ustreasurysecurities'
                df_bills = df_USTreasurySecurities[
                    (df_USTreasurySecurities['Series Name'] == 'RESPPALGUOB_N.WW') | 
                    (df_USTreasurySecurities['Series Name'] == 'RESPPALGUOB_XCH1_N.WW') | 
                    (df_USTreasurySecurities['Series Name'] == 'RESPPALGUOB_XCH52_N.WW')
                ]

                #create chart
                color_palette = {
                    'domain': ['RESPPALGUOB_N.WW', 'RESPPALGUOB_XCH1_N.WW', 'RESPPALGUOB_XCH52_N.WW'],
                    'range': ['#0074e4', '#D3D3D3', '#333333']
                }

                series_name_mapping = {
                    'RESPPALGUOB_N.WW': 'RESPPALGUOB',
                    'RESPPALGUOB_XCH1_N.WW': 'Change (1W)',
                    'RESPPALGUOB_XCH52_N.WW': 'Change (52W)'
                }

                # Create a new column 'New Series Name' with the mapped names
                df_bills.loc[:, 'Series Name'] = df_bills['Series Name'].map(series_name_mapping)

                # Create chart with custom series names in legend
                time_series_chart_bills = alt.Chart(df_bills).mark_line().encode(
                    x='Time Period:T',
                    y='Observation Value:Q',
                    color=alt.Color('Series Name:N', scale=alt.Scale(domain=list(series_name_mapping.values()), range=color_palette['range'])),
                    tooltip=[
                        'Series Name:N',
                        alt.Tooltip('Time Period:T', format='%Y-%m-%d'),
                        alt.Tooltip('Observation Value:Q', format=',')
                    ]
                ).interactive().properties(
                    title="RESPPALGUOB: Bills",
                    width=1200,
                    height=600
                )

                st.altair_chart(time_series_chart_bills)

                ########################

                # Create 'df_ustreasurysecurities'
                df_notesandbondsnominal = df_USTreasurySecurities[
                    (df_USTreasurySecurities['Series Name'] == 'RESPPALGUOMN_N.WW') | 
                    (df_USTreasurySecurities['Series Name'] == 'RESPPALGUOMN_XCH1_N.WW') | 
                    (df_USTreasurySecurities['Series Name'] == 'RESPPALGUOMN_XCH52_N.WW')
                ]

                #create chart
                color_palette = {
                    'domain': ['RESPPALGUOMN_N.WW', 'RESPPALGUOMN_XCH1_N.WW', 'RESPPALGUOMN_XCH52_N.WW'],
                    'range': ['#0074e4', '#D3D3D3', '#333333']
                }

                series_name_mapping = {
                    'RESPPALGUOMN_N.WW': 'RESPPALGUOMN',
                    'RESPPALGUOMN_XCH1_N.WW': 'Change (1W)',
                    'RESPPALGUOMN_XCH52_N.WW': 'Change (52W)'
                }

                # Create a new column 'New Series Name' with the mapped names
                df_notesandbondsnominal.loc[:, 'Series Name'] = df_notesandbondsnominal['Series Name'].map(series_name_mapping)

                # Create chart with custom series names in legend
                time_series_chart_notesandbondsnominal = alt.Chart(df_notesandbondsnominal).mark_line().encode(
                    x='Time Period:T',
                    y='Observation Value:Q',
                    color=alt.Color('Series Name:N', scale=alt.Scale(domain=list(series_name_mapping.values()), range=color_palette['range'])),
                    tooltip=[
                        'Series Name:N',
                        alt.Tooltip('Time Period:T', format='%Y-%m-%d'),
                        alt.Tooltip('Observation Value:Q', format=',')
                    ]
                ).interactive().properties(
                    title="RESPPALGUOMN: Notes and bonds, nominal",
                    width=1200,
                    height=600
                )

                st.altair_chart(time_series_chart_notesandbondsnominal)

                ########################

                # Create 'df_ustreasurysecurities'
                df_notesandbondsinflationindexed = df_USTreasurySecurities[
                    (df_USTreasurySecurities['Series Name'] == 'RESPPALGUOMI_N.WW') | 
                    (df_USTreasurySecurities['Series Name'] == 'RESPPALGUOMI_XCH1_N.WW') | 
                    (df_USTreasurySecurities['Series Name'] == 'RESPPALGUOMI_XCH52_N.WW')
                ]

                #create chart
                color_palette = {
                    'domain': ['RESPPALGUOMI_N.WW', 'RESPPALGUOMI_XCH1_N.WW', 'RESPPALGUOMI_XCH52_N.WW'],
                    'range': ['#0074e4', '#D3D3D3', '#333333']
                }

                series_name_mapping = {
                    'RESPPALGUOMI_N.WW': 'RESPPALGUOMI',
                    'RESPPALGUOMI_XCH1_N.WW': 'Change (1W)',
                    'RESPPALGUOMI_XCH52_N.WW': 'Change (52W)'
                }

                # Create a new column 'New Series Name' with the mapped names
                df_notesandbondsinflationindexed.loc[:, 'Series Name'] = df_notesandbondsinflationindexed['Series Name'].map(series_name_mapping)

                # Create chart with custom series names in legend
                time_series_chart_notesandbondsinflationindexed = alt.Chart(df_notesandbondsinflationindexed).mark_line().encode(
                    x='Time Period:T',
                    y='Observation Value:Q',
                    color=alt.Color('Series Name:N', scale=alt.Scale(domain=list(series_name_mapping.values()), range=color_palette['range'])),
                    tooltip=[
                        'Series Name:N',
                        alt.Tooltip('Time Period:T', format='%Y-%m-%d'),
                        alt.Tooltip('Observation Value:Q', format=',')
                    ]
                ).interactive().properties(
                    title="RESPPALGUOMI: Notes and bonds, inflation-indexed",
                    width=1200,
                    height=600
                )

                st.altair_chart(time_series_chart_notesandbondsinflationindexed)

                ########################

                # Create 'df_ustreasurysecurities'
                df_inflationcompensation = df_USTreasurySecurities[
                    (df_USTreasurySecurities['Series Name'] == 'RESPPALGUOMC_N.WW') | 
                    (df_USTreasurySecurities['Series Name'] == 'RESPPALGUOMC_XCH1_N.WW') | 
                    (df_USTreasurySecurities['Series Name'] == 'RESPPALGUOMC_XCH52_N.WW')
                ]

                #create chart
                color_palette = {
                    'domain': ['RESPPALGUOMC_N.WW', 'RESPPALGUOMC_XCH1_N.WW', 'RESPPALGUOMC_XCH52_N.WW'],
                    'range': ['#0074e4', '#D3D3D3', '#333333']
                }

                series_name_mapping = {
                    'RESPPALGUOMC_N.WW': 'RESPPALGUOMC',
                    'RESPPALGUOMC_XCH1_N.WW': 'Change (1W)',
                    'RESPPALGUOMC_XCH52_N.WW': 'Change (52W)'
                }

                # Create a new column 'New Series Name' with the mapped names
                df_inflationcompensation.loc[:, 'Series Name'] = df_inflationcompensation['Series Name'].map(series_name_mapping)

                # Create chart with custom series names in legend
                time_series_chart_inflationcompensation = alt.Chart(df_inflationcompensation).mark_line().encode(
                    x='Time Period:T',
                    y='Observation Value:Q',
                    color=alt.Color('Series Name:N', scale=alt.Scale(domain=list(series_name_mapping.values()), range=color_palette['range'])),
                    tooltip=[
                        'Series Name:N',
                        alt.Tooltip('Time Period:T', format='%Y-%m-%d'),
                        alt.Tooltip('Observation Value:Q', format=',')
                    ]
                ).interactive().properties(
                    title="RESPPALGUOMC: Inflation compensation",
                    width=1200,
                    height=600
                )

                st.altair_chart(time_series_chart_inflationcompensation)

################################################
        with tab_loans:

            if st.button("Fetch Data", key="loans"):

                # Query to retrieve rows
                conn = st.connection("postgresql", type="sql")
                query = f"SELECT * FROM h41_h41_observations WHERE tr87_series_name LIKE '%RESPPALD_N.WW%' OR tr87_series_name LIKE '%RESPPALD_XCH1_N.WW%' OR tr87_series_name LIKE '%RESPPALD_XCH52_N.WW%' ORDER BY tr87_series_name ASC;"    
                df_Loans = conn.query(query, ttl="60m")
                
                columns = {
                    'tr87_series_name': 'Series Name',
                    'tr87_time_period': 'Time Period',
                    'tr87_observation_value': 'Observation Value'
                }

                # Use the rename() method to change the column names
                df_Loans = df_Loans.rename(columns=columns)
                st.session_state.df_Loans = df_Loans

                # Check if 'df_Loans' exists in session state
                if 'df_Loans' not in st.session_state:
                    with st.spinner('Loading data...'):
                        df_Loans = st.session_state.df_Loans
                else:
                    df_Loans = st.session_state.df_Loans

                # Create 'df_Loans'
                df = df_Loans[
                    (df_Loans['Series Name'] == 'RESPPALD_N.WW') | 
                    (df_Loans['Series Name'] == 'RESPPALD_XCH1_N.WW') | 
                    (df_Loans['Series Name'] == 'RESPPALD_XCH52_N.WW')
                ]

                #create chart
                color_palette = {
                    'domain': ['RESPPALD_N.WW', 'RESPPALD_XCH1_N.WW', 'RESPPALD_XCH52_N.WW'],
                    'range': ['#0074e4', '#D3D3D3', '#333333']
                }

                series_name_mapping = {
                    'RESPPALD_N.WW': 'RESPPALD',
                    'RESPPALD_XCH1_N.WW': 'Change (1W)',
                    'RESPPALD_XCH52_N.WW': 'Change (52W)'
                }

                # Create a new column 'New Series Name' with the mapped names
                df.loc[:, 'Series Name'] = df['Series Name'].map(series_name_mapping)

                # Create chart with custom series names in legend
                time_series_chart_bills = alt.Chart(df).mark_line().encode(
                    x='Time Period:T',
                    y='Observation Value:Q',
                    color=alt.Color('Series Name:N', scale=alt.Scale(domain=list(series_name_mapping.values()), range=color_palette['range'])),
                    tooltip=[
                        'Series Name:N',
                        alt.Tooltip('Time Period:T', format='%Y-%m-%d'),
                        alt.Tooltip('Observation Value:Q', format=',')
                    ]
                ).interactive().properties(
                    title="RESPPALD: Loans",
                    width=1200,
                    height=600
                )

                st.altair_chart(time_series_chart_bills)

################################################
        with tab_treasurygeneralaccount:

            if st.button("Fetch Data", key="treasurygeneralaccount"):

                # Query to retrieve rows
                conn = st.connection("postgresql", type="sql")
                query = f"SELECT * FROM h41_h41_observations WHERE tr87_series_name LIKE '%RESPPLLDT_N.WW%' OR tr87_series_name LIKE '%RESPPLLDT_XCH1_N.WW%' OR tr87_series_name LIKE '%RESPPLLDT_XCH52_N.WW%' ORDER BY tr87_series_name ASC;"    
                df_TGA = conn.query(query, ttl="60m")
                
                columns = {
                    'tr87_series_name': 'Series Name',
                    'tr87_time_period': 'Time Period',
                    'tr87_observation_value': 'Observation Value'
                }

                # Use the rename() method to change the column names
                df_TGA = df_TGA.rename(columns=columns)
                st.session_state.df_TGA = df_TGA

                # Check if 'df_TGA' exists in session state
                if 'df_TGA' not in st.session_state:
                    with st.spinner('Loading data...'):
                        df_TGA = st.session_state.df_TGA
                else:
                    df_TGA = st.session_state.df_TGA

                # Create 'df_TGA'
                df = df_TGA[
                    (df_TGA['Series Name'] == 'RESPPLLDT_N.WW') | 
                    (df_TGA['Series Name'] == 'RESPPLLDT_XCH1_N.WW') | 
                    (df_TGA['Series Name'] == 'RESPPLLDT_XCH52_N.WW')
                ]

                #create chart
                color_palette = {
                    'domain': ['RESPPLLDT_N.WW', 'RESPPLLDT_XCH1_N.WW', 'RESPPLLDT_XCH52_N.WW'],
                    'range': ['#0074e4', '#D3D3D3', '#333333']
                }

                series_name_mapping = {
                    'RESPPLLDT_N.WW': 'RESPPLLDT',
                    'RESPPLLDT_XCH1_N.WW': 'Change (1W)',
                    'RESPPLLDT_XCH52_N.WW': 'Change (52W)'
                }

                # Create a new column 'New Series Name' with the mapped names
                df.loc[:, 'Series Name'] = df['Series Name'].map(series_name_mapping)

                # Create chart with custom series names in legend
                time_series_chart_TGA = alt.Chart(df).mark_line().encode(
                    x='Time Period:T',
                    y='Observation Value:Q',
                    color=alt.Color('Series Name:N', scale=alt.Scale(domain=list(series_name_mapping.values()), range=color_palette['range'])),
                    tooltip=[
                        'Series Name:N',
                        alt.Tooltip('Time Period:T', format='%Y-%m-%d'),
                        alt.Tooltip('Observation Value:Q', format=',')
                    ]
                ).interactive().properties(
                    title="RESPPLLDT: Treasury General Account",
                    width=1200,
                    height=600
                )

                st.altair_chart(time_series_chart_TGA)

        with tab_rarra:
            st.markdown("<h2><u>Coming Soon</u></h2>", unsafe_allow_html=True)

        with tab_usdliquidityswaps:
            st.markdown("<h2><u>Coming Soon</u></h2>", unsafe_allow_html=True)

        with tab_someholdings:
            st.markdown("<h2><u>Coming Soon</u></h2>", unsafe_allow_html=True)


# Display the page
show_moneybankingcredit_h41()