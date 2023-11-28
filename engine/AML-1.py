import statistics as st
import math
import random as rd
import pandas as pd
import json

class AdaptML:
    def __init__(self):
        self.train_data = None
        self.train_learn_data = None
        self.model_initialized = True

    def load_training_data(self, file=None):
        if file is None:
            raise Exception("(ERR03)Train Data Method Never Provided-->> no training data was passed")
        try:
            __ = "myml" in file
            with open(f"{file}", "r") as f:
                self.train_data = json.load(f)
                # self.train_learn_data = f.read()
                # print("hshsh: " + self.train_learn_data)

                with open("AdaptML\\log\\tld.myml", "w") as _f_:
                    try:
                        _f_.write(self.train_data)
                    except Exception:
                        _f_.write((str(self.train_data)).replace("'", '"'))
                
        except Exception:
            raise Exception(f"(ERR01)File Name doesn't exist-->> No file named {file}")
        if __ is False:
            raise Exception("(ERR02)Invalid File Extension-->> file extension not supported")
        return self.train_data
    
    def load_test_data(self, file=None, data_list=None,line=1):
        if data_list is None:
            try:
                __ = "mymlt" in file
                with open(f"{file}")  as _f:
                    t_data_raw = _f.read()
            except Exception:
                raise Exception(f"(ERR01)File Name doesn't exist-->> No file named {file}")
            if __ is False:
                raise Exception("(ERR02)Invalid File Extension-->> file extension not supported")
        elif file is None:
            t_data_raw = data_list
        
        else:
            raise Exception("(ERR03)Test Data Method Never Provided-->> no testing data was passed")
        
        return [t_data_raw, line]
    
    def start(self, t=None, td=None, n=1, e=True, s=False):
        if t is None:
            raise Exception("(ERR04)Train Data 'None'-->> no training data was passed")
        elif td is None:
            raise Exception("(ERR04)Test Data 'None'-->> no test data was passed")
        else:
            get_n = 1
            get_e = e
            get_s = s
            train_data = t
            with open("AdaptML\\log\\tld.myml", "r") as __f:
                train_learn_data = json.load(__f)

            try:
                line = td[1]
            except KeyError:
                line = td

            # print(type(train_data))
            train_data_n = (train_data)
            train_learn_data_n = (train_learn_data)
            try:
                test_data = eval(td[0])
            except KeyError:
                test_data = td
            
            # Calculating the Adaptive Difference(a.k.a David's Difference)

            res = []

            for _key_, _values_ in train_data_n.items():
                for u in range(len(list(train_data_n[_key_]))-1):
                    d_fs = train_data_n[_key_][u + 1] - train_data_n[_key_][u]
                    print(f"{train_data_n[_key_][u + 1]} - {train_data_n[_key_][u]}")
                res.append(d_fs)
            d_b = max(res)
            d_s = min(res)
            E_d = sum(res)

            # Adaptive Difference
            a_d =  (E_d) / (d_b - d_s)
            # print(a_d)
            for __key in train_learn_data_n.keys():
                train_learn_data_n[__key] = [x + a_d for x in train_learn_data_n[__key]]

            
            result = {}
            nc_list = []
            c_list = []

            for _key in train_data_n.keys():
                if _key in train_learn_data_n:
                    result[_key] = [x - y for x, y in zip(train_learn_data_n[_key], train_data_n[_key])]
                
                v = train_data_n[_key]
                val = train_learn_data_n[_key]
                # print(val)
                # diff = [j - k for j, k in zip(val, v)]
                tstdt = test_data
                for d in tstdt:
                    if d >= (min(val) + a_d):
                        if d <= (max(val) + a_d):
                            c_list.append(1)
                        else:
                            nc_list.append(1)
                    
                    elif d <= (max(val) + a_d):
                        c_list.append(1)
                

                    elif d <= (min(val) + a_d):
                        if d == (min(val) + a_d):
                            if d >= (max(val) + a_d):
                                c_list.append(1)
                            else:
                                nc_list.append(1)

                        elif d < (min(val) + a_d):
                            nc_list.append(1)
                        elif d > (max(val) + a_d):
                            nc_list.append(1)
                    else:
                        raise Exception("(ERR05)Validation Error-->> error encountered while validating")

            
            if len(nc_list) > len(c_list):
                list_of_names = []
                for ____keys, ____values in train_data.items():
                    list_of_names.append(____keys)
                
                which_key = rd.choice([list_of_names])
                print(f"Unable to predict class therefore guessing class: {rd.choices((which_key))}")

            elif len(c_list) > len(nc_list):
                try:
                    df = pd.DataFrame(train_learn_data_n)
                    for col in df.columns:
                        if df[col].max() >= min(test_data) and df[col].min() <= max(test_data):
                            which_key = col
                        else:
                            pass
                    print(f"\nPredicted class: {which_key}")
                except Exception:
                    raise Exception("(ERR06)Class Prediction Error-->> an error must have occured during prediction")
            elif nc_list == c_list:
                try:
                    df = pd.DataFrame(train_learn_data_n)
                    for col in df.columns:
                        if df[col].max() >= min(test_data) and df[col].min() <= max(test_data):
                            which_key = col
                        else:
                            pass
                    print(f"\nPredicted class: {which_key}")
                except Exception:
                    raise Exception("(ERR06)Class Prediction Error-->> an error must have occured during prediction")

            
            def get_stats(data_list):
                mean = st.mean(data_list)
                median = st.median(data_list)
                mode = st.mode(data_list)
                Range = (max(data_list) - min(data_list))
                stdev = st.stdev(data_list)
                varnc = st.variance(data_list)

                print(f"Mean: {mean}")
                print(f"Median: {median}")
                print(f"Mode: {mode}")
                print(f"Range: {Range}")
                print(f"Standard Deviation: {stdev}")
                print(f"Variance: {varnc}")

            if get_e is True:
                pass
            else:
                print("\n\nJavaScript Engine Coming Soon\n\n")
            if get_s is True:
                for __keys_, __values_ in train_data_n.items():
                    l = __values_
                    get_stats(l)
            else:
                pass
            return [a_d, train_learn_data_n, tstdt, result, c_list, nc_list, train_data_n, which_key]
    
    def predict_next_value(self, Model=None):
        if Model is None:
            raise Exception("(ERR07)No Model Error-->> no model was passed")
        else:
            # predict_class = False
            train_data_n = Model[6]
            current_key = Model[7]

            res_list = []

            
            for u in range(len(list(train_data_n[current_key]))-1):
                d_fs = train_data_n[current_key][u + 1] - train_data_n[current_key][u]
                res_list.append(d_fs)

            d_b = max(res_list)
            d_s = min(res_list)
            E_d = sum(res_list)

            # Adaptive Difference
            a_d =  (E_d) / (d_b - d_s)
            sequ = train_data_n[current_key]
            next_value = sequ[-1] + a_d
            # print(sequ)
            if (a_d + min(sequ)) <= next_value <= (a_d + max(sequ)):
                # print(sequ[-1])
                pass
            print(f"\nPredicted Next value: {next_value}")

            return [next_value, current_key]

    def update_and_predict(self, Model=None, predicted_value=None):
        if predicted_value is None or Model is None:
            raise Exception("(ERR08)No Value/Model Error-->> no predicted value/Model was passed")
        else:
            predicted_val = int(predicted_value[0])
            current_key = predicted_value[1]
            with open('AdaptML\\log\\tld.myml', "r") as _f__:
                current_data = _f__.read()

            current_data = (eval(current_data))
            for kk, vv in current_data.items():
                current_data[kk].append(predicted_val)

            # print(f"CD: {current_data[kk]}")


            train_data_n = Model[6]

            res_list = []
            sequ = train_data_n[current_key]
            for u in range(len(list(train_data_n[current_key]))-1):
                d_fs = train_data_n[current_key][u + 1] - train_data_n[current_key][u]
                res_list.append(d_fs)


            d_b = max(res_list)
            d_s = min(res_list)
            E_d = sum(res_list)

            # Adaptive Difference
            a_d =  (E_d) / (d_b - d_s)

            next_value = sequ[-1] + a_d
            res_list.append(next_value)
            train_data_n[current_key].append(next_value)
            # print(res_list)
            next_next_value = res_list[-1] + a_d
            # print(sequ)
            if (a_d + min(sequ)) <= next_value <= (a_d + max(sequ)):
                # print(sequ[-1])
                print(f"\n(UAP)Predicted Next value: {next_next_value}\n")


    def accuracy(self, Model=None):
        if Model is None:
            raise Exception("(ERR07)No Model Error-->> no model was passed")
        else:
            c_list = Model[4]
            nc_list = Model[5]
            
            if len(nc_list) > len(c_list):
                calc = (len(nc_list) / ((len(nc_list)) + (len(c_list)))) * 100
                print(f"Accuracy: {calc}%")
            elif len(c_list) > len(nc_list):
                calc = (len(c_list) / ((len(c_list)) + (len(nc_list)))) * 100
                print(f"Accuracy: {calc}%")
            else:
                calc = (((len(nc_list) + len(c_list)) / 2) / ((len(c_list)) + (len(nc_list))) ) * 100
                print(f"Accuracy: {calc}%")

    def related_info(self, Model=None):
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
            class_key = Model[7]

            print(f"1.) The predicted training dataset class has an adaptive difference of {adaptive_difference}\n\n2.) The training dataset class: {trained_data_pattern[class_key]}\n\n3.) Test data used: {test_data}\n\n4.) Results obtained: {results[class_key]}\n\n5.) No of Reasons to consider prediction: {c_list}\n\n6.) No of Reasons not to consider prediction: {nc_list}\n")
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
            for _keys__, _values__ in training_data.items():
                training_data_values = _values__
                stats(training_data_values)
            
            print("------[Finished generating Info]--------")



    
    def close(self, Model=None):
        if Model is None:
            raise Exception("(ERR07)No Model Error-->> no model was passed")
        else:
            if self.model_initialized:
                self.model_initialized = False
                with open("AdaptML\\log\\tld.myml", "w") as tld_:
                    tld_.write("")
                print("Model Disposed")
            else:
                pass


