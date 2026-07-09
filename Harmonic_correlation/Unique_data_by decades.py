import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = pd.read_csv("songs_with_release_year.csv")

df_reduce = df.drop(columns=['track_id', 'artist_genres', 'key', 'mode', 'speechiness', 'danceability'])

col_to_cor = ['energy','loudness','acousticness','instrumentalness','liveness','valence','tempo']
df_reduce.dropna(inplace=True)

df_reduce['release_year'] = df_reduce['release_year'].astype(int)
print(df_reduce['release_year'].min())

def get_decade(df, start_year):
    end_year = start_year + 9
    return df[(df['release_year'] >= start_year) & (df['release_year'] <= end_year)]

decades = list(range(1950, 2030, 10))

correlation_data = {decade: [] for decade in decades}

for decade in decades:
    decade_data = get_decade(df_reduce, decade)
    
    for col in col_to_cor:
        correlation = decade_data[col].corr(decade_data['popularity'])
        correlation_data[decade].append(correlation)


correlation_df = pd.DataFrame(correlation_data, index=col_to_cor)

plt.figure(figsize=(12, 6))
sns.heatmap(correlation_df, annot=True, cmap='coolwarm', center=0, linewidths=0.5)
plt.title('Correlation of Features with Popularity for Each Decade')
plt.xlabel('Decades')
plt.ylabel('Features')

plt.show()

plt.figure(figsize=(12, 6))

for decade in decades:
    plt.plot(correlation_df.index, correlation_df[decade], marker='o', label=f'{decade}s')

plt.title('Correlation of Features with Popularity by Decade')
plt.xlabel('Features')
plt.ylabel('Correlation with Popularity')
plt.xticks(rotation=45)  # Rotate x labels for better readability
plt.legend(title='Decade', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()