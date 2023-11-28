# Models
from engine.BeetleML.BeetleML.BTLAnn import Ann
from engine.BeetleML.BeetleML.BTLLolo import Lolo
from engine.BeetleML.BeetleML.BTLCore import Core
import json
from . import DateSplitter as ds
import datetime

# Get the current date
current_date = datetime.date.today()

# Format the date as "YYYY-MM-DD"
formatted_date = current_date.strftime("%Y-%m-%d")

def funnel(data, filter_object):
    key_residues = []
    value_residues = []

    for filter, filter_children in data.items():
        key_residues.append(filter)
        value_residues.append(filter_children)

    if filter_object in key_residues:
        historical_data = []  # List to store historical data for the corresponding dates in previous years
        for year, months_data in value_residues[key_residues.index(filter_object)].items():
            for month, temperatures in months_data.items():
                historical_data.extend(temperatures)

        # Call BTLAnn function with the historical data list
        forecast_result = BTLAnn(filter_object, formatted_date, historical_data)
        return forecast_result

    else:
        return ""


def LiFo(model, test_data):
    # Calculate adaptive differences for the loaded training data
    model.calculate_adaptive_differences()

    # Adjust training data based on adaptive differences
    model.adjust_data()

    # Make predictions for the test data using LiFo (Last-in, First-out)
    predictions = [model.predict([value]) for value in reversed(test_data)]

    # Return the forecasted value for the specified date
    return predictions

def BTLAnn(city, date, historical_data=None):
    model = Ann()

    # Load existing training data
    with open("samples\\month-temperature.bet", "r") as tdata:
        try:
            train_data = eval(tdata.read())
        except Exception:
            train_data = eval(tdata.read())

    # If historical data is provided, extend the existing training data
    if historical_data:
        train_data[city][str(ds.split_date(date)["Year"])] = historical_data

    month = ds.split_date(date)["MonthW"]
    year = ds.split_date(date)["Year"]
    day = ds.split_date(date)["Day"]
    int_day = int(day)

    # Load data from the previously generated "_lg.bet" file
    try:
        with open("_lg.bet", "r") as ldata:
            lg_data = eval(ldata.read())
    except Exception as e:
        # Handle the exception as needed
        print(f"Error loading data from '_lg.bet': {e}")
        lg_data = {}  # Set an empty dictionary in case of an error

    # Get historical values for the specified date
    historical_values = []
    for historical_year in train_data[city]:
        if historical_year != str(year):
            try:
                historical_values.append(train_data[city][historical_year][month][int_day - 1])
            except KeyError:
                pass  # Handle missing data for the specified date

    # Pass the historical values as test data to the LiFo function
    forecasted_value = LiFo(model, historical_values)

    return [forecasted_value, date]


def BTLLolo(city, date):
	pass

def BTLCore(city, date):
	pass
