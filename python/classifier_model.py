from sklearn.tree import DecisionTreeClassifier, plot_tree # Decision tree access
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt # Visualizing tree
import pandas # Simplify data analysis

# Load data
dataset = pandas.read_csv('/Users/vivianacebrero/Documents/UCI/Research/SoundClassifier/python/complete_feature_data.csv')

X = dataset.drop(columns=['label'])
y = dataset['label']

# Split data into training and testing sets into equal parts based on labels
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=5, stratify=y
)

# Create model
model = DecisionTreeClassifier(
    criterion='entropy',
    max_depth=4,
    random_state=5
)

# Train model
model.fit(X_train, y_train)

# Show results
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Compute confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Divide correct predictions (diagonal) by total true items per class (row sum)
per_class_accuracy = cm.diagonal() / cm.sum(axis=1)

# Pair with class labels for readability
classes = y.unique()
for cls, acc in zip(classes, per_class_accuracy):
    print(f"Class '{cls}' Accuracy: {acc:.2%}")

"""
# Visualize the trained tree structure
plt.figure(figsize=(12, 8))
plot_tree(
    model, 
    feature_names=X.columns.tolist(), 
    class_names=y.unique(), 
    filled=True, 
    rounded=True
)
plt.show()"""