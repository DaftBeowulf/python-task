# Load JSON function
import json

# open movies.json and load it into python list
input_file = open('data/movies.json')
movies = json.load(input_file)



def assemble_cast(movie_list):
    cast_dict = {}

    for movie in movie_list:
        for member in movie["cast"]:
            key=f'{member},{movie["year"]}'
            if key in cast_dict:
                cast_dict[key] += 1
            else:
                cast_dict[key]=1

    for key in sorted(cast_dict.keys()):
        print(f'{key},{cast_dict[key]}')
    # length of output: 55484



assemble_cast(movies)