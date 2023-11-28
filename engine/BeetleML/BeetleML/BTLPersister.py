import random as rd
import os
import statistics as st

class Persister:
    """Persister is a class for saving, loading, and removing models."""

    def __init__(self):
        self.initialize_persistor = True

    @staticmethod
    def persist(Model, filename):
        """Save a model to a file with the specified filename.

        Args:
            Model (list): A list containing model information to be saved, including:
                - adaptive_difference (float): The adaptive difference value.
                - adaptive_difference_list (list): List of adaptive differences for classes.
                - key_list (list): List of class labels.
                - baselines (list): List of baseline values for different classes.
                - test (list): Test data.
                - train_data (dict): Training data.

            filename (str): The name of the file where the model will be saved. 
                            The filename extension should be in .btl.

        Returns:
            str: The filename where the model is saved.
        """
        adaptive_difference = Model[0]
        adaptive_difference_list = Model[1]
        key_list = Model[2]
        baselines = Model[3]
        test = Model[4]
        train_data = Model[5]
        model_number = str(rd.randrange(1000)) + str(rd.randrange(100)) + str(rd.randrange(10)) + str(rd.randrange(1000)) + str(rd.randrange(100)) + str(rd.randrange(10))

        try:
            try:
                with open(f"{filename}", "w") as savedModel:
                    savedModel.write(f"MODEL SCRIPT\nSerial Number: {model_number}\nModel Info:\n{adaptive_difference}\n{adaptive_difference_list}\n{key_list}\n{baselines}\n{test}\n{train_data}")
            except Exception:
                with open(f"{filename}.btl", "w") as savedModel:
                    savedModel.write(f"Model Script:\nSerial Number: {model_number}\nModel Info: {adaptive_difference}\n{adaptive_difference_list}\n{key_list}\n{baselines}\n{test}{train_data}")
        except Exception as e:
            raise e

        print(f"Model saved as {filename.replace('.btl', '')}.btl")
        return filename

    @staticmethod
    def load(filename, run=False):
        """Load a model from a file with the specified filename.

        Args:
            filename (str): The name of the file from which to load the model.
            run (bool): If True, additional processing is performed (default: False).

        Returns:
            list: A list containing loaded model information, including:
                - adaptive_difference (float): The adaptive difference value.
                - adaptive_difference_list (list): List of adaptive differences for classes.
                - key_list (list): List of class labels.
                - baselines (list): List of baseline values for different classes.
                - test (list): Test data.
                - train_data (dict): Training data.
        """
        if run is False:
            try:
                with open(f"{filename}", "r") as savedModel:
                    file = savedModel.readline()
                    serno = savedModel.readline()
                    info = savedModel.readline()
                    adaptive_difference = (savedModel.readline())
                    adaptive_difference_list = (savedModel.readline())
                    key_list = (savedModel.readline())
                    baselines = (savedModel.readline())
                    test = (savedModel.readline())
                    train_data = (savedModel.readline())

                return [adaptive_difference, adaptive_difference_list, key_list, baselines, test, train_data]
            except Exception as e:
                raise e
        else:
            with open(f"{filename}", "r") as savedModel:
                file = savedModel.readline()
                serno = savedModel.readline()
                info = savedModel.readline()
                adaptive_difference = float((savedModel.readline()).replace("\n", ""))
                adaptive_difference_list = list(savedModel.readline())
                key_list = list(savedModel.readline())
                baselines = list(savedModel.readline())
                test = list(savedModel.readline())
                train_data = dict(savedModel.readline())

            baseline_test = st.mean(test)
            tolerance = 1e-6

            deviations = []

            for baseline in baselines:
                for adl in adaptive_difference_list:
                    pass

                if True:
                    rdListIndex = rd.randrange((len(test)))
                    testIndex = test[rdListIndex]
                    deviations.append(round(baseline - adl, len(str(testIndex))))

            def secondOption():
                the_class_list = []
                for i in range(len(adaptive_difference_list)):
                    if (round((baseline_test - adaptive_difference_list[i]), int(tolerance))) <= deviations[i] <= (round((baseline_test + adaptive_difference_list[i]), int(tolerance))):
                        the_class_list.append(key_list[i])
                    elif (round((baseline_test - adaptive_difference_list[i]), int(tolerance))) <= deviations[i] <= ((baseline_test + adaptive_difference_list[i])):
                        the_class_list.append(key_list[i])
                    elif ((baseline_test - adaptive_difference_list[i])) <= deviations[i] <= (round((baseline_test + adaptive_difference_list[i]), int(tolerance))):
                        the_class_list.append(key_list[i])
                    elif ((baseline_test - adaptive_difference_list[i])) <= deviations[i] <= ((baseline_test + adaptive_difference_list[i])):
                        the_class_list.append(key_list[i])
                    elif ((baseline_test - adaptive_difference_list[i])) <= deviations[i] < ((baseline_test + adaptive_difference_list[i])):
                        the_class_list.append(key_list[i])
                    elif ((baseline_test - adaptive_difference_list[i])) < deviations[i] <= ((baseline_test + adaptive_difference_list[i])):
                        the_class_list.append(key_list[i])
                    elif ((baseline_test - adaptive_difference_list[i])) < deviations[i] < ((baseline_test + adaptive_difference_list[i])):
                        the_class_list.append(key_list[i])

                try:
                    return [rd.randint(0, len(the_class_list) - 1), the_class_list]
                except Exception:
                    print("(G)")
                    the_class_list = key_list
                    return [rd.randint(0, len(the_class_list) - 1), the_class_list]

            for deviation in deviations:
                if deviation == baseline_test:
                    print(f"Class: {key_list[deviations.index(deviation)]}")

            if (deviation == baseline_test) is False:
                prediction = secondOption()
                print(f"Class: {prediction[1][0]}")

    @staticmethod
    def depersist(persisted_model):
        """Remove a persisted model file.

        Args:
            persisted_model (str): The name of the persisted model file to remove.

        Returns:
            str: A message indicating the removal of the model file.
        """
        try:
            os.remove(persisted_model)
        except Exception as e:
            raise e

        return f"Depersisted Model {persisted_model}"
