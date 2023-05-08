from . import routes


@routes.route("/")
def index():
    return "<h1>:)</h1>"