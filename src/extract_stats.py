import pandas as pd
import sqlite3
from datetime import datetime
import os


# Get the absolute path of the script
script_path = os.path.abspath(__file__)
# Get the directory containing the script
script_dir = os.path.dirname(script_path)
# Change the working directory to the directory containing the script
os.chdir(script_dir)

# Load the sensors data
path_to_the_sensor_dataset = '../pedestrian-counting-system-sensor-locations.csv'
path_to_the_counts_dataset = '../Pedestrian_Counting_System_Monthly_counts_per_hour_may_2009_to_14_dec_2022.csv'
sensors_df = pd.read_csv(path_to_the_sensor_dataset)
# Load the counts data
counts_df = pd.read_csv(path_to_the_counts_dataset)


# Print the column names of the first table
print('Columns in sensors_df:')
print(sensors_df.columns)
# Print the column names of the second table
print('Columns in counts_df:')
print(counts_df.columns)


# Merge the two tables on the sensor_id and Sensor_ID columns
merged_df = pd.merge(sensors_df, counts_df, left_on='sensor_id', right_on='Sensor_ID')

# Convert the dat_time column to a datetime object
merged_df['Date_Time'] = pd.to_datetime(merged_df['Date_Time'])

# Add a column for day of the week
merged_df['day_of_week'] = merged_df['Date_Time'].dt.day_name()

# Add a column for year
merged_df['year'] = merged_df['Date_Time'].dt.year

# Add a column for month
merged_df['month'] = merged_df['Date_Time'].dt.month

# Add a column for date
merged_df['date'] = merged_df['Date_Time'].dt.date

# Add a column for hour
merged_df['hour'] = merged_df['Date_Time'].dt.hour

# Top 10 (most pedestrians) locations by day
top10_day = merged_df.groupby(['date', 'location'])['Hourly_Counts'].sum().reset_index().\
    sort_values(by='Hourly_Counts', ascending=False).groupby('date').head(10)

print("Top 10 (most pedestrians) locations by day:")
print(top10_day)

# Top 10 (most pedestrians) locations by month
top10_month = merged_df.groupby(['year', 'month', 'location'])['Hourly_Counts'].sum().reset_index().\
    sort_values(by='Hourly_Counts', ascending=False).groupby(['year', 'month']).head(10)

print("Top 10 (most pedestrians) locations by month:")
print(top10_month)

# Which location has shown most decline due to lockdowns in last 2 years
current_year = merged_df['year'].max()
two_years_ago = current_year - 2

last_two_years = merged_df[(merged_df['year'] >= two_years_ago) & (merged_df['year'] <= current_year)]
lockdown_dates = [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in ['2020-03-23', '2022-08-06']]
lockdown_df = last_two_years[last_two_years['date'].isin(lockdown_dates)]

lockdown_counts = lockdown_df.groupby(['location'])['Hourly_Counts'].sum().reset_index()

total_counts = last_two_years.groupby(['location'])['Hourly_Counts'].sum().reset_index()

combined_counts = pd.merge(total_counts, lockdown_counts, on='location')
combined_counts['percent_change'] = (combined_counts['Hourly_Counts_x'] - combined_counts['Hourly_Counts_y']) / combined_counts['Hourly_Counts_x']

most_decline = combined_counts.loc[combined_counts['percent_change'].idxmax(), 'location']

print("Location with the most decline due to lockdowns in the last 2 years:")
print(most_decline)

# Which location has most growth in last year
last_year = merged_df[merged_df['year'] == current_year - 3]
growth_df = last_year.groupby(['location'])['Hourly_Counts'].sum().reset_index().\
    sort_values(by='Hourly_Counts', ascending=False)

most_growth = growth_df.loc[growth_df['Hourly_Counts'].idxmax(), 'location']
most_growth_count = growth_df.loc[growth_df['Hourly_Counts'].idxmax(), 'Hourly_Counts']
print(f"Location with the most growth in the last year is in {most_growth} and the hourly count is {most_growth_count}")


# Create a connection to a SQLite database
connect_to_sqlite = sqlite3.connect('pedestrian_counts.db')
# Insert the sensors data into the database
sensors_df.to_sql('sensors', connect_to_sqlite, if_exists='replace', index=False)
# Insert the counts data into the database
counts_df.to_sql('counts', connect_to_sqlite, if_exists='replace', index=False)
print("Data Inserted to the database successfully")

# Execute a SQL query to retrieve data from the sensors table
sensors_data = pd.read_sql_query("SELECT * from sensors", connect_to_sqlite)
print('Retrived Sensor data from database', sensors_data)
# Execute a SQL query to retrieve data from the counts table
counts_data = pd.read_sql_query("SELECT * from counts", connect_to_sqlite)
print('Retrived Sensor data from database', counts_data)


# Define a list of dictionaries containing the results
results = [
    {'type': 'Location with the most decline due to lockdowns in the last 2 years', 'data': most_decline},
    {'type': 'Location with the most growth in the last year', 'data': most_growth},
]

# Create an empty DataFrame
summary_table = pd.DataFrame()

# Iterate over the results and append them to the summary table
for result in results:
    # Get the type and data of the result
    result_type = result['type']
    result_data = result['data']
    # Create a new DataFrame with the type and data
    result_df = pd.DataFrame({'type': [result_type], 'data': [result_data]})
    # Append the new DataFrame to the summary table
    summary_table = summary_table.append(result_df, ignore_index=True)

print('*************************** Summary of all results ***************************')
# Print the summary table
print(summary_table)
print("Top 10 (most pedestrians) locations by day:")
print(top10_day)
print("Top 10 (most pedestrians) locations by month:")
print(top10_month)