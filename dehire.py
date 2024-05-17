# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 08:47:43 2023

@author: hp
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

dehire = pd.read_excel(r"C:/Users/hp/Downloads/Dataset dehire Original.xlsx")
dehire.info()
dehire.columns

###DATA CLENSING

###checking the duplicates 
duplicate = dehire.duplicated()
dehire.drop_duplicates()

sum(duplicate)

###Type function
dehire['From WhsCode'] = dehire['From WhsCode'].astype(str)
dehire['To whsCode'] = dehire['To whsCode'].astype(str)

###Identify missing values
dehire.isnull().sum()

####Removing unwanted columns 

dehire = dehire.drop(['Quarantine Item COde', 'Loading/Unloading', 'Customer Type', 'DOCNUM', 'Detention', 'Business Heads', 'EFFECTIVE DATE', 'CREATE DATE', 'TRANSPORTER NAME', 'Vehicle Type'], axis =1)

dehire.describe()


########EXPLORATORY DATA ANALYTICS

# to find the price for each order = raqt = rate * quantity 
dehire['raqt'] = dehire ['RATE'] * dehire ['QUANTITY']

####Measures of Central tendency

dehire.raqt.mean()
dehire.QUANTITY.median()

from sklearn.impute import SimpleImputer
mode_imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
dehire["City"] = pd.DataFrame(mode_imputer.fit_transform(dehire[["City"]]))
dehire["STATE"] = pd.DataFrame(mode_imputer.fit_transform(dehire[["STATE"]]))

dehire.City.value_counts()
dehire.STATE.value_counts() ###Maharastra has highest count 

####Measures of dispersion

dehire.raqt.var()    ####The quantity of dehired pallets returns is very high
dehire.raqt.std()
  
###Third moment business decision

dehire.raqt.skew()  ###hence the 

####Fourth moment business decision

dehire.raqt.kurt()

###checking the corelation

plt.figure(figsize=(20,10))
sns.heatmap(dehire.corr(),cbar=True,annot=True,cmap='Blues')  
dehire['QUANTITY']=abs(dehire['QUANTITY']) #### Corelation is positive to customervendor code, u-frt, quantity, rate

###count plot

dehire['LOB'].value_counts().plot(kind='bar',title='LOB' , figsize = (10,5))
dehire['QUANTITY'].value_counts().plot(kind='bar',title='LOB' , figsize = (10,5))
dehire['Region'].value_counts().plot(kind='bar',title='Region of sales' , figsize = (10,5))


from pandas_profiling import ProfileReport

ProfileReport(dehire)

###AutoEDA libraries

import sweetviz as sv

s = sv.analyze(dehire)
s.show_html()

import os
os.getcwd()
