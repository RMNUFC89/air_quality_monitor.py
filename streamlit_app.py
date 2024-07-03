import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Your AQICN API key
api_key = 'dd88e9b11b0d167c66e46b3338a4b4b0fd2127f9'

# Main cities for each region in the UK
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
    "South East England": "Brighton and Hove",
    "East of England": "Norwich",
    "South West England": "Bristol"
}

# Function to fetch air quality data for a specific city
def fetch_air_quality(city):
    url = f"http://api.waqi.info/feed/{city}/?token={api_key}"
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    data = response.json()
    if data['status'] == 'ok':
        return data['data']
    else:
        raise Exception(f"Error fetching data for {city}: {data['data']}")

# Fetch air quality data for each city and region
air_quality_data = []

for region, city in cities.items():
    try:
        city_data = fetch_air_quality(city)
        air_quality_data.append({
            'region': region,
            'city': city,
            'aqi': city_data['aqi'],
            'pm25': city_data['iaqi']['pm25']['v'] if 'pm25' in city_data['iaqi'] else None,
            'pm10': city_data['iaqi']['pm10']['v'] if 'pm10' in city_data['iaqi'] else None,
            'no2': city_data['iaqi']['no2']['v'] if 'no2' in city_data['iaqi'] else None,
            'so2': city_data['iaqi']['so2']['v'] if 'so2' in city_data['iaqi'] else None,
            'co': city_data['iaqi']['co']['v'] if 'co' in city_data['iaqi'] else None,
            'o3': city_data['iaqi']['o3']['v'] if 'o3' in city_data['iaqi'] else None
        })
    except Exception as e:
        print(f"Error fetching data for {city}: {e}")

# Convert the data into a pandas DataFrame
df = pd.DataFrame(air_quality_data)

# Display the DataFrame using Streamlit
st.title("Air Quality Data for UK Regions")
st.dataframe(df)

# Save the DataFrame to a CSV file
df.to_csv('uk_air_quality_data.csv', index=False)
st.write("Data saved to CSV: uk_air_quality_data.csv")
