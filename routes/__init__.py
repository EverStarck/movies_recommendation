from flask import Blueprint

routes = Blueprint("routes", __name__, url_prefix="/api")

from .index import *
from .ai import *