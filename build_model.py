
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score

import joblib 
import numpy as np 

from import_data import X, yc

# Load in mask to create a dataset using only the most informative columns
mask = np.load('mask.npy')
X = X.loc[:, mask]

default_clf =  DecisionTreeClassifier(random_state=0)
opt_clf = DecisionTreeClassifier(random_state=0,max_depth=4,max_leaf_nodes=24) # limited in size

X_train, X_test, y_train, y_test = train_test_split(X, yc, test_size=0.2, random_state=42) 

# Train the models
default_clf.fit(X_train,y_train)
opt_clf.fit(X_train,y_train)

# Predict on the test data
def_pred = default_clf.predict(X_test)
opt_pred = opt_clf.predict(X_test)

# Evaluate the model performance
default_pscore = round(precision_score(y_test, def_pred),3)
limited_pscore = round(precision_score(y_test, opt_pred),3)

print("Precision score (Large Tree Size):", default_pscore)
print("Precision score (Limited Tree Size):", limited_pscore)

# # Save the trained model
joblib.dump(opt_clf, 'tree_clf.pkl') 

from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

# Plot how the decision tree works
plt.figure(figsize=(20,10))
plot_tree(opt_clf)
plt.savefig('Tree_plot.png') 