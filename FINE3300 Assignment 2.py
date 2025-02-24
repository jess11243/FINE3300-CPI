"""
Assignment 2: Consumer Price Index
Course: FINE3300 
Name: Jessica L. Draper
Date: 02/23/25

Purpose: Form a Dataframe using data files from Statistic Canada's monthly recorded CPI levels in 2024
"""

import pandas as pd
import numpy as np

# -- Q1: Combining all dataframes ---------------------------------------------

# listing jurisdictions (also sorted in this order)
jurisdictions = ['Canada', 'MB', 'NB', 'NL', 'NS', 'ON', 'PEI', 'QC', 'SK', 'AB', 'BC']

"""
For Reference:

MB - Manitoba
NB - New Brunswick
NL - Newfoundland and Labrador
NS - Nova Scotia
ON - Ontario
PEI - Prince Edward Island
QC - Quebec
SK - Saskatchewan
AB - Alberta
BC - British Columbia

"""
dataframes = []

# reading each file
for jurisdiction in jurisdictions:
    df = pd.read_csv(f"{jurisdiction}.CPI.1810000401.csv")
    
    df_melted = pd.melt(df, id_vars=['Item'], var_name='Month', value_name='CPI') # convert months from columns to rows
    df_melted['Jurisdiction'] = jurisdiction
    
    dataframes.append(df_melted)

# .concat, to combine all the data
cpi_data = pd.concat(dataframes, ignore_index=True)

# converting and applying new month format.
def month_format(month):
    parts = month.split('-')  # '24-Jan' turns into ['24', 'Jan']
    return (parts[1] + '-' + parts[0])  # string is now 'Jan-24'

cpi_data['Month'] = cpi_data['Month'].apply(month_format)

# reordering columns
cpi_data = cpi_data[['Item', 'Month', 'Jurisdiction', 'CPI']]


# -- Q2: First 12 lines in df ---------------------------------------------------

print("2: ")
print(cpi_data.head(12))
print("\n")

# -- Q3: avg month-to-month changes ---------------------------------------------------

def calculate_monthly_changes(df, items):
    results = []

    month_order = ['Jan-24', 'Feb-24', 'Mar-24', 'Apr-24', 'May-24', 'Jun-24', 
                   'Jul-24', 'Aug-24', 'Sep-24', 'Oct-24', 'Nov-24', 'Dec-24']
    

    # for each jurisdiction
    for jurisdiction in df['Jurisdiction'].unique():
        # storing data for each jurisdiction
        jurisdiction_data = []
        
        # loop through each category (food, shelter, etc)
        for item in items:
            # we get the data for the certain jurisdiction and category
            data = df[(df['Jurisdiction'] == jurisdiction) & (df['Item'] == item)]
            data = data.set_index('Month').reindex(month_order).reset_index()
            
            # calculate month-to-month percentage in CPI
            pct_changes = data['CPI'].pct_change() * 100
            avg_change = pct_changes.mean()
            
            # add to jurisdiction_data
            jurisdiction_data.append((item, round(avg_change, 1)))
        
        # then add to results
        results.append((jurisdiction, jurisdiction_data))
    
    return results

# checking food and shelter categories, then calculating the month-to-month changes. 
items_to_analyze = ['Food', 'Shelter', 'All-items excluding food and energy']
monthly_changes = calculate_monthly_changes(cpi_data, items_to_analyze)

# printing results
print("\n3: Average month-to-month changes (%):")
for jurisdiction, changes in monthly_changes:
    print("\n" + jurisdiction + ":") 
    
    for item, change in changes:
        print(item + ": " + str(change) + "%")


# -- Q4: Highest average changes ---------------------------------------------------


print("\n4: Highest average changes by category:")

# for each category
for item in items_to_analyze:
    # temp max variables
    max_jurisdiction = None
    max_change_value = float('-inf')

    # for each juisdiction and its changes
    for jurisdiction, changes in monthly_changes:
        for category, change in changes:
            # check if the category is the same
            if category == item:
                # update if a new maximum is found
                if change > max_change_value:
                    max_change_value = change
                    max_jurisdiction = jurisdiction
                break  # stop inner loop

    print("The highest avg CPI change for " + item + ": located in " + str(max_jurisdiction) + " at (" + str(max_change_value) + "%)")

# -- Q5: Annual change in services ---------------------------------------------------

def calculate_annual_change(df):
    results = []

    # for each jurisdiction
    for jurisdiction in df['Jurisdiction'].unique():
        # Get services data for jurisdiction
        services_data = df[(df['Jurisdiction'] == jurisdiction) & (df['Item'] == 'Services')]
        
        # find jan value and dec value and then difference of the two
        jan_value = services_data[services_data['Month'] == 'Jan-24']['CPI'].iloc[0]
        dec_value = services_data[services_data['Month'] == 'Dec-24']['CPI'].iloc[0]
        annual_change = ((dec_value - jan_value) / jan_value * 100).round(1)
        
        # add to results
        results.append((jurisdiction, annual_change))
    return results

# calling the function
services_changes = calculate_annual_change(cpi_data)

print("\n5: Annual CPI change in services (%):")
for jurisdiction, change in services_changes:
    print(jurisdiction + ": " + str(change) + "%")


# -- Q6: Region with highest services inflation ---------------------------------------------------

max_services_change = services_changes[0]  # setting initial maximum

# finding max in services_changes
for entry in services_changes:
    jurisdiction, inflation = entry
    if inflation > max_services_change[1]: # if new max is found, update max
        max_services_change = entry

region, highest_inflation = max_services_change

print("\n6: Region with the highest services inflation:")
print(region + " (" + str(highest_inflation) + "%)")