from django.core.management.base import BaseCommand

from core.api_clients.tmdb_client import TMDBClient
from core.models import Movie, Genre, Crew, Picture, Watchlist, WatchlistHasMovie


class Command(BaseCommand):
    tmdb_client = TMDBClient()

    def handle(self, *args, **options):
        self.seed_movies()
        self.add_movies_to_watch_lists()
        self.stdout.write(self.style.SUCCESS(
            "Database seeded with fake data"
        ))

    def seed_movies(self):
        j_movies = self.tmdb_client.random_movies()
        for j_movie in j_movies:
            movie = Movie.from_json(j_movie)
            count = Movie.objects.filter(tmdb_id=movie.tmdb_id).count()
            if count == 0:
                movie.save()
                self.process_genres(j_movie, movie)
                self.process_credits(j_movie, movie)
                self.process_pictures(j_movie, movie)

    @staticmethod
    def add_movies_to_watch_lists():
        lists = Watchlist.objects.all()
        offset_index = 0

        for watchlist in lists:
            if offset_index == 3:
                offset_index = 0

            offset = 20 * offset_index
            movies = Movie.objects.filter(id__gt=offset)[:20]
            for movie in movies:
                has_movie = WatchlistHasMovie()
                has_movie.watchlist_id = watchlist.id
                has_movie.movie_id = movie.id
                has_movie.added_by_id = watchlist.owner().id
                has_movie.save()

            offset_index += 1

    @staticmethod
    def process_genres(j_movie, movie):
        for j_genre in j_movie['genres']:
            genre = Genre.from_json(j_genre)

            count = Genre.objects.filter(id=genre.id).count()
            if count == 0:
                genre.save()
                movie.genres.add(genre)
            else:
                genre = Genre.objects.filter(id=genre.id).first()
                movie.genres.add(genre)

    @staticmethod
    def process_credits(j_movie, movie):

        # Process cast
        for j_cast in j_movie['credits']['cast']:
            crew = Crew()
            crew.movie_id = movie.id
            crew.category_id = 2
            crew.name = j_cast['name']
            crew.character_name = j_cast['character']
            crew.picture_url = j_cast['profile_path']
            crew.save()

        # Process directors
        for j_crew in j_movie['credits']['crew']:
            if j_crew['job'] == 'Director':
                crew = Crew()
                crew.movie_id = movie.id
                crew.category_id = 1
                crew.name = j_crew['name']
                crew.picture_url = j_crew['profile_path']
                crew.save()

    @staticmethod
    def process_pictures(j_movie, movie):
        if 'backdrop_path' in j_movie and j_movie['backdrop_path'] != None:
            picture = Picture()
            picture.category_id = 2
            picture.movie_id = movie.id
            picture.url = j_movie['backdrop_path']
            picture.save()

        if 'poster_path' in j_movie and j_movie['poster_path'] != None:
            picture = Picture()
            picture.category_id = 1
            picture.movie_id = movie.id
            picture.url = j_movie['poster_path']
            picture.save()
