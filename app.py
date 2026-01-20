import streamlit as st
import requests
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters


# Streamlit app layout
st.title("Health Monitoring Tool")
st.write("A public health monitoring platform tool that collects and visualizes data related to community health.")

st.subheader("Data from API.")

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

    # Display filters and the filtered dataframe
    dynamic_filters.display_filters()
    dynamic_filters.display_df()

    


    

else:
    st.warning("Could not load data from the API.")

