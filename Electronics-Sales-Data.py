import pandas as pd
import os
import matplotlib.pyplot as plt

desired_width = 320
pd.set_option('display.width', desired_width,
              'display.max_columns', 10)

###: Clean data
all_data = pd.read_csv("all_data.csv")
nan_df = all_data[all_data.isna().any(axis=1)]
all_data = all_data.dropna(how='all')
all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']

###: Add Month column
all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int64')

###: Convert string into interger & Add Sales column
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])
all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']

###: Add City column - using Lambda in Python
def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")

###: Create all_data.csv file contains all datas from other csv files
files = [file for file in os.listdir(
    'D:\Pandas-Data-Science-Tasks-master\SalesAnalysis\Sales_Data')]

all_months_data = pd.DataFrame()

for file in files:
    df = pd.read_csv("D:/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/" + file)
    all_months_data = pd.concat([all_months_data, df])

all_months_data.to_csv('D:/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/all_data.csv',
    index=False)

###: Question 1: What was the best month for sales? How much was earned that month?
results = all_data.groupby('Month').sum()

###: Visualizing the results
months = range(1,13)
plt.figure(figsize=(12,6))
plt.bar(months, results['Sales'])
plt.ticklabel_format(useOffset=False, style='plain')
plt.xticks(months)
plt.title('Sales in every months')
plt.ylabel('Sales in USD($)')
plt.xlabel('Month number')

##: Answer = December with Revenue at around $4,613,443

###: Question 2: What city has the highest number of Sales?
results = all_data.groupby('City').sum()

###: Visualizing the results
cities = [i for i, df in all_data.groupby('City')]
plt.figure(figsize=(18,8))
plt.bar(cities, results['Sales'])
plt.ticklabel_format(style='plain', axis='y')
plt.xticks(cities)
plt.title('Sales in every Cities')
plt.ylabel('Sales in USD($)')
plt.xlabel('Name of Cities')

###: Question 3: What time should we display advertisements to maximize likelihood of customer's buying product?
all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
all_data['Hour'] = all_data['Order Date'].dt.hour

hours = [hour for hour, df in all_data.groupby('Hour')]

plt.plot(hours, all_data.groupby('Hour').count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of Orders')
plt.grid()
plt.show()
### Answer: Recommendation from 11 A.M to 7 P.M

###: Question 4: What products are most often sold together?
df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df = df[['Order ID', 'Grouped']].drop_duplicates()

from itertools import combinations
from collections import Counter

count = Counter()

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

for key,value in count.most_common(10):
    print(key,value)
