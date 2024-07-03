# Air Quality Data - Digital Futures Capstone #
## Skills I have used: API Requests, Data Handling with Pandas, Data Visualization with Streamlit ##

### Importing the Libraries ###
#### This section is used to import some of the data libraries from the API to help retrieve the data. ####

import requests
import pandas as pd
import streamlit as st

# Load environment variables from the .env file
load_dotenv()

# Access the API key from environment variables
api_key = os.getenv('API_KEY')

# Main Cities in every UK Region #
## This section shows the biggest city for each UK region ##
cities = {
    "Wales": "Cardiff",
    "Scotland": "Edinburgh",
    "Northern Ireland": "Belfast",
    "London": "London",
    "North East England": "Newcastle upon Tyne",
    "North West England": "Manchester",
    "Yorkshire and the Humber": "Leeds",
    "East Midlands": "Nottingham",
    "West Midlands": "Birmingham",
    "South East England": "Brighton",
    "East of England": "Norwich",
    "South West England": "Bristol"
}

# Fetching the Air Quality Data Function #
## This function should retrive the air quality data for each city listed above in the dictionary. ##
### A function is code that can be used multiple times to do a specific task/job. The below code is used for creating the web address that is needed to retrieve the Air Quality Data for each city ###

def fetch_air_quality(city):
    # Constructing the API request URL #
    ## The below URL is made by combining the URL with the city name and the API key. ##
    url = f"http://api.waqi.info/feed/{city}/?token={api_key}"

    # Request to the API
    ## This requests a library to get data from the API ##
    response = requests.get(url)

    # Convert the data to JSON format #
    ## With the data from API the below should convert this into a JSON format. ##
    data = response.json()
    
    # Checking if the response status is 'ok' #
    ## The below should be able to check If the status is 'ok' and fine. If it is okay then it means the data was retrieved with no issues. But if is not okay then it should return as none per the last section of the code. ##
    if data['status'] == 'ok':
        return data['data']
    else:
        return None

# Empty List to Store the Air Quality Data #
## This list should hold all the air quality data from the API. ##
air_quality_data = []

# Search each city to get the air quality data #
for region, city in cities.items():
    try:
        # Fetch the air quality data for the city #
        city_data = fetch_air_quality(city)
        
        # Check if data is returned. If yes, add to the list. #
        if city_data:
            # Create a dictionary to store the air quality data for each city #
            city_info = {
                'region': region,
                'city': city,
                'aqi': city_data['aqi'],  # Air Quality Index: A measure of how polluted the air is.
                'pm25': city_data['iaqi'].get('pm25', {}).get('v', None),  # Particulate Matter < 2.5 microns.
                'pm10': city_data['iaqi'].get('pm10', {}).get('v', None),  # Particulate Matter < 10 microns.
                'no2': city_data['iaqi'].get('no2', {}).get('v', None),  # Nitrogen Dioxide.
                'so2': city_data['iaqi'].get('so2', {}).get('v', None),  # Sulfur Dioxide.
                'co': city_data['iaqi'].get('co', {}).get('v', None),  # Carbon Monoxide.
                'o3': city_data['iaqi'].get('o3', {}).get('v', None)  # Ozone.
            }
            # Add the city's data to the list #
            air_quality_data.append(city_info)
    except Exception as e:
        # Print an error message if there's a problem
        print("Error fetching data for", city, ":", e)

### Convert the List of Data into a Pandas DataFrame ###
# Use pandas to create a DataFrame, which is like a table, to store the data.
df = pd.DataFrame(air_quality_data)

# Display the DataFrame in the app #
# The data will be formatted into a table for users to read #
st.dataframe(df)

# Save the DataFrame to a CSV file for later use
csv_file = 'uk_air_quality_data.csv'
df.to_csv(csv_file, index=False)
st.write("Data saved to CSV:", csv_file)
