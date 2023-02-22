# Belongs-test
Pedestrian Counting System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Task Description](#API-Description)
- [List of Technologies](#List-of-Technologies)
- [Features](#Features)
- [Installation](#Installation)
- [Usage](#Usage)
- [Design and Architecture](#Design-and-Architecture)
- [Deployment Suggestions](#Deployment-Suggestions)
- [License](#License)
- [Contact Information](#Contact-Information)

---

## Task Description

# Extract Stats : Need to show these expected outputs.
- Top 10 (most pedestrians) locations by day
- Top 10 (most pedestrians) locations by month
- Which location has shown most decline due to lockdowns in last 2 years
- Which location has most growth in last year
# Load & Stage Data in an appropriate format for future querying 
- For this purpose you can mock up data visually to represent tables and columns
- What other metrics can be derived that you can suggest from these data sets
- Describe the data model and include a diagram

---

## List of Technologies

I used the following technologies for creating image-labeling-api.
| Technology | Description | Version |
|------------|-------------------------------------------|--------|
| Python | Main programming language | 3.11.2 |
| Sqlite3 | C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine |  |


---

## Features

Belongs-test can extract the following information from the databases:

- Top 10 (most pedestrians) locations by day
- Top 10 (most pedestrians) locations by month
- Location has shown most decline due to lockdowns in last 2 years
- Location has most growth in last year
# Extera useful information
- Average hourly pedestrian counts by location
- Median hourly pedestrian counts by location
- Total pedestrian counts by day of the week
- Total pedestrian counts by month
- Average hourly pedestrian counts by day of the week
- Average hourly pedestrian counts by month
- Percent change in pedestrian counts from one year to the next by location
- Busiest hour of the day by location
- Average hourly pedestrian counts by sensor direction

---

## Installation

After cloning the repository into your local workstation, please install all necessary documents by running,

- pip install -r requirements.txt

---

## Usage

After installing all required libraries, you can run the code in your terminal by,

For requested stats:

$ python extract_stats.py

For requested + suggested stats:

$ python extract_stats_promoted.py


---

### Database design and data modelling

Based on provided datasets, the data model can be described as having two entities: Sensors and Counts.
# The Sensors entity has the following attributes:
- sensor_id (unique identifier for each sensor)
- sensor_description (description of the sensor)
- sensor_name (name of the sensor)
- installation_date (date the sensor was installed)
- sensor_status (status of the sensor)
- note (additional notes about the sensor)
- direction_1 (direction of the sensor)
- direction_2 (direction of the sensor)
- latitude (latitude of the sensor)
- longitude (longitude of the sensor)
- location (location of the sensor)

# The Counts entity has the following attributes:
- id (unique identifier for each count)
- date_time (date and time of the count)
- year (year of the count)
- month (month of the count)
- date (date of the count)
- day (day of the count)
- time (time of the count)
- sensor_id (unique identifier of the sensor)
- sensor_name (name of the sensor)
- hourly_counts (number of pedestrians counted in the given hour)

There is a one-to-many relationship between Sensors and Counts, where one sensor can have multiple counts associated with it. The relationship is - based on the sensor_id attribute, which is a foreign key in the Counts entity, referencing the primary key of the Sensors entity.

![ERD diagram](https://github.com/bakhshi-ali/Belongs-test/blob/main/Diagram.jpg)

---

## License

Belongs-test is licensed under MIT.

---

## Contact Information

My Github username is bakhshi-ali.
