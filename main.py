from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import pymongo
import sys
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from Functions import get_list, get_movie_details

# app initialisation
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["Top_Movies"]
collection = db["Movies"]
Bootstrap(app)


# Form Creation
class Edit_form(FlaskForm):
    rating = StringField('Your Ratings out of 10', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('done')


class Add_form(FlaskForm):
    movie_name = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


# route creations
@app.route("/")
def home():
    if "Movies" in db.list_collection_names() and len(list(collection.find({}))) != 0:
        all_movies = list(collection.find({}))
        all_movies = sorted(all_movies, key=lambda k: k['rating'], reverse=False)
        for i in range(len(all_movies)):
            all_movies[i]["ranking"] = len(all_movies) - i
        return render_template("index.html", all_movies=all_movies)
    else:
        all_movies = None
        return render_template("index.html", all_movies=all_movies)


@app.route("/edit", methods=["POST", "GET"])
def edit_details():
    if request.method == "GET":
        movie_title = request.args.get("movie_title")
        movie_selected = collection.find_one({"title": movie_title})
        my_form = Edit_form()
        return render_template("edit.html", movie_selected=movie_selected, form=my_form)
    else:
        new_rating = request.form["rating"]
        new_review = request.form["review"]
        movie_title = request.args.get("movie_title")
        collection.update_one({"title": movie_title}, {"$set": {"rating": new_rating, "review": new_review}})
        return redirect(url_for('home'))


@app.route("/delete", methods=["POST", "GET"])
def delete_movie():
    movie_title = request.args.get("movie_title")
    collection.delete_one({"title": movie_title})
    return redirect(url_for('home'))


@app.route("/add", methods=["POST", "GET"])
def add_movie():
    form = Add_form()
    if form.validate_on_submit():
        movie_name = request.form["movie_name"]
        movies_list = get_list(movie_name)
        return render_template("select.html", movies_list=movies_list)
    else:
        return render_template("add.html", form=form)


@app.route("/select", methods=["POST", "GET"])
def select_movie():
    movie_id_moviedb = request.args.get("movie_id")
    movie_details = get_movie_details(movie_id_moviedb)
    collection.insert_one(movie_details)
    movie_to_be_added = collection.find_one({"title": movie_details["title"]})
    movie_to_be_added = movie_to_be_added["title"]
    return redirect(url_for('edit_details', movie_title=movie_to_be_added))


if __name__ == '__main__':
    app.run(debug=True)
