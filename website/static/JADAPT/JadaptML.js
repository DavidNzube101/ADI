const fs = require('fs');
const math = require('mathjs');
const random = require('random');
const pandas = require('pandas-js');
const jsonfile = require('jsonfile');

class AdaptML {
    constructor() {
        this.trainData = null;
        this.trainLearnData = null;
        this.modelInitialized = true;
    }

    loadTrainingData(file) {
        if (!file) {
            throw new Error("(ERR03) Train Data Method Never Provided -- no training data was passed");
        }
        try {
            if (!file.endsWith('.myml')) {
                throw new Error("(ERR02) Invalid File Extension -- file extension not supported");
            }
            this.trainData = jsonfile.readFileSync(file);
            jsonfile.writeFileSync('AdaptML/log/tld.myml', this.trainData);
        } catch (err) {
            throw new Error(`(ERR01) File Name doesn't exist -- No file named ${file}`);
        }
        return this.trainData;
    }

    loadTestData(file, dataList, line = 1) {
        let tDataRaw = "";
        if (!dataList) {
            try {
                if (!file.endsWith('.mymlt')) {
                    throw new Error("(ERR02) Invalid File Extension -- file extension not supported");
                }
                tDataRaw = fs.readFileSync(file, 'utf8');
            } catch (err) {
                throw new Error(`(ERR01) File Name doesn't exist -- No file named ${file}`);
            }
        } else if (!file) {
            tDataRaw = dataList;
        } else {
            throw new Error("(ERR03) Test Data Method Never Provided -- no testing data was passed");
        }
        return [tDataRaw, line];
    }

    start(t, td, n = 1, e = true, s = false) {
        if (!t) {
            throw new Error("(ERR04) Train Data 'None' -- no training data was passed");
        } else if (!td) {
            throw new Error("(ERR04) Test Data 'None' -- no test data was passed");
        } else {
            let getN = 1;
            let getE = e;
            let getS = s;
            let trainData = t;

            // Load previously saved training data
            this.trainLearnData = jsonfile.readFileSync('AdaptML/log/tld.myml');

            let line = td[1];

            // Convert data types and initialize test_data
            let trainDataN = trainData;
            let trainLearnDataN = this.trainLearnData;
            let test_data = [];
            try {
                test_data = JSON.parse(td[0]);
            } catch (err) {
                test_data = [];
            }

            let res = [];
            for (let key in trainDataN) {
                for (let u = 0; u < trainDataN[key].length - 1; u++) {
                    let d_fs = trainDataN[key][u + 1] - trainDataN[key][u];
                    res.push(d_fs);
                }
            }

            let d_b = math.max(res);
            let d_s = math.min(res);
            let E_d = math.sum(res);

            // Calculate Adaptive Difference
            let a_d = E_d / (d_b - d_s);

            // Adjust training data based on Adaptive Difference
            for (let key in trainLearnDataN) {
                trainLearnDataN[key] = trainLearnDataN[key].map(x => x + a_d);
            }

            let result = {};
            let ncList = [];
            let cList = [];

            for (let key in trainDataN) {
                if (key in trainLearnDataN) {
                    result[key] = trainLearnDataN[key].map((x, i) => x - trainDataN[key][i]);
                }

                let val = trainLearnDataN[key];
                for (let d of test_data) {
                    if (d >= (math.min(val) + a_d)) {
                        if (d <= (math.max(val) + a_d)) {
                            cList.push(1);
                        } else {
                            ncList.push(1);
                        }
                    } else if (d <= (math.max(val) + a_d)) {
                        cList.push(1);
                    } else if (d <= (math.min(val) + a_d)) {
                        if (d === (math.min(val) + a_d)) {
                            if (d >= (math.max(val) + a_d)) {
                                cList.push(1);
                            } else {
                                ncList.push(1);
                            }
                        } else if (d < (math.min(val) + a_d)) {
                            ncList.push(1);
                        } else if (d > (math.max(val) + a_d)) {
                            ncList.push(1);
                        }
                    } else {
                        throw new Error("(ERR05) Validation Error -- error encountered while validating");
                    }
                }
            }

            if (ncList.length > cList.length) {
                let list_of_names = Object.keys(trainData);
                let which_key = random.choice(list_of_names);
                console.log(`Unable to predict class, therefore guessing class: ${which_key}`);
            } else if (cList.length > ncList.length) {
                try {
                    let df = new pandas.DataFrame(trainLearnDataN);
                    let which_key = '';
                    for (let col of df.columns) {
                        if (df[col].max() >= math.min(test_data) && df[col].min() <= math.max(test_data)) {
                            which_key = col;
                        }
                    }
                    console.log(`Predicted class: ${which_key}`);
                } catch (err) {
                    throw new Error("(ERR06) Class Prediction Error -- an error must have occurred during prediction");
                }
            } else if (ncList.length === cList.length) {
                try {
                    let df = new pandas.DataFrame(trainLearnDataN);
                    let which_key = '';
                    for (let col of df.columns) {
                        if (df[col].max() >= math.min(test_data) && df[col].min() <= math.max(test_data)) {
                            which_key = col;
                        }
                    }
                    console.log(`Predicted class: ${which_key}`);
                } catch (err) {
                    throw new Error("(ERR06) Class Prediction Error -- an error must have occurred during prediction");
                }
            }

            function getStats(dataList) {
                let mean = math.mean(dataList);
                let median = math.median(dataList);
                let mode = math.mode(dataList);
                let Range = math.max(dataList) - math.min(dataList);
                let stdev = math.std(dataList);
                let varnc = math.var(dataList);

                console.log(`Mean: ${mean}`);
                console.log(`Median: ${median}`);
                console.log(`Mode: ${mode}`);
                console.log(`Range: ${Range}`);
                console.log(`Standard Deviation: ${stdev}`);
                console.log(`Variance: ${varnc}`);
            }

            if (getE) {
                // JavaScript Engine code here (coming soon)
            } else {
                console.log("\n\nJavaScript Engine Coming Soon\n\n");
            }

            if (getS) {
                for (let key in trainDataN) {
                    let l = trainDataN[key];
                    getStats(l);
                }
            } else {
                // Display statistics if enabled
            }

            return [a_d, trainLearnDataN, test_data, result, cList, ncList, trainDataN];
        }
    }

