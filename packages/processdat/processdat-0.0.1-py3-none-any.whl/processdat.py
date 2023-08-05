# All the imports
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

def preprocess(data):
	# Importing the dataset
	df = pd.read_csv(data)
	# features
	X = df.iloc[:, :-1].values
	# (dependent) labels, assuming last col is target
	y = df.iloc[:, -1].values

	# taking care missing value
	# replace missing values by average of the column
	imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
	# get only numerical columns
	numerics = ['int64', 'int32', 'int16', 'float16', 'float32', 'float64']
	numerics_labels = df.select_dtypes(include=numerics).columns
	numerics_index = []
	for numerics_label in numerics_labels: 
		numerics_index.append(df.columns.get_loc(numerics_label))
		pd.to_numeric(df.columns.get_loc(numerics_label))
	# fit the data
	imputer.fit(X[:, numerics_index])
	# apply transform, ie actually replace the values
	# this updates the columns and returns
	# so let us update them in the original df too
	X[:, numerics_index] = imputer.transform(X[:, numerics_index])

	# Encoding categorical data
	# these can be important in our model, so we convert
	# the strings to numerical categories so that
	# we can derieve meaningful objectives
	# we cannot turn them to numbers as it will have some precedence, hence Hot Encoding is important

	# First getting categorical columns of only features
	X_df = pd.DataFrame(X)
	X_df[numerics_index] = X_df[numerics_index].apply(pd.to_numeric)
	categorical_labels_index = list(X_df.select_dtypes(include=['object']).columns)

	# Encoding the independent variable
	ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), categorical_labels_index)], remainder='passthrough')
	# Now france is 1, 0, 0, Germany: 0, 1, 0
	X = np.array(ct.fit_transform(X))
	#print(X)

	# Encode dependent variable, with label encoder
	le = LabelEncoder()
	y = le.fit_transform(y)
	# Yes and No converted to 1, 0
	#print(y)

	## New and updated numeric_index after encoding, it is shifted by n in right side
	## we can check for shifting if categorical index is on left and right 
	n =  X.shape[1] - (df.shape[1] - 1)
	new_numerics_index = []
	for index in numerics_index:
		if numerics_index[0] > categorical_labels_index[0]:
			index = index + n
		else:
			index = index - n
		new_numerics_index.append(index)

	# Splitting dataset to train, test then do feature scaling
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
	#print(X_train, y_train)

	#feature scaling
	sc = StandardScaler()
	# as dummy variable already in range, so leave them
	# if we do scaling on dummy var, we will get nonsense vals
	# so only numerical indexes, not objs or categoricals
	#print(X_train)
	X_train[:, new_numerics_index] = sc.fit_transform(X_train[:, new_numerics_index])
	X_test[:, new_numerics_index] = sc.transform(X_test[:, new_numerics_index])

	# return a tuple of values in fashoin of sklear
	return (X_train, X_test, y_train, y_test)