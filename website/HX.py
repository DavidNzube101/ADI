import datetime

def adaptive_difference_forecast(training_data, target_date):
    # Convert the target_date to a datetime object
    target_date = datetime.datetime.strptime(target_date, "%d %B %Y")

    # Extract values for the given date from the training data
    values_for_date = []
    month_name = target_date.strftime("%B").lower()  # Convert month name to lowercase
    year_str = str(target_date.year)

    if year_str in training_data["Abuja"] and month_name in training_data["Abuja"][year_str]:
        values_for_date.extend(training_data["Abuja"][year_str][month_name])

    # Check if there are values for the given date
    if not values_for_date:
        return None  # or raise an exception, depending on your use case

    # Calculate adaptive differences
    differences = [values_for_date[i + 1] - values_for_date[i] for i in range(len(values_for_date) - 1)]

    # Check if there are differences before forecasting
    if not differences:
        return values_for_date[-1]

    # Forecast the next value using the adaptive difference logic
    forecasted_value = values_for_date[-1] + differences[-1]

    return forecasted_value

with open("month-temperature.bet", "r") as tdata:
    try:
        train_data = eval(tdata.read())
    except Exception:
        train_data = (tdata.read())

# Example usage:
training_data = train_data

target_date = "4 October 2023"
forecasted_value = adaptive_difference_forecast(training_data, target_date)

if forecasted_value is not None:
    print(f"Forecasted value for {target_date}: {forecasted_value}")
else:
    print(f"No data available for {target_date}")
