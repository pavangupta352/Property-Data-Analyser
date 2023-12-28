import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class PropertyDataAnalyser:
    def __init__(self, file_path):
        self.dataframe = self.extract_property_info(file_path)

    def extract_property_info(self, file_path):
        df = pd.read_csv(file_path)
        return df

    def currency_exchange(self, exchange_rate):
        transformed_prices = self.dataframe['price'].apply(
            lambda x: x * exchange_rate)
        return np.array(transformed_prices)

    def suburb_summary(self, suburb):
        if suburb == 'all':
            summary = self.dataframe.describe()
        elif suburb in self.dataframe['suburb'].unique():
            summary = self.dataframe[self.dataframe['suburb']
                                     == suburb].describe()
        else:
            print("Error: Suburb does not exist in the dataframe.")
            return
        print(summary)

    def avg_land_size(self, suburb):
        if suburb == 'all':
            avg_land_size = self.dataframe['land_size'].mean()
        elif suburb in self.dataframe['suburb'].unique():
            avg_land_size = self.dataframe[self.dataframe['suburb']
                                           == suburb]['land_size'].mean()
        else:
            print("Error: Suburb does not exist in the dataframe.")
            return None
        return avg_land_size

    def prop_val_distribution(self, suburb, target_currency='AUD'):
        currency_dict = {"AUD": 1, "USD": 0.66, "INR": 54.25, "CNY": 4.72, "JPY": 93.87,
                         "HKD": 5.12, "KRW": 860.92, "GBP": 0.51, "EUR": 0.60, "SGD": 0.88}

        if target_currency not in currency_dict:
            print("Error: Target currency does not exist in the currency dictionary.")
            target_currency = 'AUD'

        exchange_rate = currency_dict[target_currency]

        if suburb == 'all':
            property_values = self.dataframe['price'] * exchange_rate
        elif suburb in self.dataframe['suburb'].unique():
            property_values = self.dataframe[self.dataframe['suburb']
                                             == suburb]['price'] * exchange_rate
        else:
            print("Error: Suburb does not exist in the dataframe.")
            property_values = self.dataframe['price'] * exchange_rate

        plt.hist(property_values.dropna(), bins=30)
        plt.xlabel('Property Value (' + target_currency + ')')
        plt.ylabel('Frequency')
        plt.title('Property Value Distribution for ' + suburb)
        plt.savefig('property_value_distribution.png')

    def sales_trend(self):
        sales_per_year = self.dataframe.groupby(pd.to_datetime(
            self.dataframe['sold_date'], format='%d/%m/%Y').dt.year)['price'].count()
        plt.plot(sales_per_year.index, sales_per_year.values)
        plt.xlabel('Year')
        plt.ylabel('Number of Properties Sold')
        plt.title('Sales Trend')
        plt.savefig('sales_trend.png')

    def locate_price(self, target_price, target_suburb):
        prices = self.dataframe[self.dataframe['suburb'] ==
                                target_suburb]['price'].sort_values(ascending=False)

        def binary_search(prices, target_price, low, high):
            if high >= low:
                mid = (high + low) // 2
                if prices.iloc[mid] == target_price:
                    return True
                elif prices.iloc[mid] > target_price:
                    return binary_search(prices, target_price, mid + 1, high)
                else:
                    return binary_search(prices, target_price, low, mid - 1)
            else:
                return False

        return binary_search(prices, target_price, 0, len(prices) - 1)


# Usage
analyser = PropertyDataAnalyser('property_information.csv')
analyser.suburb_summary('Clayton')
print(analyser.avg_land_size('Clayton'))
analyser.prop_val_distribution('Clayton', 'USD')
analyser.sales_trend()
print(analyser.locate_price(1000000, 'Clayton'))
