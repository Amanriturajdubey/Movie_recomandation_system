import pandas as pd
import numpy as np

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')


movies = movies.merge(credits ,on='title')    # First we merge the both data_sets  ...in base of title coloum

movies = movies[['movie_id','title','crew','cast','genres','keywords','overview']]   #  we Target the selected coloum




movies.dropna(inplace=True)                       #  Handle the Missing Value ......
# print(movies.isnull().sum())

print(movies.duplicated().sum())                  # Check Duplicates Rows are Exits or Not .....




import ast
# ast.literal_eval()          ast.literal_eval() Function convert string values in (actual) list..

def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
     L.append(i['name'])
    return L    



movies['genres'] = movies['genres'].apply(convert)    # we store the converted values in same rows .... in Genres coloum
movies['keywords'] = movies['keywords'].apply(convert)   # We same Function Apply on Keyword coloum .....


# print(movies['genres'])
# print(movies['keywords'])

def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
     if counter != 3 :
       L.append(i['name'])
       counter += 1 
     else :
       break
    return L    

movies['cast'] = movies['cast'].apply(convert3) 
# print(movies['cast'])




def fetch_director(obj):       # we perform operation in crew coloum  and find the [ job == director name ] with function()
    L = []
    for i in ast.literal_eval(obj):
     if i['job'] == 'Director' :
       L.append(i['name'])
       break
    return L    

movies['crew'] = movies['crew'].apply(fetch_director)
# print(movies['crew'])




movies['overview'] = movies['overview'].apply(lambda x:x.split())     # We use Split function to convert all overview coloum  collective data in seprate list
# print(movies['overview'])



movies['genres']  = movies['genres'].apply(lambda x: [i.replace(" ","") for i in x])        #  In this code we remove spces from name like [aman dubey] this code remove space between aman and dubey  the code make is amandubey ...
movies['crew']  = movies['crew'].apply(lambda x: [i.replace(" ","") for i in x])
movies['cast']  = movies['cast'].apply(lambda x: [i.replace(" ","") for i in x])
movies['keywords']  = movies['keywords'].apply(lambda x: [i.replace(" ","") for i in x])




movies['tags']   =  movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']   # In this code we concate the 5 colum and store them in tags coloum ...



new_df = movies[['movie_id','title','tags']]      #    We create a new dataframe and store the 3 coloum data ....



movies['tags']  = movies['tags'].apply(lambda x:" ".join(x))   # we convert the list into string

# new_df['tags']  = new_df['tags'].apply(lambda x: x.lower())

# new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())     # we convert into lowercase()

# print(new_df.head())
# print(new_df['tags'][0])





from nltk.stem.porter import PorterStemmer                  # this Liabarary convert word in same word [love,loving,loved]  into [love,love,love]
ps = PorterStemmer()                                        # example : ['martin' , 'harvey','wearyy']   into ['mart' , 'harve' ,'weary']

def stem(text):
  y = []
  for i in text.split():
    y.append(ps.stem(1))

    return " ".join(y)
   
  new_df['tags'] = new_df['tags'].apply(stem)





                                   #  WE Start Here Victorrization  ...... [Victorrization Means Convert text Into Number]




from sklearn.feature_extraction.text import CountVectorizer

new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))          #  We Convert List into String


cv = CountVectorizer(max_features=5000,stop_words='english')        # [Stop_word Means : common word like .. is,am ,are ,the ,a, etc...like that]
                                                                    # [max_features means:  maximum count for countVectorizer]


vectors = cv.fit_transform(new_df['tags']).toarray()            # Convert sparse metrix into numpy array

ai = cv.get_feature_names_out()
# print(ai)
# print(vectors[0])




from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vectors)   
                                                            # ye cousine_similarity function find the similarity between start from 1 rows too all rows [4806] ... 
                                                             # this function find the similarity between rows...he comapre 1 first rows too 4804 rows and after that he comapere next rows too alll..



def recommend(movie):
  movie_index = new_df[new_df['title'] == movie].index[0]
  distances = similarity[movie_index]
  movie_list = sorted(list(enumerate(distances)),reverse=True ,key = lambda x:x[1])[1:11]

  for i in movie_list :
    print(new_df.iloc[i[0]].title)

recommend('The Avengers')



import pickle

pickle.dump(new_df.to_dict(),open('movie_dict.pkl','wb'))

new_df.to_dict

pickle.dump(similarity,open('similarity.pkl','wb'))





