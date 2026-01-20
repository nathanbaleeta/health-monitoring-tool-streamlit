import streamlit as st
import requests
import pandas as pd

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

# Streamlit app layout
st.title("Health Monitoring Tool")
st.write("A public health monitoring platform tool that collects and visualizes data related to community health.")


API_ENDPOINT = "https://disease.sh/v3/covid-19/countries"

# Fetch data
api_data = get_health_stats_data(API_ENDPOINT)

if api_data is not None:
    # Convert the fetched list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(api_data)
    
    # Drop unnecessary columns
    df.drop('countryInfo', inplace=True, axis=1)

    # Create a selectbox with unique categories
    country_selection = st.selectbox(
        'Select Country',
        options=df['country'].unique()
    )

    # Filter the data based on the selection
    filtered_df = df[df['country'] == country_selection]

    st.subheader("Data from API.")
    st.write(f"Fetched {len(filtered_df)} records.")

    # Display the DataFrame in an interactive table
    st.dataframe(filtered_df) # Use st.dataframe for an interactive table

else:
    st.warning("Could not load data from the API.")

