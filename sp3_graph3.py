
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


avocado_data = pd.read_csv("C:/Users/mowma/Downloads/avocado.csv")
#read in csv as df
avocado_data['Date'] = pd.to_datetime(avocado_data['Date'], format='%m/%d/%y')
#format date
filtered_avocado = avocado_data[avocado_data['Date'].dt.year.isin([2015, 2016, 2017]) & (avocado_data['Number_Avocados_Sold'] > 0)]
#filter for years excluding 2018 and sales above zero
filtered_locations = filtered_avocado[filtered_avocado['region'].isin(['Chicago','MiamiFtLauderdale', 'Boston', "LosAngeles"])].copy()
#filter for our desired locations
filtered_locations['Month'] = filtered_locations['Date'].dt.month
#create month coloumn
filtered_locations['Year'] = filtered_locations['Date'].dt.year
#create year coloumn
filtered_locations_totals = filtered_locations.groupby(['Year','region','Month'])['Number_Avocados_Sold'].sum().reset_index()
#get totals sales inclusive with months

#list of cities and years for enumeration purposes
cities = ['Chicago', 'MiamiFtLauderdale', 'Boston', 'LosAngeles']
years = [2015, 2016, 2017]


#three subplots, sharey to ensure common y axis
fig, axs = plt.subplots(1, 3, figsize =(20,5), sharey = True)


#for each distinct year

for i, year in enumerate(years):
    #pull data for specified year
    year_data = filtered_locations_totals[filtered_locations_totals['Year'] == year]
    for city in cities:
        #pull data for each city as an inner loop so it exectes for each year
        city_data = year_data[year_data['region'] ==  city]
        axs[i].plot(city_data['Month'], city_data['Number_Avocados_Sold'], marker = 'o', label = f'{city}')
        #formatted to display points for each month with a line connecting the month points
    axs[i].set_title(f'{year},avocado sales across Chicago, Miami/ Ft Lauderdale, Boston, and Los Angeles')
    #formatted title for different years
    axs[i].set_xticks(range(1,13))
    axs[i].set_yticks((250000000, 500000000, 750000000, 1000000000, 1250000000))
    axs[i].set_yticklabels(['250m', '500m', '750m','1 billion', '1.25 billion' ])
    axs[i].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axs[i].set_xlabel("Month of the Year")
    axs[i].set_ylabel("Volume of avocados sold")
    #all above just for aesthetic reasons
    axs[i].legend(title = f"city")
    #set legend to different cities

plt.tight_layout()
plt.show()

