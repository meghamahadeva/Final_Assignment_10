'''
Name:	                   Megha Mahadeva
Date: 	   				   06/5/2022
Course:                    Python Programming ICT – 4370

Description: This program focuses on calculating the earnings and loss of each share for Bob Smith. It will also show which share has made the most earning
             and which share has suffered the biggest loss till June 3rd 2022.Predefined purchase price and purchase date has been considered from Data_Stock.csv
             and using Yahoo Finance API to consider the latest selling price and date(June 3rd) for calculations. The try and error functions has been used to
             test a block of code for errors and the except to handle the error. This program will visualize the stock value as per the purchase dates.
'''

import csv
import json
import pandas as pd
import matplotlib.pyplot as plt
from Classes import stock
from DataClass import UpdatedStock
import time
import datetime

#call_api is a method created to call the external api which is yahoo-finance and fetch data from it.
#it requires 4 parameters which are the name of the stock, starting date for the stock, ending date of the stock and time interval between two reccords respectively
#this method converting the api response to data frame which is more suitable format for data traversal.
#if there is any error, the method returns an empty data frame.  
def call_api(token, period1, period2, interval):
    try:
        query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{token}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
        df = pd.read_csv(query_string)
        return df
    except:
        print("There was an error in api call")
        return pd.DataFrame()

#plot_graph is used to initalize all the parameters required for plotting the graph, I am using matplotlib.pyplot for this purpose
#time period is on the x-axis and price of stock on y-axis.
def plot_graph(rows):
    company_name = []
    for CompanyName in rows:
        if CompanyName[0] not in company_name:
            company_name.append(CompanyName[0])

    company_dict = {}
    dates_dict = {}
    for CompanyName in company_name:
        earnings = []
        dates = []
        for data in rows:
            if CompanyName == data[0]:
                earnings.append(data[1])
                dates.append(data[2])
        company_dict[CompanyName] = earnings
        dates_dict[CompanyName] = dates
    df_company = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in company_dict.items()]))
    df_dates = pd.DataFrame(dict([("Dates", dates_dict[company_name[0]])]))
    df = pd.concat([df_company, df_dates], axis=1)
    df.plot.line(x='Dates')


# Here I am reading input from a csv file present in same directory as that of main.py file
file_name = r".\Data_Stocks.csv"
j=0 
# This variable is a list used to store memory address for stock objects
collection_of_stocks = []
# This variable is a list used to store memory address for UpdatedStock objects
collection_of_results = []
# Following block is used to take input from csv file and store in stock objects, which is further stored in collection_of_stocks list for later referrene
try:
    with open(file_name) as input_file:
        list_of_lists = input_file.readlines()
        for i in list_of_lists[1:]:
            x = i.split()[0].split(',')
            collection_of_stocks.append(stock(x[0], float(x[1]), float(x[2]), x[3]))
except FileNotFoundError as fnf_error:
    print(f"The {file_name} file does not exists!!!")

# Here we are creating variables for date time to be passed in yahoo-finance api
# We are using 4 days gap between dates assuming stock market is never closed for 4 consecutive dates, as the api returns data for only those dates when the market is open
today = datetime.datetime.today().timetuple()
today = int(time.mktime(today))
four_days_ago = (datetime.datetime.today() - datetime.timedelta(days=4)).timetuple()
four_days_ago = int(time.mktime(four_days_ago))
interval = '1d'
# We are calling call_api() method and storing results in UpdatedStock object which is further stored in collection_of_results list
for stok in collection_of_stocks:
    rows = []
    rows = stok.printstocks()
    df = call_api(rows[0], four_days_ago, today, interval)
    n = df['Date'].count()
    rows.append(df['Close'][n-1])
    rows.append(df['Date'][n-1])
    sum = round(rows[1] * (rows[4] - rows[2]), 2)
    rows.append(sum)
    collection_of_results.append(UpdatedStock(rows[0], rows[1], rows[2], rows[3], rows[4], rows[5], rows[6]))
# We are traversing collection_of_results list to fetch data from objects and storing them into csv file
data_of_csv = []
for stok in collection_of_results:
    data_of_csv.append(stok.printstocks())
fields = ['SYMBOL', 'NO_SHARES', 'PURCHASE_PRICE', 'PURCHASE_DATE', 'SELLING_PRICE', 'SELLING_DATE', 'PROFIT'] 
with open('output.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(data_of_csv)

# Here we are again calling the api to get data from all the dates from purchase date to current date. Then we store this data into a list and plot the graph for it.
data_for_graph = []
for stok in collection_of_results:
    from_date = str(stok.PurchaseDate).split("/")
    to_date = str(stok.CurrentDate).split("-")
    period1 = int(time.mktime(datetime.datetime(int(from_date[2]), int(from_date[0]), int(from_date[1]), 23, 59).timetuple()))
    period2 = int(time.mktime(datetime.datetime(int(to_date[0]), int(to_date[1]), int(to_date[2]), 23, 59).timetuple()))
    interval = '1d'
    df = call_api(stok.StockSymbol, period1, period2, interval)
    n = df['Date'].count()
    for i in range(n):
        data = []
        data.append(stok.StockSymbol)
        data.append(df['Close'][i])
        data.append(df['Date'][i])
        data_for_graph.append(data)
plot_graph(data_for_graph)
plt.savefig('simplePlot.png')
plt.show()
