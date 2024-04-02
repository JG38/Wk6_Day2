from flask_smorest import Blueprint

bp = Blueprint('cars', __name__, description= "Routes for cars")

from . import routes