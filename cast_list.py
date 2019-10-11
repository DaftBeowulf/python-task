# Load JSON function
import json

# load imdb library for cast name verification
from imdb import IMDb, IMDbError

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


def assemble_verified_cast(movie_list):
    cast_dict = {}
    invalid_dict = {}

    for movie in movie_list:
        for member in movie["cast"]:
            key=f'{member},{movie["year"]}'
            if key in cast_dict:
                cast_dict[key] += 1
            elif key not in invalid_dict:
                try:
                    ia=IMDb()
                    people = ia.search_person(member)
                    if len(people) >0 and people[0]['name']==member:
                        cast_dict[key]=1
                    else:
                        invalid_dict[key]=1
                except IMDbError as err:
                    print(err)

    for key in sorted(cast_dict.keys()):
        print(f'{key},{cast_dict[key]}')

    # unknown length of full output due to exceptional runtime


def assemble_pseduo_verified_cast(movie_list):
    cast_dict = {}

    for movie in movie_list:
        for member in movie["cast"]:
            key=f'{member},{movie["year"]}'
            if key in cast_dict:
                cast_dict[key] += 1
            elif member[0].isupper() or member == 'will.i.am':
                cast_dict[key]=1

    for key in sorted(cast_dict.keys()):
        print(f'{key},{cast_dict[key]}')

    # output length: 55019

# assemble_verified_cast(movies[:250])
# assemble_cast(movies)
assemble_pseduo_verified_cast(movies) 