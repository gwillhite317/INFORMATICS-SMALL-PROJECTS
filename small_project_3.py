#plot one


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np




avocado_data = pd.read_csv("C:/Users/mowma/Downloads/avocado.csv")
#reding in csv as a dataframe with pandas
avocado_data['Date'] = pd.to_datetime(avocado_data['Date'], format='%m/%d/%y')
# format the date coloumn properly
filtered_avocado = avocado_data[avocado_data['Date'].dt.year.isin([2015, 2016, 2017])] 
#filter for years 2015, 2016, 2017
filtered_avocado['Year'] = filtered_avocado['Date'].dt.year
#create year coloumn
sales_for_year = filtered_avocado.groupby([filtered_avocado['Date'].dt.year, 'type'])['Number_Avocados_Sold'].sum()
#group by year and avocado type, sum the numbers sold for each type
avg_prices_by_year_type = filtered_avocado.groupby(['Year', 'type'])['AveragePrice'].mean()
#find mean avocado price for each type
total_sales_year = (sales_for_year * avg_prices_by_year_type).unstack()
#multiply to get sales in usd then unstack to maintain atomicity


#Simple side by side bar graph to display the data
total_sales_year.plot(kind='bar')
plt.xlabel('Year')
plt.ylabel('USD')
plt.title('Avocado sales by Type (100s of billions of dollars) 2015-2017', fontsize = 14)
plt.legend(title = 'Type of Avocado')
plt.show()


