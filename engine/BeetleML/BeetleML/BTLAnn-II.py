import statistics as st
import random as rd

class Ann:
    def __init__(self):
        self.data = {}  # Dictionary to store training data
        self.adaptive_differences = {} # Dictionary to store adaptive differences
        self.l_adaptive_differences = []  # List to store adaptive differences
        self.adjusted_data = {}  # Dictionary to store adjusted data
        self.l_adjusted_data = []

    def load_train_data(self, data=None, file=None):
        """Load training data from a dictionary or a file."""
        if data is not None:
            self.data = data  # Set the data attribute to the provided data
            return self.data  # Return the loaded data
        elif file is not None:
            try:
                with open(file, "r") as the_data:
                    self.data = eval(the_data.read())  # Read and evaluate the file contents
                return self.data  # Return the loaded data
            except Exception as e:
                raise Exception(f"Error loading data from the file\n\nDetails-->> {e}")
        else:
            raise Exception("No data or file provided")


    def calculate_adaptive_differences(self):
        """Calculate adaptive differences for each month in the training data."""
        if str(type(self.data)) == "<type 'dict'>":
            for month, values in self.data.items():
                differences = [values[i + 1] - values[i] for i in range(len(values) - 1)]
                # print(f"U->> {sum(differences) / (max(differences) - min(differences))}")
                # print(f"D->> {(max(differences) - min(differences)) / sum(differences)}")
                box = [1, 2]
                fiddle = rd.choice(box)
                try:
                    adaptive_difference = (max(differences) - min(differences)) / sum(differences)
                except:
                    adaptive_difference = sum(differences) / (max(differences) - min(differences))

                self.adaptive_differences[month] = adaptive_difference
        else:
            for values in self.data:
                differences = [values[i + 1] - values[i] for i in range(len(values) - 1)]
                # print(f"U->> {sum(differences) / (max(differences) - min(differences))}")
                # print(f"D->> {(max(differences) - min(differences)) / sum(differences)}")
                box = [1, 2]
                fiddle = rd.choice(box)
                try:
                    adaptive_difference = (max(differences) - min(differences)) / sum(differences)
                except:
                    adaptive_difference = sum(differences) / (max(differences) - min(differences))

                self.l_adaptive_differences = adaptive_difference

    def adjust_data(self):
        """Adjust training data based on adaptive differences."""
        if str(type(self.data)) == "<class 'dict'>":
            for month, values in self.data.items():
                adaptive_difference = self.adaptive_differences[month]
                self.adjusted_data[month] = [value + adaptive_difference for value in values]

            with open("tldp.aml", "w") as lg:
                lg.write(str(self.adaptive_differences[month]))

        else:
            for values in self.data:
                adaptive_difference = self.l_adaptive_differences
                self.l_adjusted_data = [value + adaptive_difference for value in values]
        

    def predict(self, test_data):
        """Make predictions for the test data."""
        if str(type(self.data)) == "<class 'dict'>":
            test_mean = st.mean(test_data)
            closest_month = None
            closest_difference = float('inf')

            for month, values in self.adjusted_data.items():
                adjusted_mean = st.mean(values)
                difference = abs(test_mean - adjusted_mean)

                if difference < closest_difference:
                    closest_difference = difference
                    closest_month = month

            return closest_month

        else:
            test_mean = st.mean(test_data)
            closest_month = None
            closest_difference = float('inf')

            for values in self.l_adjusted_data:
                adjusted_mean = st.mean(values)
                difference = abs(test_mean - adjusted_mean)

                if difference < closest_difference:
                    closest_difference = difference

            return closest_difference
            

    def calculate_error_margin(self, predictions, actual):
        """Calculate the error margin for predictions."""
        total_errors = sum(1 for p, a in zip(predictions, actual) if p != a)
        return total_errors / len(actual)

    def calculate_accuracy(self, predictions, actual):
        """Calculate the accuracy of predictions."""
        correct_predictions = sum(1 for p, a in zip(predictions, actual) if p == a)
        return correct_predictions / len(actual)

    def forecast(self):
        # Calculate adaptive differences for the loaded training data
        self.calculate_adaptive_differences()
        
        # Adjust training data based on adaptive differences
        self.adjust_data()

        # Predict future values
        future_data = {}
        l_future_data = []
        if str(type(self.data)) == "<class 'dict'>":
            for month, values in self.adjusted_data.items():
                # Calculate the forecast (mean of the current month's data)
                forecast_value = st.mean(values)

                # Append the forecasted value to the adjusted data
                values.append(forecast_value)

                # Store the forecasted value in the future_data dictionary
                future_data[month] = [forecast_value]

            return future_data

        else:
            for values in self.l_adjusted_data:
                # Calculate the forecast (mean of the current month's data)
                forecast_value = st.mean(values)

                # Append the forecasted value to the adjusted data
                values.append(forecast_value)

                # Store the forecasted value in the future_data dictionary
                l_future_data = [forecast_value]

            return l_future_data

    def persist(self):
    	pass