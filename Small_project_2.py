
import pandas as pd
import numpy as np


#Question 1


#loading in the dataframe then creating finding all of the unique years (1980-1989)
dataframe_1980 = pd.read_csv("C:/Users/mowma/Downloads/archive/1980sClassics.csv")
distinct_years = dataframe_1980['Year'].unique()
yearly_averages = {}
#empty dictionary to store the average valence for each year

for year in distinct_years:
    yearly_averages[year] = dataframe_1980.loc[dataframe_1980['Year'] == year, 'Valence'].mean()

#calculate the mean valence for each year

#convert averages to a dataframe, then write it to a csv
average_valence = pd.DataFrame(list(yearly_averages.items()), columns=['Year', 'Average valence'])
average_valence.to_csv("avg_valence_per_year.csv")


#Question 2


def convert_duration_to_seconds(duration):
    minutes, seconds = map(int, duration.split(':'))
    return minutes * 60 + seconds
#function to convert the time in the format (0:00) to seconds, so we split, multiply minutes by 60 then seconds is the second part of our map and they are added together


dataframe_1980['Duration'] = dataframe_1980['Duration'].apply(convert_duration_to_seconds)  #apply the change to the original csv
bins = [0, 60, 180, 300,(np.inf)]
labels = ['<1 min', '1-3 min','3-5 min ','>5 min']
dataframe_1980['Duration_binned'] = pd.cut(dataframe_1980['Duration'], bins=bins, labels=labels, right=True)
#using bins to create a new coloumn categorizing them by their lengths



#creating variables to store top songs by category
top_5_songs = {}
formatted_data = []
distinct_bins = dataframe_1980['Duration_binned'].unique()
#get the unique duration categories


for duration_bin in distinct_bins:
    if pd.notna(duration_bin): 
        #select top 5 most danceable songs in each duration category
        top_songs = (
            dataframe_1980[dataframe_1980['Duration_binned'] == duration_bin]
            .nlargest(5, 'Danceability')
            [['Track', 'Artist', 'Duration', 'Danceability']]
        )
        #store the song details aswell as formatting it
        for _, row in top_songs.iterrows():
            formatted_data.append({
                'Category': duration_bin,
                'Track': row['Track'],
                'Artist': row['Artist'],
                'Duration': int(row['Duration']),  
                'Danceability': round(row['Danceability'], 3)  
            })

#convert to a dataframe and export to a csv
output_df = pd.DataFrame(formatted_data)
output_df.to_csv('top_5_songs_danceability.csv', index=False)


#Question 3
#Do artists whop have released more than 5 tracks tend to have a mode of 1 or 0

#use lambda to filter for artists who have released more than five tracks
over_five = dataframe_1980.groupby("Artist").filter(lambda x: len(x) > 5)

#create empty list to store results
artist_results = []
for artist, group in over_five.groupby("Artist"):
    total_songs = len(group)
    #count songs in mode one and two
    mode_1_count = (group['Mode'] == 1).sum()
    mode_0_count = (group['Mode'] == 0).sum()
    #store the results for each artist
    artist_results.append({
        'Artist': artist,
        'Total Songs': total_songs,
        'Mode 1 Songs': mode_1_count,
        'Mode 0 Songs': mode_0_count
    })

#convert to dataframe and export to a csv
results_df = pd.DataFrame(artist_results)
results_df.to_csv('mode_count.csv', index=False)


#Question 4

#identify even and odd years
odd_years = dataframe_1980[dataframe_1980['Year'] % 2 != 0]
even_years = dataframe_1980[dataframe_1980['Year'] % 2 == 0]

average_pop_odd = (
    odd_years.groupby("Year")["Popularity"]
    #group by year and popularity then find mean (average popularity) of all odd years
    .mean()
    .reset_index()
    .sort_values(by="Popularity", ascending=False)   
)


average_pop_even = (
    even_years.groupby("Year")["Popularity"]
    #group by year and popularity then find mean (average popularity)
    .mean()
    .reset_index()
    .sort_values(by="Popularity", ascending=False)
)

top_pop = (
    dataframe_1980.groupby("Year")["Popularity"]
    #find the year with the top average popularity
    .mean()
    .reset_index()
    .sort_values(by="Popularity", ascending = False)
    .head(1)
)

#headers to follow formatting requested
odd_header = pd.DataFrame([{"Year": "Odd Years", "Popularity": None}])
even_header = pd.DataFrame([{"Year": "Even Years", "Popularity": None}])
top_header = pd.DataFrame([{"Year": "Top Year", "Popularity": None}])

average_popularity_combined = pd.concat([
    odd_header,
    average_pop_odd,
    even_header,
    average_pop_even,
    top_header,
    top_pop
]).reset_index(drop=True)

#concatenate it all together

#add the results to a csv
average_popularity_combined.to_csv("even_odd.csv", index=False)





#Question 5



#creating a new coloumn  with bins and labels to identify tempo groups

bins_2 = [60, 70, 80, 100, 110, 120, 156, 168, 200, np.inf]
labels_2 = ['Adagio', 'Andante', 'Moderato', 'Allegretto', 'Allegro', 'Vivace', 'Presto', 'Prestissimo', 'NA']
dataframe_1980['Tempo_category'] = pd.cut(dataframe_1980['Tempo'], bins = bins_2, labels=labels_2, right = True)


grouped_and_counted = (
    dataframe_1980.groupby(['Artist', 'Tempo_category'])
    #group tracks by artist and tempo category then count number of trakcs
    .size()
    .reset_index(name='Number_of_Tracks')
)

sorted_and_filtered = (
    grouped_and_counted.sort_values(by=['Tempo_category', 'Number_of_Tracks'], ascending=[True, False])
    .groupby('Tempo_category')
    #sort and select the top 2 artist for each tempo category
    .head(2)  
    .reset_index(drop=True)
)

sorted_and_filtered.to_csv('top_artists_by_tempo.csv', index=False)

