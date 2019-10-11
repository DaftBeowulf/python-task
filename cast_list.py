# Load JSON function
import json

# load imdb library for cast name verification
from imdb import IMDb, IMDbError

# load sys for arg parsing
import sys

# open movies.json and load it into python list
input_file = open('data/movies.json')
movies = json.load(input_file)



def assemble_cast(movie_list):
    """
    Accepts list of movies. For each comma-separated cast member + movie year combo, stores
    entry into lookup table cast_dict for instant subsequent lookup times.

    node example: {
        'Zoey Deschanel,2011' : 2
    }

    Sorts keys alphabetically and prints each line as <name>,<year>,<# of films>
    """
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
    """
    Accepts list of movies. For new cast member + movie year combo encountered,
    uses the imdbpy library to verify if cast member exists in imdb database.
    For each comma-separated cast member + movie year combo, stores
    entry into lookup table cast_dict for instant subsequent lookup times.

    node example: {
        'Zoey Deschanel,2011' : 2
    }

    Sorts keys alphabetically and prints each line as <name>,<year>,<# of films>

    This method provides truest verification, but not ideal due to time of each API call
    to imdb's database for each search_person call.
    """
    cast_dict = {}
    invalid_dict = {}

    for movie in movie_list:
        for member in movie["cast"]:
            key=f'{member},{movie["year"]}'
            if key in cast_dict:
                cast_dict[key] += 1
            elif key not in invalid_dict:
                # Imdb's search_person() method uses weighted fuzzy search for possible name matches,
                # with exact match (if found) listed first. If search_person returns nothing or the first 
                # match is not exact, name is either not valid actor/actress or not valid name, and stored
                # in invalid_dict for faster subsequent lookup times.
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
    """
    Accepts list of movies. For new cast member + movie year combo encountered,
    performs loose validation to see if name is capitalized or if name is 'will.i.am'
    as his is currently the only non-capitalized actor's name.
    For each comma-separated cast member + movie year combo, stores
    entry into lookup table cast_dict for instant subsequent lookup times.

    node example: {
        'Zoey Deschanel,2011' : 2
    }

    Sorts keys alphabetically and prints each line as <name>,<year>,<# of films>

    Currently eliminate ~500 invalid entries, but this method provides only loose validation 
    and not reliable in every case:
    -Does not catch capitalized non-name string instead of a valid name
    -Would not catch new actor with an all-lowercase name    
    """
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

if __name__ == '__main__':
    if len(sys.argv) > 1 and 'pseudo' in sys.argv:
        assemble_pseduo_verified_cast(movies) 
    elif len(sys.argv) > 1 and 'valid' in sys.argv:
        assemble_verified_cast(movies[:250]) #only run first 250 entries to verify functionality
    else:
        assemble_cast(movies)