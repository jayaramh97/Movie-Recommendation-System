import pandas as pd
from rapidfuzz import process, fuzz
from sentence_transformers import CrossEncoder
from pick import pick
import sys

def main():
    df = pd.read_csv('https://query.data.world/s/uikepcpffyo2nhig52xxeevdialfl7')
    df['Actors'] = df['Actors'].map(lambda x: x.split(','))
    title = 'Please choose one option: '
    options = ['1) Search for movies by actor name', '2) Search for movies similar to your movie name input', "3) I'm feeling lucky (Randomly returns a movie)"]
    option, index = pick(options, title)

    if index == 0:
        search_actor = input("Enter Actor name: ")
        mov_list, url_list, actor = recommend_actor(df, search_actor)
        print(f"The top {len(mov_list)} movie(s) of {actor.strip()} are")
        for i in range(len(mov_list)):
            print(f"{mov_list[i]}:",f"{url_list[i]}")

    elif index==1:
        search_movie = input("Enter Movie name: ")
        movie = recommend_movie(df, search_movie)
        print(movie)

    elif index==2:
        movie = lucky(df)
        print(movie)

def recommend_actor(df, search_actor):



    #search_actor = input("Enter Actor name: ")
    max_score = 0
    for i in df['Actors']:
        most_similar = process.extractOne(search_actor, i, scorer=fuzz.WRatio)
        if most_similar[1] > max_score:
            max_score = most_similar[1]
            actor = most_similar[0]

    YorN = 'y'
    if search_actor.lower().strip() == actor.lower().strip():
        actor_present = False
    else:
        YorN = input(f"{search_actor} is not available. Do you mean {actor.strip()}? (Type Y to proceed/N to exit) ")
        if 'n' in YorN.lower():
            sys.exit()
        else:
            actor_present = False


    if 'y' in YorN.lower().strip():
        cool = df['Actors'].apply(lambda x: actor in x)
        mov_df = df[cool][:3]
        mov_list = mov_df['Title'].tolist()
        url_list = mov_df['tomatoURL'].tolist()
        #print(mov_list, url_list, actor)
        return mov_list, url_list, actor


def recommend_movie(df, search_movie):
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

    movie_present = True


    #search_movie = input("Enter Movie name: ")
    max_score = 0

    most_similar = process.extractOne(search_movie, df['Title'].tolist(), scorer=fuzz.WRatio)
    #print(most_similar)
    if most_similar[1] > max_score:
        max_score = most_similar[1]
        movie = most_similar[0]

    YorN = 'y'
    if search_movie.lower().strip() == movie.lower().strip():
        movie_present = False
    else:
        YorN = input(f"{search_movie} is not available. Do you mean {movie.strip()}? (Type Y to proceed/N to exit) ")
        if 'n' in YorN.lower():
            sys.exit()


    df['Summary'] = df['Plot'] + ' ' + df['Genre']
    df1 = df[df['Title'] == movie]

    query = df1['Summary'].iloc[0]
    passages = df['Summary'].tolist()
    ranks = model.rank(query, passages, return_documents=True)

    similar_movie = ranks[1]['text']
    df2 = df[df['Summary']==similar_movie]
    return f'If you liked "{movie}", you might also enjoy: {df2["Title"].iloc[0]}'

def lucky(df):
    df1 = df.sample()
    return f"You should watch '{df1['Title'].iloc[0]}', which has an IMDb rating of {df1['Ratings.Value'].iloc[0]}. You can find more information here {df1['tomatoURL'].iloc[0]}"

if __name__ == "__main__":
    main()
