#!/usr/bin/env python

"""The media_manager module contains the MediaManager class"""

from media import Movie
from tmdb import TMDB

__author__ = "Christiaan Lombard <base1.christiaan@gmail.com>"


class MediaManager():
    """Manages user media

    Attributes:
        favorite_ids (list): Static list of favorite movie ids
        api (TMBD): The TMDB API wrapper to use
    """

    favorite_ids = [
        13183,
        4935,
        9900,
        75612,
        603
    ]

    def __init__(self, api):
        """Create a MovieManager instance"""

        self.api = api

    def list_popular_movies(self):
        """Get a list of popular movies

        Returns:
            list -- List of Movie instances
        """

        movies = []
        list_response = self.api.list_popular_movies()
        for result in list_response['results']:
            detail_response = self.api.get_movie_details(result['id'])
            movies.append(self._convert_movie_detail(detail_response))
        return movies

    def list_favorite_movies(self):
        """Get a list of favorite movies

        Returns:
            list -- List of Movie instances
        """

        movies = []
        # from the list of movie ids, get the detail of each movie
        for id in self.favorite_ids:
            detail_response = self.api.get_movie_details(id)
            movies.append(self._convert_movie_detail(detail_response))
        return movies

    def _convert_movie_results(self, response):
        """Convert a list of movies API response to a list of Movie instances

        Arguments:
            response (dict): The API response containing movie results

        Returns:
            list -- List of Movie instances
        """

        results = response['results']
        movies = []
        for result in results:
            movies.append(
                Movie(
                    result['id'],
                    result['title'],
                    result['overview'],
                    TMDB.image_url + result['poster_path'],
                    result['release_date'],
                    None
                )
            )
        return movies

    def _convert_movie_detail(self, response):
        """Convert a movie API detail response to a Movie instance

        Arguments:
            response (dict): The API response containing movie results

        Returns:
            Movie -- Movie instance
        """

        youtube_url = None

        # find the trailer url in video results
        for video in response['videos']['results']:
            if(video['type'] == 'Trailer' and video['site'] == 'YouTube'):
                youtube_url = 'https://www.youtube.com/watch?v=' + video['key']

        return Movie(
            response['id'],
            response['title'],
            response['overview'],
            TMDB.image_url + response['poster_path'],
            response['release_date'],
            youtube_url
        )
