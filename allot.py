# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 14:57:13 2023

@author: hp
"""

###Data Pre-processing
 
import pandas as pd
import seaborn as sns
import numpy as np

allot = pd.read_excel(r"C:/Users/hp/Downloads/Dataset Allot.xlsx")
allot.info()
allot.columns

###Data Clensing

###checking the duplicates 

# Parameters
duplicate = allot.duplicated(keep = 'last')
duplicate

duplicate = allot.duplicated(keep = False)
duplicate

##Removing the duplicates
duplicate = allot.duplicated()
allot.drop_duplicates()

sum(duplicate)



###checking nan values
allot.isna().sum()

###Removing unwanted columns 

allot = allot.drop(['NumAtCard', 'U_GRNNO', 'Loading/Unloading', 'KITITEM', 'U_SOTYPE', 'SO Due Date', 'SO Creation Date', 'SO ID', 'Customer Type'], axis = 1)

#To find all unique words in a column
allot['Transfer Type'].unique()
allot['Document Type'].unique()

###Typecasting
allot['TRANSPORTER NAME'] = allot['TRANSPORTER NAME'].astype(str)

# Detection of outliers (find limits for salary based on IQR)
IQR = allot['RATE'].quantile(0.75) - allot['RATE'].quantile(0.25)

lower_limit = allot['RATE'].quantile(0.25) - (IQR * 1.5)
upper_limit = allot['RATE'].quantile(0.75) + (IQR * 1.5)

##Boxplot 
sns.boxplot(allot.RATE)

###Hence outliers are present 
. Remove (let's trim the dataset) ################
# Trimming Technique
# Let's flag the outliers in the data set
import numpy as np
import seaborn as sns

outliers_df = np.where(allot['RATE'] > upper_limit, True, np.where(allot['RATE'] < lower_limit, True, False))
df_trim = allot.loc[~(outliers_df),]
allot.shape, df_trim.shape

 ##Hence check the outliers
sns.boxplot(df_trim.RATE)    ###hence the whisker plot is not symmetrical and tail is towards left side

############### 2. Replace ###############
# Replace the outliers by the maximum and minimum limit
allot['Rate_replaced'] = pd.DataFrame(np.where(allot['RATE'] > upper_limit, upper_limit, np.where(allot['RATE'] < lower_limit, lower_limit, allot['RATE'])))
sns.boxplot(allot.Rate_replaced)

################## Missing Values - Imputation ###########################

# Check for count of NA's in each column
allot.isna().sum()
from sklearn.impute import SimpleImputer

# Median Imputer
median_imputer = SimpleImputer(missing_values=np.nan, strategy='median')
allot["RATE"] = pd.DataFrame(median_imputer.fit_transform(allot[["RATE"]]))

# Mode Imputer
mode_imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
allot["TO WhsName"] = pd.DataFrame(mode_imputer.fit_transform(allot[["TO WhsName"]]))
allot["UNIT"] = pd.DataFrame(mode_imputer.fit_transform(allot[["UNIT"]]))
allot["TRANSPORTER NAME"] = pd.DataFrame(mode_imputer.fit_transform(allot[["TRANSPORTER NAME"]]))
allot["Vehicle Type"] = pd.DataFrame(mode_imputer.fit_transform(allot[["Vehicle Type"]]))
allot.isnull().sum()  # all Sex, MaritalDesc records replaced by mode

# EDA

# to find the price for each order = raqt = rate * quantity 
allot['raqt'] = allot ['RATE'] * allot ['QUANTITY']


# First moment of business decision

allot.raqt.mean()
allot.raqt.median()
allot.raqt.mode()
from scipy import stats
stats.mode(allot.raqt)

###second moment business decision

allot.raqt.var()
allot.raqt.std()
range = max(allot.raqt)-min(allot.raqt)
range

####Third moment business decision
allot.raqt.skew()

####Fourth moment business decision
allot.raqt.kurt()

# bar plot, histogram, boxplot

data1.raqt.describe()

import matplotlib.pyplot as plt 
plt.hist(allot.raqt) #histogram


sns.boxplot(allot.raqt)
plt.boxplot(allot.raqt)

##Imputation 
median_imputer = SimpleImputer(missing_values=np.nan, strategy='median')
allot["raqt"] = pd.DataFrame(median_imputer.fit_transform(allot[["raqt"]]))
 allot.isna().sum()

allot.to_csv('EDA with Allot.csv', encoding = 'utf-8')
import os
os.getcwd()

#############AUTO EDA

import sweetviz as sv
s = sv.analyze(allot)
s.show_html()
