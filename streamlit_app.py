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
from datetime import datetime, timedelta  # for date handling

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

# Function to fetch air quality data for a specific city on a specific date
def fetch_air_quality(city, date):
    url = f"http://api.waqi.info/feed/{city['name']}/?token={api_key}&date={date}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'ok':
        return data['data']
    else:
        return None

# Get today's date and the date seven days ago
today = datetime.today().date()
seven_days_ago = today - timedelta(days=7)

# Set up our Streamlit app
st.title("Air Quality Data for UK Regions")  # Title of our app
st.write("## Main Cities and Their Air Quality Data")

# Date input from the user
start_date = st.date_input("Start date", seven_days_ago)
end_date = st.date_input("End date", today)

# Ensure the start date is not after the end date
if start_date > end_date:
    st.error("Error: End date must fall after start date.")
else:
    # Create an empty list to store the air quality data
    air_quality_data = []

    # Loop through each date in the selected date range
    for single_date in pd.date_range(start=start_date, end=end_date):
        date_str = single_date.strftime("%Y-%m-%d")
        # Loop through each city to get the air quality data
        for region, city in cities.items():
            try:
                # Fetch the air quality data for the city on the given date
                city_data = fetch_air_quality(city, date_str)
                if city_data:
                    # Create a dictionary to store the data for each city
                    city_info = {
                        'date': date_str,
                        'region': region,
                        'city': city['name'],
                        'aqi': city_data['aqi']  # Air Quality Index: A measure of how polluted the air is
                    }
                    # Add the city's data to our list
                    air_quality_data.append(city_info)
            except Exception as e:
                print(f"Error fetching data for {city['name']} on {date_str}: {e}")

    # Convert the list of data into a pandas DataFrame (like a table)
    df = pd.DataFrame(air_quality_data)

    # Function to determine the color of the row based on AQI
    def get_row_color(aqi):
        if aqi <= 50:
            return 'background-color: green'
        elif 51 <= aqi <= 100:
            return 'background-color: yellow'
        else:
            return 'background-color: red'

    # Apply the row color function to the DataFrame
    styled_df = df.style.applymap(lambda x: get_row_color(x) if isinstance(x, int) else '')

    # Display the styled DataFrame in our app
    st.dataframe(styled_df)

    # Save the DataFrame to a CSV file
    csv_file = 'uk_air_quality_data.csv'
    df.to_csv(csv_file, index=False)
    st.write("Data saved to CSV:", csv_file)

    # Function to determine the color of the marker based on AQI
    def get_marker_color(aqi):
        if aqi <= 50:
            return 'green'  # Good
        elif 51 <= 100:
            return 'yellow'  # Moderate
        else:
            return 'red'  # Bad

    # Create a folium map centered around the UK
    map = folium.Map(location=[54.0, -2.0], zoom_start=6)

    # Add a marker for each city
    for index, row in df.iterrows():
        folium.Marker(
            location=cities[row['region']]['coords'],
            popup=f"{row['city']} (AQI: {row['aqi']})",
            icon=folium.Icon(color=get_marker_color(row['aqi']))
        ).add_to(map)

    # Display the map in the Streamlit app
    st.write("## Air Quality Map")
    folium_static(map)
