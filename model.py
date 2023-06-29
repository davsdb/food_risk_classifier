import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from sklearn.model_selection import KFold
from keras.optimizers import SGD

df = pd.read_csv(r"path...\RASFF_data.csv", sep = ";")

df.drop(["NOTIFICATION COUNTRY"], inplace=True, axis=1)

df.replace({"not serious": 0, "serious": 1}, inplace = True)

for column in ["DATE CASE", "TYPE", "PRODUCT CATEGORY", "PRODUCT",
               "HAZARD", "ORIGIN COUNTRY"]:
    df[column] = df[column].astype("category")

df = pd.get_dummies(data=df,columns=["DATE CASE", "TYPE", "PRODUCT CATEGORY", "PRODUCT", 
                                     "HAZARD", "ORIGIN COUNTRY"])

X = df.drop("RISK DECISION", axis = 1).values
y = df["RISK DECISION"].values

def train_test_split(X, y, test_size = 0.05, random_state = None):
    
    if random_state != None:
        np.random.seed(random_state)
    
    n = X.shape[0]
    
    test_indices = np.random.choice(n, int(n*test_size), replace = False)
    
    X_test = X[test_indices]
    y_test = y[test_indices]
    
    X_train = np.delete(X, test_indices, axis = 0)
    y_train = np.delete(y, test_indices, axis = 0)
    
    return(X_train, X_test, y_train, y_test)

X_train, X_test, y_train, y_test = train_test_split(X, y)

accuracy_per_fold = []
loss_per_fold = []

k_fold = KFold(n_splits = 5, 
               shuffle = True)

fold_number = 1

inputs = X_train
targets = y_train

for train, test in k_fold.split(inputs, targets):
    
    model = tf.keras.Sequential([
        layers.Dense(4, activation = "relu", input_dim = X_train.shape[1], name = "layer_1"),
        layers.Dense(8, activation = "relu", name = "layer_2"),
        layers.Dense(16, activation = "relu", name = "layer_3"),
        layers.Dropout(0.5),
        layers.Dense(1, activation = "sigmoid", name = "output")])

    model.compile(loss = "binary_crossentropy",
                  optimizer = SGD(learning_rate = 0.001),
                  metrics = "accuracy")
    
    print("---------------------------------------------------")
    print(f"Addestramento per il fold numero {fold_number} ...")
    
    history = model.fit(x = inputs[train],
                        y = targets[train],
                        validation_data = (inputs[test], targets[test]),
                        verbose = 2,
                        shuffle = True,
                        epochs = 100,
                        batch_size = 32)
    
    metrics = model.evaluate(inputs[test], 
                             targets[test], 
                             verbose = 0)
    
    print(f"Loss relativa al fold numero {fold_number}: {model.metrics_names[0]} of {metrics[0]}")
    print(f"Accuratezza relativa al fold numero {fold_number}: {model.metrics_names[1]} of {metrics[1]*100}%")
    
    loss_per_fold.append(metrics[0])
    accuracy_per_fold.append(metrics[1]*100)
    
    fold_number += 1

print("----------------------------------------------------------------------------")
print("Metriche per fold:")

for i in range(0, len(accuracy_per_fold)):
    print(f"> Fold {i+1} - Loss: {loss_per_fold[i]} - Accuracy: {accuracy_per_fold[i]}%")

print("----------------------------------------------------------------------------")
print("Metriche medie:")

print(f"> Accuracy: {np.mean(accuracy_per_fold)} (+- {np.std(accuracy_per_fold)})")
print(f"> Loss: {np.mean(loss_per_fold)}")
print("----------------------------------------------------------------------------")

test_metrics = model.evaluate(X_test, 
                              y_test, 
                              verbose = 0)
    
print(f"Loss: {model.metrics_names[0]} of {metrics[0]}")
print(f"Accuratezza: {model.metrics_names[1]} of {metrics[1]*100}%")

risk_prediction = model.predict(x = X_test)
low_risk = 0
high_risk = 0

for i, prediction in enumerate(risk_prediction):
    if prediction < 0.50:
        print("Alert %d = low risk (%.4f)" %(i+1, prediction))
        low_risk += 1
    else:
        print("Alert %d = high risk (%.4f)" %(i+1, prediction))
        high_risk += 1
        
print("il numero di alert classificati a basso rischio è:", low_risk)
print("il numero di alert classificati ad alto rischio è:", high_risk)

model.save("risk_classifier")