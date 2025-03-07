# list of disctionaries, where the inner dictionaries represent movies, and have keys: title, genre, and rating 
movies =[]

def create_movie(title, genre, rating):
    if not title or not genre or not rating:
        return None
    return {"title": title, "genre": genre, "rating": rating}

def add_to_watched(user_data, movie):
    user_data["watched"].append(movie)
    return user_data 

def add_to_watchlist(user_data, movie):
    user_data["watchlist"].append(movie)
    return user_data

def watch_movie(user_data, title):
    for movie in user_data['watchlist']:
        if movie['title'] == title:   
            user_data["watched"].append(movie)
            user_data["watchlist"] = [movie for movie in user_data["watchlist"] if not (movie['title'] == title)]
    return user_data 

def get_watched_avg_rating(user_data):
    if len(user_data["watched"]) == 0:
        return 0
    ratings = [movie['rating'] for movie in user_data["watched"]]
    return sum(ratings) / len(user_data["watched"])

def get_most_watched_genre(user_data):
    genres = {}
    if len(user_data["watched"]) == 0:
        return None
    for movie in user_data["watched"]:
        if movie['genre'] in genres.keys():
            genres[movie['genre']] += 1
        else:
            genres[movie['genre']] = 1
        winners = [genre for genre, count in genres.items() if count == max(genres.values())]   
    return winners[0]

def get_unique_watched(user_data):
    # Returns a list of movies that user has seen but none of their friends have seen.
    unique_movies = []
    friends_titles = set()
    for friend in user_data['friends']:
        friends_titles = friends_titles.union({film['title'] for film in friend['watched']})
    for movie in user_data['watched']:
        if movie['title'] not in friends_titles:
            unique_movies.append(movie)
    return unique_movies

def get_friends_unique_watched(user_data):
    # Returns a list of movies that user has not seen but at least one of their friends have seen.
    user_titles = [movie['title'] for movie in user_data['watched']]
    friends_titles = set()
    friends_unique_movies = []
    for friend in user_data['friends']:
        friends_titles = friends_titles.union({film['title'] for film in friend['watched']})
    for title in friends_titles:
        if title not in user_titles:
            friends_unique_movies.append({'title': title})
    return friends_unique_movies

def get_available_recs(user_data):
    # Returns a list of movies that user has not seen but at least one of their friends have seen, 
    # and is available on a service user is subscribed to. 
    movies = []
    for friend in user_data["friends"]:
        movies += [movie for movie in friend['watched'] if movie['host'] in user_data['subscriptions'] 
                   and movie not in user_data['watched'] and movie not in movies]
    return movies

def get_new_rec_by_genre(user_data):
    # Returns a list of movies that user has not seen but at least one of their friends have seen, 
    # and whose genre is user's most watched genre. 
    top_genre = get_most_watched_genre(user_data)
    movies = [] 
    for friend in user_data["friends"]:
        movies += [movie for movie in friend['watched'] if movie['genre'] == top_genre
                   and movie not in user_data['watched'] and movie not in movies]
    return movies


def get_rec_from_favorites(user_data):
    # Returns a list of movies from user's favorites that none of their friends have seen.
    # Assumes all movies in user's favorites are also in user's watched list.
    unique_watched = get_unique_watched(user_data)      
    recommendations = [movie for movie in unique_watched if movie in user_data['favorites']]
    return recommendations
