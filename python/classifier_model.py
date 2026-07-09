from sklearn.tree import DecisionTreeClassifier, plot_tree # Decision tree access
from sklearn.model_selection import KFold, cross_val_score # Evaluating model
from sklearn.metrics import confusion_matrix 
import matplotlib.pyplot as plt # Visualizing tree
import pandas # Simplify data analysis
import numpy as np
import m2cgen as m2c # Convert model to C code

# Load data
dataset = pandas.read_csv('/Users/vivianacebrero/Documents/UCI/Research/SoundClassifier/python/complete_feature_data.csv')

X = dataset.drop(columns=['label'])
y = dataset['label']

# Create model
model = DecisionTreeClassifier(
    criterion='entropy',
    max_depth=10,
    random_state=42
)

# Train model
kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kf, scoring='accuracy')

# Show results
print(f"\nScores per fold: {scores}")
print(f"Mean Accuracy: {np.mean(scores):.4f}")

# Gather fold results
y_true = []
y_pred = []

for train_idx, test_idx in kf.split(X): # split data into folds
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx] # locate actual data using row indices
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx] # locate labels of split data
    
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    y_true.extend(y_test)  # save the true values and predictions from this fold
    y_pred.extend(preds)

# Compute confusion matrix for the dataset
cm = confusion_matrix(y_true, y_pred)

classes = np.unique(y_true)

# Calculate class' accuracy
class_accuracy = cm.diagonal() / cm.sum(axis=1)

print("\nConfusion Matrix:")
print(cm)
print("\nClass Performance Summary:")

for label, accuracy in zip(classes, class_accuracy):
    print(f"'{label}' Accuracy: {accuracy:.4%}")

# Create and save tree plot
#model.fit(X, y)
#plt.figure(figsize=(16,10))

#plot_tree(
    #model,
    #feature_names=X.columns,
    #class_names=sorted(y.unique()),
    #filled=True,
    #rounded=True
#)

#plt.savefig('my_plot50.pdf', format='pdf', bbox_inches='tight')

# Convert decision tree model into C code and save the file
model.fit(X, y)

code = m2c.export_to_c(model, function_name="classify_audio")

with open("/Users/vivianacebrero/Documents/UCI/Research/SoundClassifier/Core/Src/classifier_tree.c", "w") as f:
    f.write(code)