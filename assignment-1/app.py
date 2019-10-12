from flask import Flask, render_template, request, jsonify

import search


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/query", methods = ["POST"])
def query():
    query = request.form["query"]
    songs = search.search_query(query)
    
    return jsonify(songs)


if __name__ == "__main__":

    app.secret_key = "whatever"
    app.run(debug = True)
