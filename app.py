
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import requests
from streamlit_dynamic_filters import DynamicFilters


#source = pd.DataFrame({"category": [1, 2, 3, 4, 5, 6], "value": [4, 6, 10, 3, 7, 8]})


st.set_page_config(
    # Title and icon for the browser's tab bar:
    page_title="Health Monitoring Tool",
    page_icon="🌦️",
    # Make the content take up the width of the page:
    layout="wide",
)

st.title("Health Monitoring Tool")
st.write("A public health monitoring platform tool that collects and visualizes data related to community health.")

API_ENDPOINT = "https://disease.sh/v3/covid-19/countries"

# Function to fetch data from the API
@st.cache_data # Cache the data to prevent re-fetching on every rerun
def get_health_stats_data(url):
    try:
        response = requests.get(url)
        # Raise an exception for bad status codes
        response.raise_for_status() 
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None
    
# Fetch data
api_data = get_health_stats_data(API_ENDPOINT)

if api_data is not None:
    # Convert the fetched list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(api_data)
    
    # Drop unnecessary columns
    df.drop('countryInfo', inplace=True, axis=1)

    # Initialize dynamic filters
    dynamic_filters = DynamicFilters(df, filters=['continent', 'country'])

    # Display filters in sidebar and the filtered dataframe in main pane
    # dynamic_filters.display_filters(location='sidebar') #columns
    dynamic_filters.display_filters(location='sidebar', num_columns=2, gap='medium')
    
    st.subheader(f"KPI Metrics Summary")

    # Get filtered dataframe
    filtered_df = dynamic_filters.filter_df()

    # Calculate and display metrics
    total_cases = filtered_df['cases'].sum()
    total_deaths = filtered_df['deaths'].sum()
    total_recovered = filtered_df['recovered'].sum()
    total_active = filtered_df['active'].sum()
    total_tests = filtered_df['tests'].sum()
    total_population = filtered_df['population'].sum()

    # Display metrics using Streamlit columns for layout
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Cases", f"{total_cases:,}")
    with col2:
        st.metric("Deaths", f"{total_deaths:,}")
    with col3:
        st.metric("Recovered", f"{total_recovered:,}")
    with col4:
        st.metric("Active", f"{total_active:,}")
    with col5:
        st.metric("Tests", f"{total_tests:,}")
    with col6:
        st.metric("Population", f"{total_population:,}")

    # Display charts
    with st.container(horizontal=True, gap="medium"):
        # Create two columns with equal width
        cols = st.columns(2, gap="medium")

        # Place a chart in the first column
        with cols[0]:
            st.write("### Cases by Continent")
            st.bar_chart(filtered_df, x="continent", y="cases")

        # Place a chart in the second column
        with cols[1]:
            st.write("### Cases by Country")
            st.bar_chart(filtered_df, x="country", y="cases", color="blue")

    with st.container(horizontal=True, gap="medium"):
        cols = st.columns(2, gap="medium")

        with cols[0]:
            st.write("### Deaths by Continent")
            st.bar_chart(filtered_df, x="continent", y="deaths", color="blue")

        with cols[1]:
            st.write("### Deaths by Country")
            st.bar_chart(filtered_df, x="country", y="deaths", color="blue")

    with st.container(horizontal=True, gap="medium"):
        cols = st.columns(2, gap="medium")

        with cols[0]:
            st.write("### Recovered by Continent")
            st.bar_chart(filtered_df, x="continent", y="recovered", color="blue")

        with cols[1]:
            st.write("### Recovered by Country")
            st.bar_chart(filtered_df, x="country", y="recovered", color="blue")

    with st.container(horizontal=True, gap="medium"):
        cols = st.columns(2, gap="medium")

        with cols[0]:
            st.write("### Active by Continent")
            st.bar_chart(filtered_df, x="continent", y="active", color="blue")

        with cols[1]:
            st.write("### Active by Country")
            st.bar_chart(filtered_df, x="country", y="active", color="blue")

    with st.container(horizontal=True, gap="medium"):
        cols = st.columns(2, gap="medium")

        with cols[0]:
            st.write("### Tests by Continent")
            st.bar_chart(filtered_df, x="continent", y="tests", color="blue")

        with cols[1]:
            st.write("### Tests by Country")
            st.bar_chart(filtered_df, x="country", y="tests", color="blue")

    # Optionally, display the filtered DataFrame
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)
else:
    st.warning("Could not load data from the API.")