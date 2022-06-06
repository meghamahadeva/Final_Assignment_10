from asyncio.windows_events import NULL

#declaration of UpdatedStock class.
#this class is used to store of all the stocks after I have called yahoo-finance api
#this has all the features of stock class along with extra parameter which are CurrentValue and CurrentDate which we get from API response
#along with it, this class also stores net profit or loss if we sold the share on most rescent closing price.
#data from this class is used to make output.csv file
class UpdatedStock():

    def __init__(self, StockSymbol, NoShares, PurchaseValue, PurchaseDate, CurrentValue, CurrentDate, Profit):
        self.StockSymbol = StockSymbol
        self.NoShares = NoShares
        self.PurchaseValue = PurchaseValue
        self.PurchaseDate = PurchaseDate
        self.CurrentValue = CurrentValue
        self.CurrentDate = CurrentDate
        self.Profit = Profit

    
    # function to print the UpdatedStock, it returns all the parameters of a UpdatedStock in form of a list
    def printstocks(self):
        row = [self.StockSymbol, self.NoShares, self.PurchaseValue, self.PurchaseDate, self.CurrentValue, self.CurrentDate, self.Profit]
        return row
    