import statistics as st
import math
import random as rd
import pandas as pd
import json

# Define a Python BeetleML class
class BeetleML:
    def __init__(self):
        # Initialize instance variables
        self.train_data = None
        self.train_learn_data = None
        self.model_initialized = True

    def load_training_data(self, file=None):
        """
        Loads training data from a JSON file and initializes the model.

        Args:
            file (str): The name of the JSON file containing training data.

        Returns:
            dict: The loaded training data.
        """
        if file is None:
            raise Exception("(ERR03)Train Data Method Never Provided-->> no training data was passed")
        try:
            __ = "bet" in file
            with open(f"{file}", "r") as f:
                self.train_data = json.load(f)
                # Save the training data into a different file.
                with open("BeetleML\\log\\tld.cml", "w") as _f_:
                    try:
                        _f_.write(self.train_data)
                    except Exception:
                        _f_.write((str(self.train_data)).replace("'", '"'))
                
        except Exception:
            raise Exception(f"(ERR01)File Name doesn't exist-->> No file named {file}")
        if __ is False:
            raise Exception("(ERR02)Invalid File Extension-->> file extension not supported")
        return self.train_data
    
    def load_test_data(self, file=None, ld=None, line=1):
        """
        Loads test data from a file or a provided list.

        Args:
            file (str): The name of the file containing test data.
            ld (list): A list of test data points.
            line (int): Line number in the file (default is 1).

        Returns:
            list: A list containing test data and a line number.
        """
        if ld is None:
            try:
                __ = "bett" in file
                with open(f"{file}")  as _f:
                    t_data_raw = _f.read()
            except Exception:
                raise Exception(f"(ERR01)File Name doesn't exist-->> No file named {file}")
            if __ is False:
                raise Exception("(ERR02)Invalid File Extension-->> file extension not supported")
        elif file is None:
            try:
                t_data_raw = ld
            except Exception as e:
                raise Exception(f"(ERR03)(LD)List Data passed isn't a list\n{e}")
        else:
            raise Exception("(ERR03)Test Data Method Never Provided-->> no testing data was passed")
        
        return [t_data_raw, line]
    
    def start(self, t=None, td=None, n=1, e=True, s=False):
        """
        Starts the BeetleML algorithm by training and making predictions.

        Args:
            t (dict): Training data dictionary.
            td (list): Test data list.
            n (int): Number of times to run the operation.
            e (bool): Flag for JavaScript engine (default is True).
            s (bool): Flag to display statistics (default is False).

        Returns:
            list: A list containing various results and information.
        """
        if t is None:
            raise Exception("(ERR04)Train Data 'None'-->> no training data was passed")
        elif td is None:
            print("(Flag)Test Data 'None'-->> no test data was passed")
        else:
            get_n = 1
            get_e = e
            get_s = s
            train_data = t
            
            # Load previously saved training data
            with open("BeetleML\\log\\tld.cml", "r") as __f:
                train_learn_data = json.load(__f)

            try:
                line = td[1]
            except KeyError:
                line = td

            # Convert data types and initialize test_data
            train_data_n = train_data
            train_learn_data_n = train_learn_data
            try:
                test_data = eval(td[0])
            except Exception:
                test_data = td[0]
            
            # Calculating the Adaptive Difference (a.k.a David's Difference)
            differences = {}
            for keys in train_data_n.keys():
                values = train_data_n[keys]
                d_fs = []

                for di in range(len(values) - 1):
                    ds = values[di + 1]  - values[di]
                    d_fs.append(ds)

                differences[keys] = d_fs

            ad_list = []

            for keys, d_fs_list in differences.items():
                d_b = max(d_fs_list)
                d_s = min(d_fs_list)
                E_d = sum(d_fs_list)

                # Calculate Adaptive Difference
                a_d =  (E_d) / (d_b - d_s)
                ad_list.append(a_d)

            # Adjust training data based on Adaptive Difference
            for each_ad in ad_list:
                def addToEachKey():
                    for k, kv in train_data_n.items():
                        train_data_n[k] = [x + each_ad for x in train_data_n[k]]

            addToEachKey()

            train_learn_data_n = train_data_n

            # print(train_learn_data_n) 
            result = {}
            nc_list = []
            c_list = []

            for _key in train_data_n.keys():
                if _key in train_learn_data_n:
                    result[_key] = [x - y for x, y in zip(train_learn_data_n[_key], train_data_n[_key])]
                
                v = train_data_n[_key]
                val = train_learn_data_n[_key]
                tstdt = test_data
                for d in tstdt:
                    if d >= (min(val) - a_d):
                        if d <= (max(val) + a_d):
                            c_list.append(1)
                        else:
                            nc_list.append(1)
                    elif d <= (max(val) + a_d):
                        c_list.append(1)
                    elif d <= (min(val) - a_d):
                        if d == (min(val) - a_d):
                            if d >= (max(val) + a_d):
                                c_list.append(1)
                            else:
                                nc_list.append(1)
                        elif d < (min(val) - a_d):
                            nc_list.append(1)
                        elif d > (max(val) + a_d):
                            nc_list.append(1)
                    else:
                        raise Exception("(ERR05)Validation Error-->> error encountered while validating")
            

            # Determine predicted class (either Aggresively(a_d < 1) or Conservatively(a_d > 1)) or guess 
            if a_d > 1:
                print("---------------------------[Conservative Mode]---------------------------")
                if len(nc_list) > len(c_list):
                    list_of_names = []
                    for ____keys, ____values in train_data.items():
                        list_of_names.append(____keys)
                    
                    which_key = rd.choice([list_of_names])
                    wh_key = which_key
                    print(f"Unable to predict class therefore guessing class: {rd.choices((which_key))}")
                elif len(c_list) > len(nc_list):
                    try:
                        for tldnkeys in train_learn_data_n.keys():
                            modified_ad = (a_d)
                            LH_MAX = (max(train_learn_data_n[tldnkeys]) - max(test_data))
                            LH_MIN = (min(train_learn_data_n[tldnkeys]) - min(test_data))
                            maximum_validation = (LH_MAX - modified_ad)
                            minimum_validation = (LH_MIN - modified_ad)
                            benchmark_value = 0.000001

                            if maximum_validation <= benchmark_value or minimum_validation <= benchmark_value:
                                which_key = tldnkeys
                            else:
                                pass

                            which_key = tldnkeys
                        print(f"\nPredicted class: {which_key}")
                    except Exception:
                        raise Exception("(ERR06)Class Prediction Error-->> an error must have occured during prediction")
                elif nc_list == c_list:
                    try:
                        keys = []
                        for tldnkeys in train_learn_data_n.keys():
                            modified_ad = (a_d)
                            LH_MAX = (max(train_learn_data_n[tldnkeys]) - max(test_data))
                            LH_MIN = (min(train_learn_data_n[tldnkeys]) - min(test_data))
                            maximum_validation = (LH_MAX - modified_ad)
                            minimum_validation = (LH_MIN - modified_ad)
                            benchmark_value = 0.000001
                            keys.append(tldnkeys)


                            if test_data == train_learn_data_n[keys]:
                                which_key = tldnkeys
                            else:
                                pass

                        print(f"\nPredicted class: {which_key}")
                    except Exception:
                        raise Exception("(ERR06)Class Prediction Error-->> an error must have occured during prediction")
            elif a_d == 0.0:
                print("(Flag)Adaptive difference is 0")
                which_key = ""

            else:
                print(f"---------------------------[Aggressive Mode]---------------------------")
                if len(nc_list) > len(c_list):
                    list_of_names = []
                    for ____keys, ____values in train_data.items():
                        list_of_names.append(____keys)
                    
                    whic_key = rd.choice([list_of_names])
                    print(f"Unable to predict class therefore guessing class: {rd.choices((whic_key))}")
                    which_key = whic_key
                elif len(c_list) > len(nc_list):
                    
                    try:
                        keys = []
                        for tldnkeys in train_learn_data_n.keys():
                            modified_ad = (a_d)
                            LH_MAX = (max(train_learn_data_n[tldnkeys]) - max(test_data))
                            LH_MIN = (min(train_learn_data_n[tldnkeys]) - min(test_data))
                            maximum_validation = (LH_MAX - modified_ad)
                            minimum_validation = (LH_MIN - modified_ad)
                            benchmark_value = 0.000001
                            keys.append(tldnkeys)


                        
                            if maximum_validation <= benchmark_value and minimum_validation <= benchmark_value:
                                wh_key = tldnkeys
                            elif (test_data) == (train_learn_data_n[tldnkeys]):
                                wh_key = tldnkeys
                            elif maximum_validation <= benchmark_value or minimum_validation <= benchmark_value:
                                wh_key = tldnkeys
                            else:
                                wh_key = tldnkeys

                        which_key = wh_key
                        print(f"\nPredicted class: {which_key}")
                    except Exception:
                        raise Exception("(ERR06)Class Prediction Error-->> an error must have occurred during prediction")
                elif nc_list == c_list:
                    try:
                        keys = []
                        for tldnkeys in train_learn_data_n.keys():
                            modified_ad = (a_d)
                            LH_MAX = (max(train_learn_data_n[tldnkeys]) - max(test_data))
                            LH_MIN = (min(train_learn_data_n[tldnkeys]) - min(test_data))
                            maximum_validation = (LH_MAX - modified_ad)
                            minimum_validation = (LH_MIN - modified_ad)
                            benchmark_value = 0.00001
                            keys.append(tldnkeys)


                            if (test_data) == (train_learn_data_n[keys]):
                                wh_key = tldnkeys
                            else:
                                pass

                        which_key = wh_key

                        print(f"\nPredicted class: {which_key}")
                    except Exception:
                        raise Exception("(ERR06)Class Prediction Error-->> an error must have occurred during prediction")
            
            # Define a function to get statistics
            def get_stats(data_list):
                mean = st.mean(data_list)
                median = st.median(data_list)
                mode = st.mode(data_list)
                Range = (max(data_list) - min(data_list))
                stdev = st.stdev(data_list)
                varnc = st.variance(data_list)

                print(f"--Statistical data for {which_key}--------------------------")
                print(f"| >> Mean: {mean}")
                print(f"| >> Median: {median}")
                print(f"| >> Mode: {mode}")
                print(f"| >> Range: {Range}")
                print(f"| >> Standard Deviation: {stdev}")
                print(f"| >> Variance: {varnc}")
                print(f"------------------------------------------------------")

            # Display JavaScript engine info if enabled
            if get_e is True:
                pass
            else:
                print("\n\nJavaScript Engine Coming Soon\n\n")
            
            # Display statistics if enabled
            if get_s is True:
                get_stats(train_data_n[which_key])
            else:
                pass
            
            # Return relevant information
            return [a_d, train_learn_data_n, tstdt, result, c_list, nc_list, train_data_n, which_key, differences]
    
    def predict_next_value(self, Model=None):
        """
        Predicts the next value in the test data based on the trained model.

        Args:
            Model: The trained model object.

        Returns:
            float: The predicted next value.
        """
        if Model is None:
            raise Exception("(ERR07)No Model Error-->> no model was passed")
        else:
            train_data_n = Model[6]
            current_key = Model[7]
            differences = Model[8]

            res_list = []

            if current_key == "":
                pass
            else:
                try:
                    d_fs = differences[current_key]
                except KeyError:
                    print("Can't predict next value")

            try:
                d_b = max(d_fs)
                d_s = min(d_fs)
                E_d = sum(d_fs)

                # Calculate Adaptive Difference
                a_d =  (E_d) / (d_b - d_s)

                # Initialize a sequence
                sequ = train_data_n[current_key]

                # Subtract the the adaptive difference to the last value in the sequence from the already trained data
                next_value = sequ[-1] - a_d

                # Consider predicted value and validate to be sure
                if (min(sequ) - a_d) <= next_value <= (max(sequ) - a_d):
                    nv = next_value
            
                print(f"\nPredicted Next value: {nv}")

                with open("BeetleML\\log\\tld.cml", "r") as _tld:
                    tld_content = _tld.read()
                tld_content = eval(tld_content)

                tld_content[current_key].append(next_value)

                # Appends the predictions to the trained learned data predictions file
                with open("BeetleML\\log\\tldp.cml", "w") as __tldp:
                    __tldp.write(f"{tld_content}")

                return [next_value, current_key]
            except Exception as e:
                print(f"Can't predict next value due to {e}")

    def update_and_predict(self, Model=None, predicted_value=None, save=False):
        """
        Updates the model with a predicted value and makes a new prediction.

        Args:
            Model: The trained model object.
            predicted_value: The value predicted by the model.
            save: Updates it's trained data file based on the prediction
        """
        if predicted_value is None or Model is None:
            raise Exception("(ERR08)No Value/Model Error-->> no predicted value/Model was passed")
        else:
            # Load necessary information
            predicted_val = (predicted_value[0])
            current_key = predicted_value[1]
            with open('BeetleML\\log\\tldp.cml', "r") as _tld__:
                c_data = _tld__.read()

            train_data_n = eval(c_data)

            differences = {}
            d_fs = []

            values = train_data_n[current_key]

            for i in range(len(values) - 1):
                d = values[i + 1] - values[i]
                d_fs.append(d)

            differences[current_key] = d_fs
            d_list = differences[current_key]


            d_b = max(d_list)
            d_s = min(d_list)
            E_d = sum(d_list)

            # Calculate Adaptive Difference
            a_d =  (E_d) / (d_b - d_s)

            # Initialize a sequence
            sequ = train_data_n[current_key]

            # subtract the the adaptive difference from the last value in the list
            next_value = train_data_n[current_key][-1]
            next_next_value = next_value - a_d

            # Consider predicted value and validate to be sure
            if (min(sequ) - a_d) <= next_next_value <= (max(sequ) - a_d):
                nnv = next_next_value

            print(f"\n(UAP)Predicted Next value: {nnv}")

            if save is False:
                pass
            elif save is True:
                with open("BeetleML\\log\\tldp.cml", "r") as _tld:
                    tld_content = _tld.read()
                tld_content = eval(tld_content)

                tld_content[current_key].append(next_value)
                tld_content[current_key].append(next_next_value)

                # Appends the predictions to the trained learned data predictions file
                with open("BeetleML\\log\\tldp.cml", "w") as __tldp:
                    __tldp.write(f"{tld_content}")
            else:
                pass

    def accuracy(self, Model=None):
        """
        Calculates and displays the accuracy of the model.

        Args:
            Model: The trained model object.
        """
        if Model is None:
            raise Exception("(ERR07)No Model Error-->> no model was passed")
        else:
            c_list = Model[4]
            nc_list = Model[5]

            # if len(nc_list) > len(c_list):
            #     calc = (len(nc_list) / ((len(nc_list)) + (len(c_list)))) * 100
            #     print(f"Accuracy: {calc}%")
            # elif len(c_list) > len(nc_list):
            calc = (len(c_list) / ((len(c_list)) + (len(nc_list))))
            print(f"Accuracy: {calc}")
            # else:
            #     calc = (((len(nc_list) + len(c_list)) / 2) / ((len(c_list)) + (len(nc_list))) ) * 100
            #     print(f"Accuracy: {calc}%")

    def related_info(self, Model=None):
        """
        Displays related information about the model and predictions.

        Args:
            Model: The trained model object.
        """
        if Model is None:
            raise Exception("(ERR07)No Model Error-->> no model was passed")
        else:
            print("More Info:")
            adaptive_difference = Model[0]
            trained_data_pattern = Model[1]
            test_data = Model[2]
            results = Model[3]
            c_list = Model[4]
            nc_list = Model[5]
            training_data = Model[6]
            current_key = Model[7]

            try:
                print(f"1.) The training dataset class have an adaptive difference of {adaptive_difference}\n\n2.) The trained data pattern[TDP]: {trained_data_pattern[current_key]}\n\n3.) Test data used: {test_data}\n\n5.) No of Reasons to consider prediction: {len(c_list)}\n\n6.) No of Reasons not to consider prediction: {len(nc_list)}\n")
            except Exception as e:
                current_key = rd.choice(current_key)
                print(f"1.) The training dataset class have an adaptive difference of {adaptive_difference}\n\n2.) The trained data pattern[TDP]: {trained_data_pattern[current_key]}\n\n3.) Test data used: {test_data}\n\n5.) No of Reasons to consider prediction: {len(c_list)}\n\n6.) No of Reasons not to consider prediction: {len(nc_list)}\n")
            if len(nc_list) > len(c_list):
                print("7.) Conclusion: Not considerable")
            elif len(c_list) > len(nc_list):
                print("7.) Conclusion: Considerable")
            
            def stats(data_list):
                mean = st.mean(data_list)
                median = st.median(data_list)
                mode = st.mode(data_list)
                Range = (max(data_list) - min(data_list))
                stdev = st.stdev(data_list)
                varnc = st.variance(data_list)

                print(f"-->>Mean: {mean}")
                print(f"-->>Median: {median}")
                print(f"-->>Mode: {mode}")
                print(f"-->>Range: {Range}")
                print(f"-->>Standard Deviation: {stdev}")
                print(f"-->>Variance: {varnc}\n")

            print("\nStatistics on your data:")
            stats(trained_data_pattern[current_key])
            
            print("------[Finished generating Info]--------")

    def close(self, Model=None):
        """
        Closes the model and releases any associated resources.

        Args:
            Model: The model object to be closed.
        """
        if Model is None:
            raise Exception("(ERR07)No Model Error-->> no model was passed")
        else:
            if self.model_initialized:
                self.model_initialized = False
                with open("BeetleML\\log\\tld.cml", "w") as tld_:
                    tld_.write("")
                print(f"Model disposed!")
            else:
                pass
