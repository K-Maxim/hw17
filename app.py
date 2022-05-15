from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


class Movie(db.Model):
    """
    СОЗДАНИЕ ТАБЛИЦЫ MOVIE
    """
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(String(255))
    trailer = Column(String(255))
    year = Column(Integer)
    rating = Column(Float)
    genre_id = Column(Integer, ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = Column(Integer, ForeignKey("director.id"))
    director = db.relationship("Director")


class MoviesSchema(Schema):
    """
    ДЛЯ СЕРИАЛИЗАЦИИ
    """
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class Director(db.Model):
    """
    СОЗДАНИЕ ТАБЛИЦЫ DIRECTOR
    """
    __tablename__ = 'director'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class DirectorsSchema(Schema):
    """
    ДЛЯ СЕРИАЛИЗАЦИИ
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()


class Genre(db.Model):
    """
    СОЗДАНИЕ ТАБЛИЦЫ GENRE
    """
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class GenresSchema(Schema):
    """
    ДЛЯ СЕРИАЛИЗАЦИИ
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        try:
            director_id = request.args.get('director_id', type=int)
            genre_id = request.args.get('genre_id', type=int)
            movies_schema = MoviesSchema(many=True)
            movies = Movie.query
            if director_id:
                movies = movies.filter(Movie.director_id == director_id)
            if genre_id:
                movies = movies.filter(Movie.genre_id == genre_id)
            movies = movies.all()
            return movies_schema.dump(movies), 200
        except Exception:
            return '', 404

    def post(self):
        try:
            movie_schema = MoviesSchema()
            post_request = request.json
            movie = Movie(**post_request)
            with db.session.begin():
                db.session.add(movie)
            return movie_schema.dump(movie), 200
        except Exception:
            return '', 404


@movie_ns.route('/<int:mid>')
class MoviesView(Resource):
    def get(self, mid):
        try:
            movie_schema = MoviesSchema()
            one_movie = Movie.query.get(mid)
            return movie_schema.dump(one_movie), 200
        except Exception:
            return '', 404

    def put(self, mid):
        movie = Movie.query.get(mid)
        movie_schema = MoviesSchema()
        try:
            put_request = request.json
            movie.title = put_request.get("title")
            movie.description = put_request.get("description")
            movie.trailer = put_request.get("trailer")
            movie.year = put_request.get("year")
            movie.rating = put_request.get("rating")
            movie.genre_id = put_request.get("genre_id")
            movie.director_id = put_request.get("director_id")

            db.session.add(movie)
            db.session.commit()

            return movie_schema.dump(movie), 204
        except Exception:
            return '', 404

    def patch(self, mid):
        movie = Movie.query.get(mid)
        # ХОТЕЛ ПОПРОБОВАТЬ СДЕЛАТЬ ЧЕРЕЗ ЦИКЛ
        # movies_fields_list_str = ["title", "description", "trailer", "year", "rating", "genre_id", "director_id"]
        # movies_fields = [movie.title, movie.description, movie.trailer, movie.year, movie.rating, movie.genre_id,
        #                  movie.director_id]

        patch_request = request.json
        movie_schema = MoviesSchema()
        # for i in range(len(movies_fields_list_str)):
        #     if movies_fields_list_str[i] in patch_request:
        #         movies_fields[i] = patch_request.get(movies_fields_list_str[i])
        # db.session.add(movie)
        # db.session.commit()
        if 'title' in patch_request:
            movie.title = patch_request.get('title')
        if 'description' in patch_request:
            movie.title = patch_request.get('description')
        if 'trailer' in patch_request:
            movie.title = patch_request.get('trailer')
        if 'year' in patch_request:
            movie.title = patch_request.get('year')
        if 'rating' in patch_request:
            movie.title = patch_request.get('rating')
        if 'genre_id' in patch_request:
            movie.title = patch_request.get('genre_id')
        if 'genre_id' in patch_request:
            movie.title = patch_request.get('genre_id')
        db.session.add(movie)
        db.session.commit()
        return movie_schema.dump(movie), 204

    def delete(self, mid):
        delete_movie = Movie.query.get(mid)
        try:
            db.session.delete(delete_movie)
            db.session.commit()
            return '', 204
        except Exception:
            return '', 404



@director_ns.route('/')
class DirectorView(Resource):
    def get(self):
        try:
            directors = Director.query.all()
            directors_schema = DirectorsSchema(many=True)
            return directors_schema.dump(directors), 200
        except Exception:
            return '', 404

    def post(self):
        try:
            director_schema = DirectorsSchema()
            post_request = request.json
            director = Director(**post_request)
            db.session.add(director)
            db.session.commit()
            return director_schema.dump(director), 200
        except Exception:
            return '', 404


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        try:
            director_schema = DirectorsSchema()
            director = Director.query.get(did)
            return director_schema.dump(director), 200
        except Exception:
            return '', 404

    def put(self, did):
        try:
            director_schema = DirectorsSchema()
            director = Director.query.get(did)
            put_request = request.json
            director.name = put_request.get('name')
            db.session.add(director)
            db.session.commit()
            return director_schema.dump(director), 204
        except Exception:
            return '', 404

    def delete(self, did):
        director = Director.query.get(did)
        try:
            db.session.delete(director)
            db.session.commit()
            return '', 204
        except Exception:
            return '', 404


@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        try:
            genres_schema = GenresSchema(many=True)
            genres = Genre.query.all()
            return genres_schema.dump(genres), 200
        except Exception:
            return '', 404

    def post(self):
        try:
            genre_schema = GenresSchema()
            post_request = request.json
            genre = Genre(**post_request)
            db.session.add(genre)
            db.session.commit()
            return genre_schema.dump(genre), 200
        except Exception:
            return '', 404


@genre_ns.route('/<int:gid>')
class GenresView(Resource):
    def get(self, gid):
        try:
            genre_schema = GenresSchema()
            genre = Genre.query.get(gid)
            return genre_schema.dump(genre), 200
        except Exception:
            return '', 404

    def put(self, gid):
        try:
            genre_schema = DirectorsSchema()
            genre = Genre.query.get(gid)
            put_request = request.json
            genre.name = put_request.get('name')
            db.session.add(genre)
            db.session.commit()
            return genre_schema.dump(genre), 204
        except Exception:
            return '', 404

    def delete(self, gid):
        try:
            genre = Genre.query.get(gid)
            db.session.delete(genre)
            db.session.commit()
            return '', 204
        except Exception:
            return '', 404


if __name__ == '__main__':
    app.run(debug=True)
