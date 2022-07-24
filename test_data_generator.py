from random import randrange
from datetime import timedelta, datetime
import json


def random_date_int(start, end):
    "Returns a random int representing a datetime between a start and end datetime."
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


# Define the start and end datetime
d1 = datetime.strptime("2022-07-01 00:00:00", "%Y-%m-%d %H:%M:%S")
d2 = datetime.strptime("2022-07-31 00:00:00", "%Y-%m-%d %H:%M:%S")

# Create dictionary structure from the random datetimes
emtpy_list = []
column_names = ["startDate", "endDate"]
for x in range(100):
    start_date = random_date_int(d1, d2)
    # Assuming maximum video length of 5 hours, generate a random end datetime
    end_date = start_date + timedelta(seconds=randrange(18000))
    date_list = [
        start_date.strftime("%Y-%m-%d %H:%M:%S"),
        end_date.strftime("%Y-%m-%d %H:%M:%S"),
    ]
    emtpy_list.append(dict(zip(column_names, date_list)))

empty_dict = {}
id = 0
for x in emtpy_list:
    empty_dict[f"VideoPlay_{id}"] = x
    id = id + 1

# Output Sample Data
with open("sample_data.json", "w") as f:
    json.dump(dict(empty_dict), f, ensure_ascii=False)
