import random

from flask import Flask, render_template, jsonify, json

from helpers import SpotifyAPI

app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template("dashboard.html")


@app.route('/tracks/<genre>')
def get_tracks(genre):
    if not genre:
        return jsonify(code='error', msg="You should specify a genre")
    with open('C:/Users/ViraSoft/PycharmProjects/tracks/static/genres.json') as json_file:
        data = json.load(json_file)
    genre = genre.lower()
    if genre not in data:
        return jsonify(code='error', msg="Invalid Genre")
    artist = random.choice(data[genre])
    spotify = SpotifyAPI()
    artist_id = spotify.find_artist_id(genre, artist)
    top_ten_list = spotify.get_top_ten(artist_id)
    print(top_ten_list)
    return jsonify(code='ok', data=top_ten_list)


if __name__ == '__main__':
    app.run()
