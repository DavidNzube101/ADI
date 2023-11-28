import statistics as st
import math
import random as rd
import pandas as pd
import json

class Lolo:
    """Lolo is a class for managing and analyzing data with adaptive differences."""
    
    def __init__(self):
        self.baseline = None

    def load_train_data(self, listdata=None, file=None):
        """Load training data from either a list or a file.
        
        Args:
            listdata (list): List of training data (optional).
            file (str): File path to load training data from (optional).
        
        Returns:
            str: The loaded training data.
        """
        self.listdata = listdata
        self.file = file
        if file is None:
            listdata = train_data
        else:
            if ".bet" in file:
                with open(f"{file}", "r") as train_data_file:
                    tdf_content = train_data_file.read()
                train_data = tdf_content
                with open("Lolo\\log\\tld.aml", "w") as tldfile:
                    tldfile.write(f"{tdf_content}")
            else:
                print(">> File name not supported")
        return train_data

    def fit(self, test, train=None):
        """Fit a model to the training data and calculate adaptive differences.
        
        Args:
            test (list or dict): Test data for fitting the model.
            train (list or dict): Training data (optional).
        
        Returns:
            list or dict: Results of the fitting process.
        """
        if str(type(train)) == "<class 'list'>":
            try:
                self.baseline = st.mean(train)
                return self.baseline
            except Exception as e:
                raise e
        elif str(type(eval(train))) == "<class 'dict'>":
            train = eval(train)
            train_data = train
            try:
                # Calculate Adaptive Difference
                differences = {}
                for keys in train_data.keys():
                    values = train_data[keys]
                    d_fs = []
                    for di in range(len(values) - 1):
                        ds = values[di + 1] - values[di]
                        d_fs.append(ds)
                    differences[keys] = d_fs

                ad_list = []
                for keys, d_fs_list in differences.items():
                    d_b = max(d_fs_list)
                    d_s = min(d_fs_list)
                    E_d = sum(d_fs_list)

                    # Calculate Adaptive Difference
                    a_d = (E_d) / (d_b - d_s)
                    # a_d = (d_b - d_s) / (E_d)
                    ad_list.append(a_d)

                # Adjust training data based on Adaptive Difference
                for each_ad in ad_list:
                    def addToEachKey():
                        for k, kv in train_data.items():
                            train_data[k] = [x + each_ad for x in train_data[k]]
                            adj_train_data = train_data

                    addToEachKey()
                    with open("Lolo\\log\\tld.aml", "w") as tldfile:
                        adj_train_data = train_data
                        tldfile.write(f"{adj_train_data}")

                key_list = []
                baselines = []
                for keys in train_data.keys():
                    baselines.append(st.mean(train_data[keys]))
                    key_list.append(keys)

                return [a_d, ad_list, key_list, baselines, test, train_data]
            except Exception as e:
                raise e
        else:
            pass

    def predict(self, Model):
        if isinstance(Model, list):
            adaptive_difference, adaptive_difference_list, key_list, baselines, test, baseline_test = Model
        elif isinstance(Model, dict):
            adaptive_difference_list = Model['adaptive_difference_list']
            key_list = Model['key_list']
            baselines = Model['baselines']
            test = Model['test']
            baseline_test = Model['baseline_test']
        else:
            print("Invalid Model format. Please provide a valid Model format.")
            return

        deviations = []

        for baseline in baselines:
            for adl in adaptive_difference_list:
                rdListIndex = rd.randrange(len(test))
                testIndex = test[rdListIndex]
                deviation = baseline - adl  # Calculate the deviation
                deviations.append(deviation)

        # Check if deviations list is empty
        if not deviations:
            print("No deviations found.")
            return

        # Find the minimum deviation and its index
        min_deviation = min(deviations)
        min_deviation_index = deviations.index(min_deviation)

        # Check if min_deviation_index is valid
        if 0 <= min_deviation_index < len(key_list):
            # Get the predicted class
            predicted_class = key_list[min_deviation_index]
            print(f"Predicted Class: {predicted_class}")
            return predicted_class
        else:
            print("Unable to determine a predicted class.")
            return




    def statistics(self, Model, mode=True):
        """Calculate and display statistics for test and training data.
        
        Args:
            Model (list): Model information.
            mode (bool): Determines whether to display detailed statistics (default: True).
        
        Returns:
            None
        """
        adaptive_difference = Model[0]
        test = Model[4]
        train_data = Model[5]

        if mode is True:
            def cal_stats(t, td):
                mean = st.mean(t)
                median = st.median(t)
                mode = st.mode(t)
                Range = (max(t) - min(t))
                stdev = st.stdev(t)
                varnc = st.variance(t)

                print("| >> Statistical data for test data")
                print(f"| >> Adaptive Difference: {adaptive_difference}")
                print(f"| >> Mean: {mean}")
                print(f"| >> Geometric Mean: {st.geometric_mean(t)}")
                print(f"| >> Harmonic Mean: {st.harmonic_mean(t)}")
                print(f"| >> Median: {median}")
                print(f"| >> Mode: {mode}")
                print(f"| >> Range: {Range}")
                print(f"| >> Standard Deviation: {stdev}")
                print(f"| >> Population Standard Deviation: {st.pstdev(t)}")
                print(f"| >> Variance: {varnc}")
                print(f"| >> Population Variance: {st.pvariance(t)}\n\n")

                try:
                    td = eval(td)
                except Exception:
                    for key in td.keys():
                        tdlist = td[key]

                        mean = st.mean(tdlist)
                        median = st.median(tdlist)
                        mode = st.mode(tdlist)
                        Range = (max(tdlist) - min(t))
                        stdev = st.stdev(tdlist)
                        varnc = st.variance(tdlist)

                        print(f"{key}\n| >> Statistical data for train data")
                        print(f"| >> Adaptive Difference: {adaptive_difference}")
                        print(f"| >> Mean: {mean}")
                        print(f"| >> Geometric Mean: {st.geometric_mean(tdlist)}")
                        print(f"| >> Harmonic Mean: {st.harmonic_mean(tdlist)}")
                        print(f"| >> Median: {median}")
                        print(f"| >> Mode: {mode}")
                        print(f"| >> Range: {Range}")
                        print(f"| >> Standard Deviation: {stdev}")
                        print(f"| >> Population Standard Deviation: {st.pstdev(tdlist)}")
                        print(f"| >> Variance: {varnc}")
                        print(f"| >> Population Variance: {st.pvariance(tdlist)}\n\n")

            cal_stats(t=test, td=train_data)
        else:
            def cal_stats(t, td):
                mean = st.mean(t)
                median = st.median(t)
                mode = st.mode(t)
                Range = (max(t) - min(t))

                print("| >> Statistical data for test data")
                print(f"| >> Adaptive Difference: {adaptive_difference}")
                print(f"| >> Mean: {mean}")
                print(f"| >> Median: {median}")
                print(f"| >> Mode: {mode}")
                print(f"| >> Range: {Range}")

                try:
                    td = eval(td)
                except Exception:
                    for key in td.keys():
                        tdlist = td[key]

                        mean = st.mean(tdlist)
                        median = st.median(tdlist)
                        mode = st.mode(tdlist)
                        Range = (max(tdlist) - min(t))

                        print(f"{key}\n| >> Statistical data for train data")
                        print(f"| >> Adaptive Difference: {adaptive_difference}")
                        print(f"| >> Mean: {mean}")
                        print(f"| >> Median: {median}")
                        print(f"| >> Mode: {mode}")
                        print(f"| >> Range: {Range}")

            cal_stats(t=test, td=train_data)

    def dispose(self, Model):
        """Dispose of the model and reset parameters.
        
        Args:
            Model (list): Model information.
        
        Returns:
            None
        """
        self.baseline = None
        with open("Lolo\\log\\tld.aml", "w") as tld_:
            tld_.write("")
        print(f"Model disposed!")
