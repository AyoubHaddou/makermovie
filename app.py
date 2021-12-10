# Les imports : 
from os import waitpid
import streamlit as st
import pandas as pd
import numpy as np 


# Fonction pour charger les données sur streamlit :
@st.cache
def load_data(nrows):
    data = pd.read_csv("imdb_movie.csv", nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Import du CSV dans mon Df
imdb = pd.read_csv("imdb_movie.csv")


## --------------  ## -----------------------Déclaration de mes variables : 

# I Convert my Datafram title colomn to list 
list_movies = imdb['title'].tolist()

# I convert my Datafram actors colomn to list 
list_actors = []
for i in imdb['actors']:
    for j in i.split(","):
        list_actors.append(j)

# I convert my Datafram country colomn to list 
list_country = []
for i in imdb['Origin country']:
    for j in i.split(','):
        list_country.append(j)

# I convert my Datafram category colomn in a list 
list_category = []
for i in imdb["genre"]:
    for j in i.split(','):
        list_category.append(j)

# I convert my Datafram language colomn in a list 
list_language = []
for i in imdb["Origin language"]:
    for j in i.split(","):
        list_language.append(j)

# For my slide bar duration (slider between 60min and 400min)
time = [i for i in range (60,400, 30)] 
# For rating movie filter (not slider between 8,10 and 10)
score = [i for i in np.arange(8,10.5,0.5)]

# Je supprime la colonne 0 
imdb.drop(imdb.columns[0], axis=1, inplace=True)

# # J'arrondie la colonne note a 0.1 
# (fonctionnne pas, a refaire)
# imdb['note'] = round(imdb['note'], 1)

# Titre de la page
st.title('Make your movie:')
st.sidebar.subheader('Filters :')
st.subheader('Movies explorer:')

# Je change les NaN de ma colonne video par la bande annonce de Ghostbuster 
# (a faire plus tard : Creer condition pour afficher message pas de bande annonce dispo pour les NaN)
imdb['video'].fillna('https://www.imdb.com/video/vi637322009?playlistId=tt4513678&ref_=tt_pr_ov_vi',  inplace=True)


## --------------  ## ----------------------- Déclaaration des inputs :

# Boutons sidebar pour la navigation dans le site 
all = st.sidebar.radio("Choose options :", ("All","Filters", 'Modelisation',"Others"))


# All pour afficher le df complet 
if all == "All" :
    st.write( "Our all Liberary below! ",imdb)

    st.subheader('TOP 3 movies from IMDB:')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Top - 1")
        st.write("Jai Bhin - Trailer song")
        st.video("https://www.youtube.com/watch?v=YwVHHZNtdKU")
    with col2:
        st.subheader("Top - 2")
        st.write("Les évadés - Original Trailer")
        st.video("https://www.youtube.com/watch?v=2e8Otbbcowc")
    with col3:
        st.subheader("Top - 3 ")
        st.write("From IMDB.com")
        st.write("Le parrain - Original Trailer")
        st.video("https://imdb-video.media-imdb.com/vi1158527769/1434659607842-pgv4ql-1564710232825.mp4?Expires=1638049348&Signature=GbVqeeVDcF8FtN933wd3MhHd5b2YMBuvtDQRbDLE2vCfn~hdqNpDRxttFF4bOPU4qv68dfM5EqPF7xIUdKfPXdd2Jy5Q449X9uYMrwSJqznMMCma-ajm4VOO-WFQr2VcwWffa-r7b5POYpYUN5kGQvgCA5U7HLf3kjY27kIcaA73p9MR5FfFGkTxiQEmV31xD55kBFm2L~KM5WMGvU7leYpuSuAj9c89t2OAwTLaIxQaKfZCnwPSOyJQQKPzCVhENNbgnT~nJF8Tjn72Q3ceQLCmT8HwASQfTxDDN1-pfQfZfAEYLEJoTN7hJbN6lChidJc5CrDv1qiOAsC~F7iLuw__&Key-Pair-Id=APKAIFLZBVQZ24NQH3KA")
        

# Selections pour les filtres 
if all == "Filters":
    duration = st.sidebar.select_slider("By duration", time )
    movie = st.sidebar.multiselect("By movies title", set(list_movies))
    choose_actors = st.sidebar.multiselect('Select your actors',set(list_actors))
    country = st.sidebar.multiselect("Country", set(list_country))
    category = st.sidebar.multiselect('Category',set(list_category))
    language = st.sidebar.multiselect('Language', set(list_language))
    note = st.sidebar.select_slider('By score', score )
    

# Instentciation de mon mask
    mask = pd.Series(True, index=imdb.index)
    
# Creation des conditions dans les mask ( Par Durée, par films, par acteurs, par pays, par langue ou par catégorie)
    for i in choose_actors :
        mask &= imdb['actors'].str.contains(i)
    for i in country:
        mask &= imdb['Origin country'].str.contains(i)
    for i in category :
        mask &= imdb['genre'].str.contains(i)
    for i in language :
        mask &= imdb['Origin language'].str.contains(i)
    if duration > 60:
        mask &= imdb['duration'] <= int(duration)
    if note > 8 :
        mask &= imdb['note'] <= note
    if movie : 
        mask &= imdb['title'].isin(movie)
    st.write("With filters :", imdb[mask])
    
#  Inserer la selection du mask dans recherche de streaming ou Bande annonce
    stream_choose = st.sidebar.selectbox('Your movie selection: ' ,  imdb[mask])


    stream_button_trailer = st.sidebar.button("Clic to redirect youtube trailer")
    if stream_button_trailer :
        vid = imdb["video"][imdb['title'].str.contains(stream_choose)]
        st.write('Clic below if the video doesn\'t start ')
        st.write(vid.iloc[0])
        st.video(vid.iloc[0])
        
 
    stream_button_watch = st.sidebar.button("Clic to watch in streaming ")
    if stream_button_watch:
        st.warning('Correct content below is coming soon')
        st.video("https://www.youtube.com/watch?v=0QKGhig31Rw&t=2s")
        

# Partie bonus : Modélisation de nos données 
if all == "Modelisation" : 
    country = [i for i in list_country]
    st.bar_chart(imdb.groupby('Origin country')['note'].mean())
    st.bar_chart(imdb.groupby('Origin country')['duration','movie cost'].mean())
    st.bar_chart(imdb.groupby('Origin country')['duration'].mean())
    st.bar_chart(imdb.groupby(['note']).mean())
    st.bar_chart(imdb.groupby(['duration']).mean())
    st.bar_chart(imdb['note'].describe())

    # st.bar_chart(imdb.sort_values(by = ["Origin country", "genre"], ascending = False ))
    
 # Partie ou je peux essayer des trucscon
if all == "Others":
    st.map()



#Markdown 
st.markdown(

    " ###### Made by Pirate Ayoub.py  "
)

# data_container = st.container()
# with data_container :
# A utiliser pour faire un seul Datafram filtrable avec les conditions ?
# ou plutot st.empty() => Manipule un seul élement ?  