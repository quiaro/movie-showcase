import json
import os
import operator

import media
import fresh_tomatoes

# JSON data file

# current_dir = os.path.dirname(__file__)
data_file = os.path.abspath(__file__ + '/../../../static/data.json')

# List of Movie instances
movies = []

# Open JSON data file and store its data (JSON object) in a variable
with open(data_file) as data:
    all_data = json.load(data)

# Sort movies by their title
# sorted_movies = sorted(all_data, key=lambda k: k['title'])
sorted_movies = sorted(all_data['movies'], key=operator.itemgetter('title'))

# Extract the information of the 'movies' attribute in the JSON object.
# The 'movies' attribute should be a list of movie objects. For each,
# movie object create a Movie instance and append it to the Movie instances
# list.
for movie_data in sorted_movies:
    movies.append(media.Movie(movie_data))

# Call the method to open the page with the movie listing
fresh_tomatoes.open_movies_page(movies)