    predictNextValue(Model) {
        if (!Model) {
            throw new Error("(ERR07) No Model Error -- no model was passed");
        } else {
            let trainDataN = Model[6];

            let resList = [];
            for (let key in trainDataN) {
                for (let u = 0; u < trainDataN[key].length - 1; u++) {
                    let d_fs = trainDataN[key][u + 1] - trainDataN[key][u];
                    resList.push(d_fs);
                }
            }

            let d_b = math.max(resList);
            let d_s = math.min(resList);
            let E_d = math.sum(resList);

            // Calculate Adaptive Difference
            let a_d = E_d / (d_b - d_s);
            for (let k in trainDataN) {
                let sequ = trainDataN[k];
                let nextValue = sequ[sequ.length - 1] + a_d;
                if ((a_d + math.min(sequ)) <= nextValue && nextValue <= (a_d + math.max(sequ))) {
                    console.log(`Predicted Next value: ${nextValue}`);
                }
            }
            return nextValue;
        }
    }

    updateAndPredict(Model, predictedValue) {
        if (!predictedValue || !Model) {
            throw new Error("(ERR08) No Value/Model Error -- no predicted value/Model was passed");
        } else {
            let predictedVal = parseInt(predictedValue);
            let currentData = fs.readFileSync('AdaptML/log/tld.myml', 'utf8');
            currentData = JSON.parse(currentData);

            for (let key in currentData) {
                currentData[key].push(predictedVal);
            }

            let trainDataN = Model[6];

            let resList = [];
            for (let key in trainDataN) {
                for (let u = 0; u < trainDataN[key].length - 1; u++) {
                    let d_fs = trainDataN[key][u + 1] - trainDataN[key][u];
                    resList.push(d_fs);
                }
            }

            let d_b = math.max(resList);
            let d_s = math.min(resList);
            let E_d = math.sum(resList);

            // Calculate Adaptive Difference
            let a_d = E_d / (d_b - d_s);
            for (let k in trainDataN) {
                let sequ = trainDataN[k];
                let nextValue = sequ[sequ.length - 1] + a_d;
                if ((a_d + math.min(sequ)) <= nextValue && nextValue <= (a_d + math.max(sequ))) {
                    console.log(`(UAP) Predicted Next value: ${nextValue}`);
                }
            }
        }
    }

    accuracy(Model) {
        if (!Model) {
            throw new Error("(ERR07) No Model Error -- no model was passed");
        } else {
            let cList = Model[4];
            let ncList = Model[5];

            if (ncList.length > cList.length) {
                let calc = (cList.length / ncList.length) * 100;
                console.log(`Accuracy: ${100 - calc}%`);
            } else if (cList.length > ncList.length) {
                let calc = (ncList.length / cList.length) * 100;
                console.log(`Accuracy: ${100 - calc}%`);
            } else {
                console.log(`Accuracy: 50%`);
            }
        }
    }

    relatedInfo(Model) {
        if (!Model) {
            throw new Error("(ERR07) No Model Error -- no model was passed");
        } else {
            console.log("More Info:");
            let adaptiveDifference = Model[0];
            let trainedDataPattern = Model[1];
            let test_data = Model[2];
            let results = Model[3];
            let cList = Model[4];
            let ncList = Model[5];
            let trainingData = Model[6];

            console.log(`1.) The training dataset classes have an adaptive difference of ${adaptiveDifference}`);
            console.log(`2.) The trained data pattern[TDP]: ${JSON.stringify(trainedDataPattern)}`);
            console.log(`3.) Test data used: ${JSON.stringify(test_data)}`);
            console.log(`4.) Results obtained: ${JSON.stringify(results)}`);
            console.log(`5.) No of Reasons to consider prediction: ${cList.length}`);
            console.log(`6.) No of Reasons not to consider prediction: ${ncList.length}`);
            if (ncList.length > cList.length) {
                console.log("7.) Conclusion: Not considerable");
            } else if (cList.length > ncList.length) {
                console.log("7.) Conclusion: Considerable");
            }

            function getStats(dataList) {
                let mean = math.mean(dataList);
                let median = math.median(dataList);
                let mode = math.mode(dataList);
                let Range = math.max(dataList) - math.min(dataList);
                let stdev = math.std(dataList);
                let varnc = math.var(dataList);

                console.log(`-->> Mean: ${mean}`);
                console.log(`-->> Median: ${median}`);
                console.log(`-->> Mode: ${mode}`);
                console.log(`-->> Range: ${Range}`);
                console.log(`-->> Standard Deviation: ${stdev}`);
                console.log(`-->> Variance: ${varnc}`);
            }

            console.log("\nStatistics on your data:");
            for (let key in trainingData) {
                let trainingDataValues = trainingData[key];
                getStats(trainingDataValues);
            }

            console.log("------[Finished generating Info]--------");
        }
    }

    close(Model) {
        if (!Model) {
            throw new Error("(ERR07) No Model Error -- no model was passed");
        } else {
            if (this.modelInitialized) {
                this.modelInitialized = false;
                console.log("Model destroyed!");
            }
        }
    }
}
