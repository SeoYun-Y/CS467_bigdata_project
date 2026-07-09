import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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
print(df_merged['year'].min())



# Q1-4 data with popularity below year 1990 
df_Q1 = df_merged[(df_merged['Q'] == 'Q1') & (df_merged['year'] <= 1999)]
df_Q2 = df_merged[(df_merged['Q'] == 'Q2') & (df_merged['year'] <= 1999)]
df_Q3 = df_merged[(df_merged['Q'] == 'Q3') & (df_merged['year'] <= 1999)]
df_Q4 = df_merged[(df_merged['Q'] == 'Q4') & (df_merged['year'] <= 1999)]

#print(df_Q3.head())


#These for loops will show the correlation between the Timbres and the Quarters with year 1999 and below
for i in range(8):
    topic_col = 'tTopic_0' + str(i+1)  
    correlation = df_Q1[topic_col].corr(df_Q1['popularity'])
    print(f"Correlation between {topic_col} and popularity in Q1: {correlation}")

for i in range(8):
    topic_col = 'tTopic_0' + str(i+1)  
    correlation = df_Q2[topic_col].corr(df_Q2['popularity'])
    print(f"Correlation between {topic_col} and popularity in Q2: {correlation}")

for i in range(8):
    topic_col = 'tTopic_0' + str(i+1)  
    correlation = df_Q3[topic_col].corr(df_Q3['popularity'])
    print(f"Correlation between {topic_col} and popularity in Q3: {correlation}")

for i in range(8):
    topic_col = 'tTopic_0' + str(i+1)  
    correlation = df_Q4[topic_col].corr(df_Q4['popularity'])
    print(f"Correlation between {topic_col} and popularity in Q4: {correlation}")

# Hold the values
correlation_data = {'Topic': [], 'Q1': [], 'Q2': [], 'Q3': [], 'Q4': []}

# Calculate correlations again
for i in range(8):
    topic_col = 'tTopic_0' + str(i+1)
    correlation_data['Topic'].append(topic_col)
    correlation_data['Q1'].append(df_Q1[topic_col].corr(df_Q1['popularity']))
    correlation_data['Q2'].append(df_Q2[topic_col].corr(df_Q2['popularity']))
    correlation_data['Q3'].append(df_Q3[topic_col].corr(df_Q3['popularity']))
    correlation_data['Q4'].append(df_Q4[topic_col].corr(df_Q4['popularity']))


# Convert to DataFrame for easier plotting
correlation_df = pd.DataFrame(correlation_data)

# Plot the data
plt.figure(figsize=(10, 6))

for q in ['Q1', 'Q2', 'Q3', 'Q4']:
    plt.plot(correlation_df['Topic'], correlation_df[q], marker='o', label=q)

plt.title('Correlation of popularity and timbres in Q1 Q2 Q3 Q4 <= 1999')
plt.xlabel('Topics')
plt.ylabel('Correlation with Popularity')
plt.xticks(rotation=45) 
plt.legend(title='Quarter')
plt.grid(True)
plt.tight_layout()
plt.show()

print("-----------------------------------------------------------------")
# Q1-4 data with popularity with year 2000 and above 
df_Q1_ab = df_merged[(df_merged['Q'] == 'Q1') & (df_merged['year'] >= 2000)]
df_Q2_ab = df_merged[(df_merged['Q'] == 'Q2') & (df_merged['year'] >= 2000)]
df_Q3_ab = df_merged[(df_merged['Q'] == 'Q3') & (df_merged['year'] >= 2000)]
df_Q4_ab = df_merged[(df_merged['Q'] == 'Q4') & (df_merged['year'] >= 2000)]


for i in range(8):
    topic_col = 'tTopic_0' + str(i+1)  
    correlation = df_Q1_ab[topic_col].corr(df_Q1_ab['popularity'])
    print(f"Correlation between {topic_col} and popularity in Q1: {correlation}")
    
print("-----------------------------------------------------------------")

for i in range(8):
    topic_col = 'tTopic_0' + str(i+1)  
    correlation = df_Q2_ab[topic_col].corr(df_Q2_ab['popularity'])
    print(f"Correlation between {topic_col} and popularity in Q2: {correlation}")

print("-----------------------------------------------------------------")

for i in range(8):
    topic_col = 'tTopic_0' + str(i+1)  
    correlation = df_Q3_ab[topic_col].corr(df_Q3_ab['popularity'])
    print(f"Correlation between {topic_col} and popularity in Q3: {correlation}")

print("-----------------------------------------------------------------")

for i in range(8):
    topic_col = 'tTopic_0' + str(i+1)  
    correlation = df_Q4_ab[topic_col].corr(df_Q4_ab['popularity'])
    print(f"Correlation between {topic_col} and popularity in Q4: {correlation}")

print("-----------------------------------------------------------------")


# Hold the values
correlation_data = {'Topic': [], 'Q1': [], 'Q2': [], 'Q3': [], 'Q4': []}

# Calculate correlations again
for i in range(8):
    topic_col = 'tTopic_0' + str(i+1)
    correlation_data['Topic'].append(topic_col)
    correlation_data['Q1'].append(df_Q1_ab[topic_col].corr(df_Q1_ab['popularity']))
    correlation_data['Q2'].append(df_Q2_ab[topic_col].corr(df_Q2_ab['popularity']))
    correlation_data['Q3'].append(df_Q3_ab[topic_col].corr(df_Q3_ab['popularity']))
    correlation_data['Q4'].append(df_Q4_ab[topic_col].corr(df_Q4_ab['popularity']))


# Convert to DataFrame for easier plotting
correlation_df = pd.DataFrame(correlation_data)

# Plot the data

plt.figure(2,figsize=(10, 6))

for q in ['Q1', 'Q2', 'Q3', 'Q4']:
    plt.plot(correlation_df['Topic'], correlation_df[q], marker='o', label=q)

plt.title('Correlation of popularity and timbres in Q1 Q2 Q3 Q4 >= 2000')
plt.xlabel('Topics')
plt.ylabel('Correlation with Popularity')
plt.xticks(rotation=45) 
plt.legend(title='Quater')
plt.grid(True)
plt.tight_layout()
plt.show()

print("-----------------------------------------------------------------")

#Generating Grid Plot for Timbres

columns_of_interest = ['tTopic_01','tTopic_02','tTopic_03','tTopic_04','tTopic_05','tTopic_06','tTopic_07','tTopic_08']

grid_df = df_merged[columns_of_interest].dropna()

g = sns.PairGrid(grid_df)
g = g.map_upper(sns.kdeplot)
g = g.map_lower(sns.kdeplot)
g = g.map_diag(sns.kdeplot, lw=3, legend=False)
plt.show()

print("-----------------------------------------------------------------")

#Generating Grid Plot for Timbres

columns_of_interest = ['tTopic_01','tTopic_02','tTopic_03','tTopic_04','tTopic_05','tTopic_06','tTopic_07','tTopic_08']

grid_df = df_merged[columns_of_interest].dropna()

g = sns.PairGrid(grid_df)
g = g.map_upper(sns.kdeplot)
g = g.map_lower(sns.kdeplot)
g = g.map_diag(sns.kdeplot, lw=3, legend=False)
plt.show()
