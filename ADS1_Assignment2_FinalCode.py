# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 10:16:28 2023

@author: kvyja
"""

import pandas as pd  #Inputing file, Data-processing
import matplotlib.pyplot as plt  #creating visualizations
import seaborn as sns #statistical data visualization

def filter_and_process_data(filename, indicator_name, countries):
    # Filter the dataframe based on indicator name and countries
    
    #Read a CSV file into a DataFrame, skipping the first 4 rows
    df=pd.read_csv(filename, skiprows=4) 
    
    data = df[(df["Indicator Name"] == indicator_name) 
              & (df["Country Name"].isin(countries))]

    #Keeping the necessary columns('Country Name', and years from 2012 to 2020)
    columns_to_keep = ['Country Name', '2012', '2013', '2014', '2015', '2016', 
                       '2017', '2018', '2019', '2020']
    data = data.filter(columns_to_keep).reset_index(drop=True)

    # Transpose the dataframe
    data_t = data.T
    data_t.columns = data_t.iloc[0]
    data_t = data_t.iloc[1:]

    # Set index to numeric and add a 'Years' column
    data_t.index = pd.to_numeric(data_t.index)
    data_t['Years'] = data_t.index
    data_t = data_t.reset_index(drop=True)
    
    return data, data_t


def lineplot(line_plot_data, title):
    '''Define a function named 'lineplot' to create a line plot 
    using specified data and title.'''
   
    plt.figure()
    line_plot_data.plot(x='Years', y=["Algeria", "Nepal", "Brazil", "India", 
                                      "Spain"], 
                        kind='line', figsize=(10, 5), marker='o')
    
    #Set title, x-axis label, y-axis label, and display legend
    plt.title(title)
    plt.xlabel('Years')
    plt.ylabel('net inflows (% of GDP)')
    plt.legend(loc='best', bbox_to_anchor=(1, 0.4))
    plt.savefig('lineplot.png') # Saving the plot
    plt.show() 
    
def barplot(df, x_value, y_values, head_title, x_label, y_label, 
            colors, figsize=(10, 6)):  
    '''Defining the function to create the barplot using specified DataFrame 
    and customization parameters.'''
    
    sns.set_style('whitegrid')
    
    df_filtered = df[df['Years'].isin([2012, 2014, 2016, 2018, 2020])]
    
    # Create a bar plot using the filtered DataFrame and specified parameters.
    df_filtered.plot(x=x_value, y=y_values, kind='bar', title=head_title, 
                     color=colors,width=0.65, figsize=figsize, 
                     xlabel=x_label, ylabel=y_label)
    plt.legend(loc='best', bbox_to_anchor=(1, 0.4))
    plt.savefig('barplot.png') # Saving the plot
    plt.show()
    
    
def boxplot(data, countries, xlabel='Country', ylabel='Value', 
                        title='Boxplot for Selected Countries', 
                        figsize=(10, 6)):
    
    sns.set(style="whitegrid")   
    plt.figure(figsize=figsize)

    # Convert the data dictionary to a Pandas DataFrame
    df = pd.DataFrame({country: data[country] for country in countries})

    # Create box plot with seaborn
    sns.boxplot(data=df, width=0.5, palette='Set3')

    # Customize labels and title
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14)

    # Set individual labels for each box
    plt.xticks(ticks=range(len(countries)), labels=countries)
    plt.savefig('boxplot.png') # Saving the plot

    plt.show()
    

def pieplot(df, year, autopct='%1.0f%%', fontsize=11):
    '''Define a function named 'pieplot' to create a pie chart representing 
    population distribution for specific countries in a given year.'''
    
    labels = ['Algeria', 'Brazil', 'Spain', 'India', 'Nepal']
    
    # Define a color palette for the pie chart
    colors = sns.color_palette("Set2")

    plt.figure(figsize=(5, 6))
    
    #Generate a pie chart using plt.pie with specified parameters
    plt.pie(df[str(year)], autopct=autopct, labels=labels,
            colors=colors, wedgeprops={"edgecolor": "black", 
                                       "linewidth": 2, "antialiased": True})

    plt.title(f'Population growth (annual %) in {year}', fontsize=fontsize)
    plt.savefig('pieplot.png') # Saving the plot
    plt.show()
    
def slicing_and_rename(df, column_name):
    '''Define a function named 'slicing_and_rename' to extract 
    specific columns and rename one of them.'''

    return df[['Country Name', '2012']].rename(columns={'2012': column_name})


def merging(*dataframes):
    '''Define a function named 'merging' to merge multiple DataFrames 
    on the 'Country Name' column.'''
    
    # Merge multiple DataFrames on the 'Country Name' column using pd.concat
    merged_df = pd.concat(dataframes, axis=1, join='outer', ignore_index=True)
    merged_df.columns = merged_df.iloc[0]  # Set columns to the first row
    merged_df = merged_df.drop(0)  # Drop the duplicated header row
    
    # Reset the index and drop the old index column.
    merged_df = merged_df.reset_index(drop=True)
    return merged_df


def correlation_heatmap(data, title, figsize=(6, 5)):
    '''Define a function named 'create_correlation_heatmap' to generate a 
    heatmap representing the correlation matrix of numerical data.'''
    
    plt.figure(figsize=figsize)
    numeric_df = data.select_dtypes(include='number')
    # Calculate the correlation matrix
    correlation_matrix = numeric_df.corr()
    # Create a heatmap using Seaborn
    sns.heatmap(correlation_matrix, annot=True, cmap='Purples', fmt='.2f',
                linewidths=.5) 
    plt.title(title)
    plt.savefig('correlation_heatmap.png') # Save the plot
    plt.show()
    
filename = "API_19_DS2_en_csv_v2_6224512.csv" #Defining filename for CSV file

# List of specific countries for data analysis.
Country = ["Algeria", "Nepal", "Brazil", "India", "Spain"]

# Process and filter data for multiple indicators across specific countries.
data1, data1_t = filter_and_process_data(
    filename, "Population growth (annual %)", Country)
data2, data2_t = filter_and_process_data(
    filename, "CO2 emissions (kg per PPP $ of GDP)", Country)
data3, data3_t = filter_and_process_data(
    filename, "Cereal yield (kg per hectare)", Country)
data4, data4_t = filter_and_process_data(
    filename, "Foreign direct investment, net inflows (% of GDP)", Country)

data1_t.describe() # Generate and display descriptive statistics 

'''Visualising the lineplot'''
lineplot(data4_t, "Foreign direct investment, net inflows (% of GDP)")

'''Visualising the barplot'''
barplot(data2_t, 'Years', ['Algeria', 'Nepal', 'Brazil', 'India', 'Spain'],
               'Comparison of CO2 Emissions per PPP $ of GDP', 'Years', 
               'kg per PPP $ of GDP', ('skyblue', 'limegreen', 'lightcoral', 
                                       'gold', 'mediumorchid'))

'''Visualising the boxplot'''
boxplot(data3_t, ["Algeria", "Brazil", "India", "Nepal", "Spain"],
                xlabel='Country', ylabel='(kg per hectare)',
                title='Cereal Yield Boxplot(kg per hectare)')

'''Visualising the pieplot'''
pieplot(data1, '2020')

'''Extract and rename specific columns for correlation analysis 
from datasets 'data1', 'data2', 'data3', and 'data4'.'''
data1_cor = slicing_and_rename(data1, 'Population Growth')
data2_cor = slicing_and_rename(data2, 'CO2 Emission')
data3_cor = slicing_and_rename(data3, 'Cereal Yield')
data4_cor = slicing_and_rename(data4, 'Foreign Direct Investment')

# Merge the sliced and renamed datasets into a single DataFrame 'merged_data'.
merged_data = merging(data1_cor, data2_cor, data3_cor, data4_cor)

'''Visualising the correlation heatmap'''
correlation_heatmap(merged_data, 'Correlation Heatmap')

