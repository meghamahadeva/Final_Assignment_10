
from datetime import datetime

#declaring the stock class
#this class is used to fetch data from csv file and store data for further use
class stock():

    def __init__(self, StockSymbol, NoShares, ClosingValue, PurchaseDate):
        self.StockSymbol = StockSymbol
        self.NoShares = NoShares
        self.ClosingValue = ClosingValue
        self.PurchaseDate = PurchaseDate

    # function calculate the earnings(multiplying the closing price with number of shares)
    def CalculateEarning(self):
        return round((self.ClosingValue) * self.NoShares, 2)

    # function to print the stocks, it returns all the parameters of a stock in form of a list
    def printstocks(self):
        row = [self.StockSymbol, self.NoShares, self.ClosingValue, self.PurchaseDate]
        return row