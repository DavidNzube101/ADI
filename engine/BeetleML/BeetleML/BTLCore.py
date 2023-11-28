import statistics as st
import math
import random as rd
import pandas as pd
import json

class Core:
    """BeetleML is a class for managing and analyzing data with adaptive differences."""
    
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
                with open("BeetleML\\log\\tld.aml", "w") as tldfile:
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
                    with open("BeetleML\\log\\tld.aml", "w") as tldfile:
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
        """Predict the class based on the model and test data.
        
        Args:
            Model (list): Model information containing adaptive differences, etc.
        
        Returns:
            predicted_value: Predicted Value
        """
        try:
            adaptive_difference = Model[0]
            adaptive_difference_list = Model[1]
            key_list = Model[2]
            baselines = Model[3]
            test = Model[4]
            baseline_test = st.mean(test)
            tolerance = 1e-6
            deviations = []
            # print(adaptive_difference_list)

            if test:
                for baseline in baselines:
                    for adl in adaptive_difference_list:
                        pass

                    if True:
                        rdListIndex = rd.randrange(len(test))
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
                except Exception as e:
                    print(f"(G)-> {e}")
                    the_class_list = key_list
                    return [rd.randint(0, len(the_class_list) - 1), the_class_list]

            for deviation in deviations:
                if deviation == baseline_test:
                    predicted_class = key_list[deviations.index(deviation)]

            try:
                print(f"Class: {predicted_class}")
            except Exception:
                prediction = secondOption()
                print(f"Class: {prediction[1][0]}")

            try:
                return [baselines, baseline_test, key_list, predicted_class]
            except Exception:
                return [baselines, baseline_test, key_list, prediction[1]]

        except Exception:
            try:
                adaptive_difference = eval(Model[0])
                adaptive_difference_list = eval(Model[1])
                key_list = eval(Model[2])
                baselines = eval(Model[3])
            except Exception:
                adaptive_difference = (Model[0])
                adaptive_difference_list = (Model[1])
                key_list = (Model[2])
                baselines = (Model[3])

            try:
                test = eval(Model[4])
            except Exception:
                test = (Model[4])
            baseline_test = st.mean(test)
            tolerance = 1e-6
            deviations = []

            if test:
                for baseline in baselines:
                    for adl in adaptive_difference_list:
                        pass

                    if True:
                        rdListIndex = rd.randrange(len(test))
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
                except Exception as e:
                    print(f"(G)-> {e}")
                    the_class_list = key_list
                    return [rd.randint(0, len(the_class_list) - 1), the_class_list]

            for deviation in deviations:
                if deviation == baseline_test:
                    predicted_class = key_list[deviations.index(deviation)]

            try:
                print(f"Class: {predicted_class}")
            except Exception:
                prediction = secondOption()
                print(f"Class: {prediction[1][0]}")

            try:
                return [baselines, baseline_test, key_list, predicted_class]
            except Exception:
                return [baselines, baseline_test, key_list, prediction[1]]

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
        with open("BeetleML\\log\\tld.aml", "w") as tld_:
            tld_.write("")
        print(f"Model disposed!")
