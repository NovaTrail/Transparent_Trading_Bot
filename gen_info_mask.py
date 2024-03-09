#gen_info_mask.py
from sklearn.feature_selection import mutual_info_classif

import numpy as np
from import_data import X, yc

s = mutual_info_classif(X,yc)
mask = np.where(s > np.percentile(s,75), 1, 0).astype(bool) # 75th percentile 

np.save('mask.npy', mask)
loaded_mask = np.load('mask.npy')



