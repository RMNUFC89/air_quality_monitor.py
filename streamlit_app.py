"""
Air Quality Data Exploration 

Skills used: API Requests, Data Handling with Pandas, Data Visualization with Streamlit and Folium
"""

# Importing the libraries we need
import requests  # to make HTTP requests to get data from the internet
import pandas as pd  # for data manipulation
import streamlit as st  # for creating a web app
import folium  # for creating interactive maps
from streamlit_folium import folium_static  # to display folium maps in Streamlit

# Your AQICN API key
api_key = 'dd88e9b11b0d167c66e46b3338a4b4b0fd2127f9'

# These are the main cities in each UK region along with their coordinates
cities = {
    "Wales": {"name": "Cardiff", "coords": [51.4816, -3.1791]},
    "Scotland": {"name": "Edinburgh", "coords": [55.9533, -3.1883]},
    "Northern Ireland": {"name": "Belfast", "coords": [54.5973, -5.9301]},
    "London": {"name": "London", "coords": [51.5074, -0.1278]},
    "North East England": {"name": "Newcastle upon Tyne", "coords": [54.9783, -1.6174]},
    "North West England": {"name": "Manchester", "coords": [53.4808, -2.2426]},
    "Yorkshire and the Humber": {"name": "Leeds", "coords": [53.8008, -1.5491]},
    "East Midlands": {"name": "Nottingham", "coords": [52.9548, -1.1581]},
    "West Midlands": {"name": "Birmingham", "coords": [52.4862, -1.8904]},
    "South East England": {"name": "Brighton", "coords": [50.8225, -0.1372]},
    "East of England": {"name": "Norwich", "coords": [52.6309, 1.2974]},
    "South West England": {"name": "Bristol", "coords": [51.4545, -2.5879]}
}

# Function to fetch air quality data for a specific city
def fetch_air_quality(city):
    url = f"http://api.waqi.info/feed/{city['name']}/?token={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'ok':
        return data['data']
    else:
        return None

# Create an empty list to store the air quality data
air_quality_data = []

# Loop through each city to get the air quality data
for region, city in cities.items():
    try:
        # Fetch the air quality data for the city
        city_data = fetch_air_quality(city)
        if city_data:
            # Create a dictionary to store the data for each city
            city_info = {
                'region': region,
                'city': city['name'],
                'coords': city['coords'],
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
        print("Error fetching data for", city['name'], ":", e)

# Convert the list of data into a pandas DataFrame (like a table)
df = pd.DataFrame(air_quality_data)

# Set up our Streamlit app
st.title("Air Quality Data for UK Regions")  # Title of our app
st.write("## Main Cities and Their Air Quality Data")

# Display the DataFrame in our app
st.dataframe(df)

# Save the DataFrame to a CSV file
csv_file = 'uk_air_quality_data.csv'
df.to_csv(csv_file, index=False)
st.write("Data saved to CSV:", csv_file)

# Function to determine the color of the marker based on AQI
def get_color(aqi):
    if aqi <= 50:
        return 'green'  # Good
    elif 51 <= aqi <= 100:
        return 'yellow'  # Moderate
    else:
        return 'red'  # Bad

# Create a folium map centered around the UK
map = folium.Map(location=[54.0, -2.0], zoom_start=6)

# Add a marker for each city
for index, row in df.iterrows():
    folium.Marker(
        location=row['coords'],
        popup=f"{row['city']} (AQI: {row['aqi']})",
        icon=folium.Icon(color=get_color(row['aqi']))
    ).add_to(map)

# Display the map in the Streamlit app
st.write("## Air Quality Map")
folium_static(map)
