import pandas as pd
import pickle
import streamlit as st
import numpy as np

from sklearn.cluster import KMeans

data = pd.read_csv('C:/Users/LG/Pythonfiles/Project/songs_data_clean.csv')

del data['track_id']
del data['artist_id']
del data['type']
del data['id']
del data['uri']
del data['track_href']
del data['analysis_url']

def normalize_column(col):
    max_d = data[col].max()
    min_d = data[col].min()
    data[col] = (data[col] - min_d)/(max_d - min_d)


num_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
num = data.select_dtypes(include=num_types)

for col in num.columns:
    normalize_column(col)

km = KMeans(n_clusters=10)
cat = km.fit_predict(num)
data['cat'] = cat
normalize_column('cat')


class SpotifyRecommender():
    def __init__(self, rec_data):
        # our class should understand which data to work with
        self.rec_data_ = rec_data

    # function which returns recommendations, we can also choose the amount of songs to be recommended
    def get_recommendations(self, song_name, amount=20):
        distances = []
        # choosing the data for our song
        song = self.rec_data_[(self.rec_data_.track_name.str.lower() == song_name.lower())].head(1).values[0]
        # dropping the data with our song
        res_data = self.rec_data_[self.rec_data_.track_name.str.lower() != song_name.lower()]
        for r_song in (res_data.values):
            dist = 0
            for col in np.arange(len(res_data.columns)):
                # indeces of non-numerical columns
                if not col in [0, 1]:
                    # calculating the manhettan distances for each numerical feature
                    dist = dist + np.absolute(float(song[col]) - float(r_song[col]))
            distances.append(dist)
        res_data['distance'] = distances
        # sorting our data to be ascending by 'distance' feature
        res_data = res_data.sort_values('distance')
        columns = ['track_name']
        return res_data[columns][:amount]

recommender = SpotifyRecommender(data)


class SpotifyRecommender_Artist():
    def __init__(self_1, rec_data_1):
        # our class should understand which data to work with
        self_1.rec_data__1 = rec_data_1

    # function which returns recommendations, we can also choose the amount of songs to be recommended
    def get_recommendations_artist(self_1, artist_name_1, amount=20):
        distances = []
        # choosing the data for our song
        artist = \
        self_1.rec_data__1[(self_1.rec_data__1.artist_name.str.lower() == artist_name_1.lower())].head(1).values[0]
        # dropping the data with our song
        res_data_1 = self_1.rec_data__1[self_1.rec_data__1.artist_name.str.lower() != artist_name_1.lower()]
        for r_artist in (res_data_1.values):
            dist = 0
            for col in np.arange(len(res_data_1.columns)):
                # indeces of non-numerical columns
                if not col in [0, 1]:
                    # calculating the manhettan distances for each numerical feature
                    dist = dist + np.absolute(float(artist[col]) - float(r_artist[col]))
            distances.append(dist)
        res_data_1['distance'] = distances
        # sorting our data to be ascending by 'distance' feature
        res_data_1 = res_data_1.sort_values('distance')
        columns = ['track_name']
        return res_data_1[columns][:amount]

recommender_artist = SpotifyRecommender_Artist(data)


name_dict = pickle.load(open('names_all.pkl','rb'))
name = pd.DataFrame(name_dict)

song_name_dict = pickle.load(open('song_names.pkl','rb'))
song_name = pd.DataFrame(song_name_dict)

artist_name_dict = pickle.load(open('artist_names.pkl','rb'))
artist_name = pd.DataFrame(artist_name_dict)


st.title('Song Recommender System')

selected_name = st.selectbox('Enter Song name or Artist name',
                      name['name'].values)

if st.button('Recommend'):
    if selected_name in song_name.values:
        recommendation_song = recommender.get_recommendations(selected_name)
        for i in (recommendation_song['track_name']):
            st.write(i)
    else:
        recommendation_artist = recommender_artist.get_recommendations_artist(selected_name)
        for i in (recommendation_artist['track_name']):
            st.write(i)