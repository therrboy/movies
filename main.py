from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired
import add_module

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie-server.db'
db = SQLAlchemy(app)
Bootstrap(app)


class Movies(
    db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False, default=1.0)
    ranking = db.Column(db.Integer, nullable=False, unique=True, default=1)
    review = db.Column(db.String, nullable=False, default="No comentada aun")
    img_url = db.Column(db.String, nullable=False)


class SelectMovie(FlaskForm):
    title = StringField(label='Movie Title', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class EditMovie(FlaskForm):
    rating = FloatField(label='Movie Rating 0/10.0', validators=[DataRequired()])
    ranking = IntegerField(label='Movie Ranking', validators=[DataRequired()])
    review = StringField(label='My Review', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class AddMovies(FlaskForm):
    title = StringField(label='Movie Title', validators=[DataRequired()])
    year = IntegerField(label='Year', validators=[DataRequired()])
    description = StringField(label='Description', validators=[DataRequired()])
    rating = FloatField(label='Rating', validators=[DataRequired()])
    ranking = IntegerField(label='Ranking', validators=[DataRequired()])
    review = StringField(label='Review', validators=[DataRequired()])
    img_url = StringField(label='Img Url', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@app.route("/")
def home():
    with app.app_context():
        all_movies = db.session.query(Movies).all()
    return render_template("index.html", movies=all_movies)


@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id):
    movie = db.session.get(Movies, id)
    form = EditMovie(obj=movie)
    if form.validate_on_submit():
        with app.app_context():
            movie_to_update = db.session.get(Movies, id)
            if form.rating.data:
                movie_to_update.rating = form.rating.data
            if form.ranking.data:
                movie_to_update.ranking = form.ranking.data
            if form.review.data:
                movie_to_update.review = form.review.data
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('edit.html', movie=movie, form=form)


@app.route("/select", methods=["POST", "GET"])
def select():
    form = SelectMovie()
    if form.validate_on_submit():
        new_movie = Movies(title=form.title.data)
        result = add_module.buscador(new_movie.title)
        return render_template('select.html', movies=result, form=form)
    return render_template('add.html', form=form)


@app.route("/add", methods=["POST", "GET"])
def add():
    id = request.form['id']
    pelicula_id = add_module.pelicula(id)
    with app.app_context():
        new_movie = Movies(title=pelicula_id["original_title"], year=pelicula_id["release_date"],
                           description=pelicula_id["overview"],
                           img_url="https://image.tmdb.org/t/p/w500" + pelicula_id["poster_path"])
        db.session.add(new_movie)
        return redirect(url_for('home'))


@app.route('/delete/<int:id>', methods=["POST", "GET"])
def delete(id):
    with app.app_context():
        movie_to_delete = db.session.query(Movies).get(id)
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
