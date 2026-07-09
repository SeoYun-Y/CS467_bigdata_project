import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# Q1 January - March 31
# Q2 April 1 - June 3
# Q3 July 1 - September 30
# Q4 October 1 - December 31

#tTopic_01 -> drums,aggresive,precussive
#tTopic_02 -> calm,quiet,mellow
#tTopic_03 -> energetic, speech, bright
#tTopic_04 -> piano, orchestra, harmonic
#tTopic_05 -> guitar,loud,energetic
#tTopic_06 -> male,voice, vocal
#tTopic_07 -> rounded,mellow
#tTopic_08 -> female voice, melodic,vocal

# Import the csv's to Dataframe
df = pd.read_csv("EvolutionPopUSA_MainData.csv")
df2 = pd.read_csv("unique_tracks_info_noDupes.csv")

# Truncate the columns to what I want in unique tracks
colstoKeep = ['artist_name','track_title','popularity']
df2 = df2[colstoKeep]

# Rename one column to match other csv and truncate 
df.rename(columns= {'track_name': 'track_title'}, inplace=True)
colstoKeep = ['artist_name','track_title','quarter','tTopic_01','tTopic_02','tTopic_03'
              ,'tTopic_04','tTopic_05','tTopic_06','tTopic_07','tTopic_08']
df = df[colstoKeep]

#Merge to two csv's on simlar columns.
df_merged = pd.merge(df2,df,on=['artist_name','track_title'])

# Test csv to se eif it was correct
# df_merged.to_csv("test.csv",header=True)

df_merged[['year','Q']] = df_merged['quarter'].str.split(' ',expand=True)
df_merged['year'] = df_merged['year'].astype(int)
df_merged = df_merged.drop("quarter",axis=1)


quarters = ['Q1', 'Q2', 'Q3', 'Q4']
decades = list(range(1960, 2030, 10))
correlation_data = {decade: {'Topic': [], 'Q1': [], 'Q2': [], 'Q3': [], 'Q4': []} for decade in decades}

def get_decade(df,start):
    end = start + 9
    return df[(df_merged['year'] >= start) & (df['year'] <= end)]

decades_to_remove = []

for decade in decades:
    decade_data = get_decade(df_merged, decade)
    
    # Compute correlations for each quarter
    for quarter in quarters:
        quarter_data = decade_data[decade_data['Q'] == quarter]
        for i in range(8):  
            topic_col = 'tTopic_0' + str(i+1)
            
            if quarter_data[topic_col].notna().any() and quarter_data['popularity'].notna().any():
                correlation = quarter_data[topic_col].corr(quarter_data['popularity'])
                
                if topic_col not in correlation_data[decade]['Topic']:
                    correlation_data[decade]['Topic'].append(topic_col)
                correlation_data[decade][quarter].append(correlation)
            else:
               decades_to_remove.append(decade)

decades = [decade for decade in decades if decade not in decades_to_remove]


fig_size = (16, 10)
decades_per_fig = 2

num_figures = (len(decades) + decades_per_fig - 1) // decades_per_fig  # Rounded up division

for fig_num in range(num_figures):
    plt.figure(figsize=fig_size)
    
    # Set the starting and ending index for the current figure
    start_idx = fig_num * decades_per_fig
    end_idx = min((fig_num + 1) * decades_per_fig, len(decades))
    
    for i, decade in enumerate(decades[start_idx:end_idx]):
        plt.subplot(decades_per_fig, 1, i + 1)
        for q in ['Q1', 'Q2', 'Q3', 'Q4']:
            if correlation_data[decade][q]:  # Check if there's data for this quarter
                plt.plot(correlation_data[decade]['Topic'], correlation_data[decade][q], marker='o', label=q)
        plt.title(f'Correlation by Topic and Popularity ({decade}s)')
        plt.xlabel('Topics')
        plt.ylabel('Correlation')
        plt.xticks(rotation=45)
        plt.legend(title='Quarter')
        plt.ylim(-.5,.5)
        plt.grid(True)
    
    plt.tight_layout()
    plt.show()