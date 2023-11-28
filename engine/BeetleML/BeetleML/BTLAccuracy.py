class Accuracy:
    """Accuracy is a class for calculating error margins in predictions."""

    def __init__(self):
        self.initialize_accuracy = True

    @staticmethod
    def error_margin(prediction, percent=False):
        if prediction is None:
            print("Error: Unable to calculate error margin due to None prediction.")
            return None
        else:
            """Calculate the error margin of a prediction.

            Args:
                prediction (list): A list containing information about the prediction, including:
                    - baselines (list): List of baseline values for different classes.
                    - baseline_test (float): Baseline value for the test data.
                    - key_list (list): List of class labels.
                    - predicted_class (str): Predicted class label.

                percent (bool): If True, return the error margin as a percentage (default: False).

            Returns:
                float or str: The error margin, rounded to two decimal places.
                              If `percent` is True, returns the error margin as a percentage.
            """
            baselines = prediction[0]
            baseline_test = prediction[1]
            key_list = prediction[2]
            predicted_class = prediction[3]

            try:
                predicted_class_index = key_list.index(predicted_class[0])
            except Exception:
                predicted_class_index = key_list.index(predicted_class)

            accuracy = ((((baselines[predicted_class_index] - baseline_test) * 100) - 100) * 2)
            accuracy = round(abs(accuracy), 1)

            if percent is True:
                return f"{accuracy}%"
            else:
                return accuracy
