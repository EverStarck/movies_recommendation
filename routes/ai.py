from flask import jsonify, request
from . import routes
from lib import recommend


@routes.route("/recommend", methods=["GET"])
def recommends():
    try:
        movie = request.args.get("movie")
        only_recommended = request.args.get("recommended")
        movie = int(movie)
    except:
        return jsonify({"error": True, "message": "Movie not found."}), 400


    if only_recommended is not None:
        only_recommended = True

    res = recommend(movie, only_recommended)

    if res is None:
        return jsonify({"error":True, "message": "Movie not found."}), 400

    return jsonify({"error": False, "message": "Ok.", "data": res}), 200

