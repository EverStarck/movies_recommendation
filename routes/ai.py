from flask import jsonify, request
from . import routes
from lib import recommend


@routes.route("/recommend", methods=["GET"])
def recommends():
    try:
        movie = request.args.get('movie')
    except:
        return jsonify({"error": True, "message": "Movie not found."}), 400

    res = recommend(movie)

    if res is None:
        return jsonify({"error":True, "message": "Movie not found."}), 400

    return jsonify({"error": False, "message": "Ok.", "data": res}), 200

