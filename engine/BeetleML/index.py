# from BeetleML.BTLCore import BeetleML
# from BeetleML.BTLLolo import Lolo
from BeetleML.BTLAnn import Ann
# from BeetleML.BTLPersister import Persister
# from BeetleML.BTLAccuracy import Accuracy


# Adaptive Neural Network.


# Sample test data
test_data = [2.94]

# Initialize BlueBeetleML
model = Ann()

# Load training data
model.load_train_data(file="samples\\players-GA-ratio.bet")
# model.load_train_data(file="samples\\month-temperature.bet")
# model.load_train_data(file="samples\\product-revenue.bet")

# Calculate adaptive differences and adjust data
model.calculate_adaptive_differences()
model.adjust_data()

# Make predictions for the test data
predictions = [model.predict(test_data)]

# Actual classes for the test data (you should replace this with actual values)
actual_classes = ["Lionel Messi"]

# Calculate error margin and accuracy
error_margin = model.calculate_error_margin(predictions, actual_classes)
accuracy = model.calculate_accuracy(predictions, actual_classes)
forecast = model.forecast()

print("Predicted Class:", predictions[0])
print("Error Margin:", error_margin)
print("Accuracy:", accuracy)
print("Forecasted Values:", forecast[f'{predictions[0]}'])

























# engine = BeetleML()

# traindata = engine.load_train_data(file=("samples\\month-temperature.bet"))

# testdata = [1.3, 2.5, 3.2, 2.8, 1.9, 2.7, 3.5, 3.1, 2.3, 2.9, 2.1, 2.6, 3.0, 2.4, 2.7, 3.2, 3.5, 3.9, 2.8, 2.2]
# myModel = engine.fit(test=testdata, train=traindata)

# prediction = engine.predict(myModel)
# prediction2 = engine.predict(Persister.load("object-measurements-detector.btl", run=True))
# err = Accuracy.error_margin(prediction, percent=True)
# print(err)






# beetle = BeetleML()
# training_data = {
#     "feature1": [1, 2, 3, 4],
#     "feature2": [5, 6, 7, 8],
# }
# test_data = [5, 6, 7, 8]

# # beetle.load_train_data(file="sample_data.bet")
# model = beetle.fit(test_data, training_data)
# prediction = beetle.predict(Model=model)
# # print(f"This is the prediction: {prediction}")
# # beetle.statistics(model)





# stats = engine.statistics(Model=myModel)


# again = Persister.persist(Model=myModel, filename="object-measurements-detector.btl")
# newPredicyion = Persister.load("object-measurements-detector.btl")
# print(newPredicyion)
# prediction2 = engine.predict(newPredicyion)

# Persister.depersist(again)
# print(f"Prediction for: {engine.predict(Model)}")

# engine.dispose(myModel)