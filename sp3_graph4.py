import matplotlib.pyplot as plt
import pandas as pd


avocado_data = pd.read_csv("C:/Users/mowma/Downloads/avocado.csv")
#read in data as df
avocado_data['Date'] = pd.to_datetime(avocado_data['Date'], format='%m/%d/%y')
#format date coloumn
filtered_avocado = avocado_data[avocado_data['Date'].dt.year.isin([2015, 2016, 2017])]
#filter for proper years
sales_by_region = filtered_avocado.groupby(['region', filtered_avocado['Date'].dt.year, 'type'])['Number_Avocados_Sold'].sum()
#find sales by region
total_sales_by_region = sales_by_region.groupby('region').sum()
#total sales by region to find top regions
top_regions = total_sales_by_region.sort_values(ascending=False).head(5)
#5 top regions
top_regions_data = filtered_avocado[filtered_avocado['region'].isin(top_regions.index)]
#pull data for the top 5 regions
sales_by_region_year_type = top_regions_data.groupby(['region', filtered_avocado['Date'].dt.year, 'type'])['Number_Avocados_Sold'].sum().unstack()
#summ to find total sales by region and type then unstack to retain atomicity
sales_reset = sales_by_region_year_type.reset_index()
#reset index to be able to enumerate


#creates 6 subplots but we'll use 5 and cut the other, use sharey to maintain clarity when comparing the graphs
fig, axs = plt.subplots(2, 3, figsize=(20, 10), sharey = True)
axs = axs.ravel() 
#use ravel because subplot values enduce a 2d arrray


#for each unique region
for i, region in enumerate(sales_by_region_year_type.index.get_level_values(0).unique()):
    region_data = sales_by_region_year_type.loc[region]
    #pull data for region
    region_data = region_data[['organic', 'conventional']]
    #alter index for aesthetic purposes of our stacked bar graph (I want organic on bottom)
    region_data.plot(kind='bar', stacked=True, ax=axs[i])
    #create stacked bar graph
    axs[i].set_title(f'{region} Avocado Sales')
    #formatted title
    axs[i].set_xlabel('Year')
    axs[i].set_ylabel('Number of Avocados Sold')
    #set labels
    axs[i].set_xticklabels([2015, 2016, 2017], rotation=0)
    #ytick labels

if len(top_regions) < 6:
    fig.delaxes(axs[-1])
    #this is just to cut that 6th subplot created

plt.tight_layout()
fig.suptitle('Top 5 Regions - Avocado Sales by Type and Year', fontsize=16)
#general title for subplots
plt.subplots_adjust(top=0.9)
handles, labels = axs[0].get_legend_handles_labels()
#above for aesthetic purposes, label out individual sublplots by the name of their region
fig.legend(handles, labels, loc='upper right', bbox_to_anchor=(1.1, 0.9), title='Avocado Type')
#set legend
plt.show()
