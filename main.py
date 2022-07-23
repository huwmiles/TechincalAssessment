import json
from datetime import datetime, timedelta


def open_json(file_path: str) -> dict:
    """Function to open a JSON file from a specified filepath and outputs as a dictionary."""
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data


def generate_datetime_range(start_datetime: datetime, end_datetime: datetime) -> list:
    """Generates a list of integers representing seconds since the start of month (as we can assume all events happen in the same calendar month) 
        between two datetimes with an interval of 1 second."""

    month_start = start_datetime.replace(day=1, hour=0, minute=0, second=0)
    seconds = (start_datetime - month_start).total_seconds()
    end_seconds = (end_datetime - month_start).total_seconds()
    datetime_list = [seconds]
    while seconds < end_seconds:
        seconds = seconds + 1
        datetime_list.append(seconds)
    return datetime_list


# Open the sample data
json_data = open_json("sample_data.json")

# Convert dict into array of datetime objects
video_play_list = [
    [datetime.strptime(item, "%Y-%m-%d %H:%M:%S") for item in list(item.values())]
    for item in json_data.values()
]

# Calculate minimum start and maximum end datetimes
min_start_date = min([item[0] for item in video_play_list])
max_end_date = max([item[1] for item in video_play_list])
month_start = min_start_date.replace(day=1, hour=0, minute=0, second=0)

# Convert list of datetimes into integers to increase efficiency
video_play_list = [
    [(item[0] - month_start).total_seconds(), (item[1] - month_start).total_seconds()]
    for item in video_play_list
]

# Generate time list in seconds between the min and max dates in the data
datetime_list = generate_datetime_range(min_start_date, max_end_date)

# Create list of datetimes and count of active plays for each timestamp
results = []
for x in datetime_list:
    count = 0
    # Assuming a maximum video length of 5 hours, reduce video_play_list to within this range to optimise the next for loop
    max_start_datetime = x + 18000
    min_start_datetime = x - 18000
    reduced_video_play_list = [
        item
        for item in video_play_list
        if item[0] <= max_start_datetime and item[0] >= min_start_datetime
    ]

    # For each video play, calculate if this it is active during the current datetime
    for row in reduced_video_play_list:
        if x >= row[0] and x <= row[1]:
            count = count + 1

    # Only returns datetimes with at least one active play
    if count > 0:
        results.append([x, count])

# Calculate the maximum number of plays at a single time
max_plays = max([item[1] for item in results])

print(f"The maximum number of videos played at a single time is {max_plays}.")
