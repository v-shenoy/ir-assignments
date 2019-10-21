''' Module responsible for running the Flask app. '''

from flask import Flask, render_template, request, jsonify

import search


app = Flask(__name__)

@app.route("/")
def index():
    ''' Render the template for the home-page. '''

    return render_template("index.html")


@app.route("/query", methods = ["POST"])
def query():
    ''' Process the POST request with the search query. '''

    query = request.form["query"]
    songs = search.search_query(query)
    
    return jsonify(songs)


if __name__ == "__main__":
    ''' Start flask app. '''
    
    app.secret_key = "whatever"
    app.run(debug = True)
