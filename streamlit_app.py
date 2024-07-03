"""
Air Quality Data Exploration 

Skills used: API Requests, Data Handling with Pandas, Data Visualization with Streamlit
"""

# Importing the libraries #
import requests  # to make HTTP requests to get data from the internet
import pandas as pd  # for data manipulation
import streamlit as st  # for creating a web app

# Your AQICN API key
api_key = 'dd88e9b11b0d167c66e46b3338a4b4b0fd2127f9'

# These are the main cities in each UK region
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

# Function to fetch air quality data for a specific city
def fetch_air_quality(city):
    # Construct the API request URL
    url = f"http://api.waqi.info/feed/{city}/?token={api_key}"
    # Make the request to the API
    response = requests.get(url)
    # Convert the response to JSON format
    data = response.json()
    # Check if the response status is 'ok'
    if data['status'] == 'ok':
        return data['data']
    else:
        return None  # Return None if there is an error

## This is an empty list to store the air quality data in ##
air_quality_data = []

# Loop through each city to get the air quality data
for region, city in cities.items():
    try:
        # Fetch the air quality data for the city
        city_data = fetch_air_quality(city)
        # Check if data is returned
        if city_data:
            # Create a dictionary to store the data for each city
            city_info = {
                'region': region,
                'city': city,
                'aqi': city_data['aqi'],  # Air Quality Index: A measure of how polluted the air is
                'pm25': city_data['iaqi'].get('pm25', {}).get('v', None),  # Particulate Matter < 2.5 microns
                'pm10': city_data['iaqi'].get('pm10', {}).get('v', None),  # Particulate Matter < 10 microns
                'no2': city_data['iaqi'].get('no2', {}).get('v', None),  # Nitrogen Dioxide
                'so2': city_data['iaqi'].get('so2', {}).get('v', None),  # Sulfur Dioxide
                'co': city_data['iaqi'].get('co', {}).get('v', None),  # Carbon Monoxide
                'o3': city_data['iaqi'].get('o3', {}).get('v', None)  # Ozone
            }
            # Add the city's data to our list
            air_quality_data.append(city_info)
    except Exception as e:
        # Print an error message if there's a problem
        print("Error fetching data for", city, ":", e)

# Convert the list of data into a pandas DataFrame (like a table)
df = pd.DataFrame(air_quality_data)

# Set up our Streamlit app
st.title("Air Quality Data for UK Regions")  # Title of our app
st.write("## Main Cities and Their Air Quality Data")
st.write("""
This application fetches and displays the air quality data for the main cities in each of the 12 regions of the UK. 
The data includes the AQI (Air Quality Index) and concentrations of various pollutants:
- **PM2.5**: Particulate Matter < 2.5 microns. Tiny particles that reduce visibility and cause the air to appear hazy when levels are elevated.
- **PM10**: Particulate Matter < 10 microns. Particles that can be inhaled and cause health problems.
- **NO2**: Nitrogen Dioxide. A pollutant that can irritate the lungs and lower resistance to respiratory infections.
- **SO2**: Sulfur Dioxide. A gas that can cause respiratory problems and aggravate existing heart disease.
- **CO**: Carbon Monoxide. A colorless, odorless gas that can cause harmful health effects by reducing oxygen delivery to the body's organs and tissues.
- **O3**: Ozone. A gas that can cause respiratory problems and other health issues.
""")

# Display the DataFrame in our app
st.dataframe(df)

# Save the DataFrame to a CSV file
csv_file = 'uk_air_quality_data.csv'
df.to_csv(csv_file, index=False)
st.write("Data saved to CSV:", csv_file)

# Visualization: Show AQI for each city in a bar chart
st.write("## Air Quality Index (AQI) for Each City")
st.bar_chart(df.set_index('city')['aqi'])
