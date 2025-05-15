from project import recommend_actor, recommend_movie, lucky
import pandas as pd
import re

df = pd.read_csv('https://query.data.world/s/uikepcpffyo2nhig52xxeevdialfl7')
df['Actors'] = df['Actors'].map(lambda x: x.split(','))

def test_recommend_actor():
    assert recommend_actor(df, 'Tom Hanks') == (['Forrest Gump', 'Saving Private Ryan', 'The Green Mile'], ['http://www.rottentomatoes.com/m/forrest_gump/', 'http://www.rottentomatoes.com/m/saving_private_ryan/', 'http://www.rottentomatoes.com/m/green_mile/'], 'Tom Hanks')
    assert recommend_actor(df, 'Christian Bale') == (['The Dark Knight', 'The Dark Knight Rises', 'Batman Begins'], ['http://www.rottentomatoes.com/m/the_dark_knight/', 'http://www.rottentomatoes.com/m/the_dark_knight_rises/', 'http://www.rottentomatoes.com/m/batman_begins/'], 'Christian Bale')
    assert recommend_actor(df, 'Tom Cruise') == (['Rain Man'], ['http://www.rottentomatoes.com/m/rain_man/'], ' Tom Cruise')

def test_recommend_movie():
    assert recommend_movie(df, 'The Shawshank Redemption') == 'If you liked "The Shawshank Redemption", you might also enjoy: Papillon'
    assert recommend_movie(df, 'The Dark Knight') == 'If you liked "The Dark Knight", you might also enjoy: The Dark Knight Rises'
    assert recommend_movie(df, 'The Lord of the Rings: The Fellowship of the Ring') == 'If you liked "The Lord of the Rings: The Fellowship of the Ring", you might also enjoy: The Lord of the Rings: The Return of the King'

def test_lucky():
    value = lucky(df)
    assert re.match(r"You should watch '.*', which has an IMDb rating of \d.?\d/10\. You can find more information here (https?://)?(www\.)?rottentomatoes.com/m/.*/",value)
