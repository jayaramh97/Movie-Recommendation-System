# MOVIE RECOMMENDATION FROM TOP 250 IMDb MOVIES
#### Description: This is a movie recommendation system that helps you pick your next movie night watch, using data from IMDb's Top 250 list.

The data for the top 250 movies on IMDb is available [here](https://query.data.world/s/uikepcpffyo2nhig52xxeevdialfl). This is read as a CSV file using pandas library. Three types of recommendations are given to the user to be selected using the [pick](https://pypi.org/project/pick/) library. Those recommendations are:
1) By actor name – find up to 3 top-rated movies of a specific actor.
2) By movie similarity – find the most similar movie based on a chosen title
3) I'm feeling lucky - Get a random recommendation

### Recommendation by Actor Name
If the first option is selected, the user has to input an actor's name. Let us assume the user inputs the name as 'Tom Hanks', then the program proceeds to recommend the top three Tom Hanks movies from the top 250 movies available in the CSV file we picked earlier (which are 'Forrest Gump', 'Saving Private Ryan' and 'The Green Mile'). In case the user makes an error in typing and inputs 'Tom Banks' instead, the program asks the user if they were looking for 'Tom Hanks' instead, to which the user can respond with input 'Y' to proceed or 'N' to exit the program. This matching of 'Tom Banks' to 'Tom Hanks' is done using [RapidFuzz](https://pypi.org/project/RapidFuzz/) library, which is a fast string matching library for Python, which uses the string similarity calculations from FuzzyWuzzy. The best match is returned by calculating the weighted ratio and returns the highest matching string from the list of actors in the CSV file. Finally the three highest rated movies are returned, along with the Rotten Tomatoes URL for the movies.

### Recommendation by Movie Similarity
If the second option is selected, the user has to input a movie name. Let us assume the user inputs the name as 'The Shawshank Redemption', then the program proceeds to find the 'Summary' of the movie, which is a mixture of the 'Plot' of the movie and the 'Genre' of the movie as present in the CSV file. It then uses [sentence transformers](https://sbert.net/) Cross-Encoder class and loads the pretrained model named "cross-encoder/ms-marco-MiniLM-L6-v2". This is trained on the [MS MARCO](https://microsoft.github.io/msmarco/Datasets.html) datasets and the model is ready to rank the input movies summary with the rest of the movies in the top 250 and returns a sorted list with rankings 'Summary'. The first most relevant 'Summary' will obviously be of 'The Shawshank Redemption' so we take the second most relevant summary as the movie that is closest to 'The Shawshank Redemption' in terms of the 'Plot' and 'Genre'. Here that movie is 'Papillon'. We could also use something like the [Rake-nltk](https://pypi.org/project/rake-nltk/) library. RAKE is short for Rapid Automatic Keyword Extraction algorithm, which is a domain independent keyword extraction algorithm which tries to determine key phrases in a body of text by analyzing the frequency of word appearance and its co-occurance with other words in the text. We could use this library as well, along with Vectorizers like [Count-Vectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html) and use the [Cosine-similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html) of the 'Summary' to determine which movie is the most similar to 'The Shawshank Redemption'. I preferred to use Sentence Transformers since it is an LLM based ranking model.

### I'm Feeling Lucky
If the third option is selected, a random movie is picked from the pandas dataframe using [df.sample()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html). This function then returns a string like "You should watch 'Paths of Glory', which has an IMDb rating of 8.5/10. You can find more information here http://www.rottentomatoes.com/m/paths_of_glory/". This can also be done using the random function, to pick an integer between 0-249 and pick the movie based on row index of the pandas dataframe.

### Testing
In my `test_project.py` file, I have tested out each of the functions by giving the inputs as the pandas dataframe and other inputs as required in the function.

The first function takes the pandas dataframe and the name of the actor as inputs, and returns a tuple of a list of movies, a list of Rotten Tomatoes URLs and the actors name.

The second function takes the pandas datafram and the name of the movie as inputs, and returns a string which tells us which movie is the most similar to the input movie.

The third function returns a string that gives a random movie, the corresponding IMDb score and Rotten Tomatoes URL of the movie, which is checked using a regex match like `"You should watch '.*', which has an IMDb rating of \d.?\d/10\. You can find more information here (https?://)?(www\.)?rottentomatoes.com/m/.*/"`.

### Libraries used
- `pandas`
- `sentence-transformers`
- `RapidFuzz`
- `pick`
- (optional, if using other similarity methods) `sklearn`
- (optional, if using keyword extraction) `rake-nltk`
