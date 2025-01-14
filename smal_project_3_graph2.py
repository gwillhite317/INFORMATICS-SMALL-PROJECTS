import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

avocado_data = pd.read_csv("C:/Users/mowma/Downloads/avocado.csv")
#read in data as df
avocado_data['Date'] = pd.to_datetime(avocado_data['Date'], format='%m/%d/%y')
#convert date coloumn into proper formatiing
filtered_avocado = avocado_data[avocado_data['Date'].dt.year.isin([2015, 2016, 2017])] 
#filter for years excluding 2018
sales_by_region = filtered_avocado.groupby(['region', filtered_avocado['Date'].dt.year])['Number_Avocados_Sold'].sum()
#get sales by region per year
total_sales_by_region = sales_by_region.groupby('region').sum()
#total all sales so we can find top regions
top_regions = total_sales_by_region.sort_values(ascending=False).head(10)
#find top regions by taking the top 10 values of our sorted dataframe
top_regions_data = sales_by_region.loc[top_regions.index].unstack()
#unstack to remain atomicity



#this plot shows trends between the top 10 regions
plt.figure(figsize=(10, 6))
top_regions_data.T.plot(marker='o')
plt.title('Avocado Sales trends 2015-2017 across top 10 regions')
plt.ylabel('Volume by 100 billion')
plt.xlabel('Year')

plt.xticks([2015,2016,2017])
plt.legend(title='Region', loc='upper left')
plt.tight_layout()
plt.show()