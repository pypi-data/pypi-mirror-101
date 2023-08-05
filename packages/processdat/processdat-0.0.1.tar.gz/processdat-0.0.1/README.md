# **Data Preprocessing Module**

### *This python module preprocesses a csv dataset, which has a categorical data at the last column. This module makes use of scikit-learn, pandas and numpy.*

The following steps of preprocessing be done in order: 
1. Importing Dataset
1. Missing Value treatement
1. Encoding Categorical Data
1. Splitting Dataset into training and testing set
1. Feature Scaling using Standard Scaler

****
## Inut and output

- The input value to the sole function preprocess is a csv dataset

- The return value is a tuple of 4 values in the fashing of train_test_split of scikit-learn, i.e X_train, X_test, y_train, y_test** 

****
## Module Installation from PyPI

```bash
$ pip install processdat
```
****

## Usage

```python
> import processdat as pro

...
X_train, X_test, y_train, y_test = pro.preprocess('Data.csv')
...

```
****
## Developing *processdat*

To install *processdat*, along with the tools you need to develop and run tests, run the following in the terminal/environment:

```bash
$ pip install -e .[dev]
```
****

### Created by: Shayan Banerjee (shayanbanerhee96@gmail.com)