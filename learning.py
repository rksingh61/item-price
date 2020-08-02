from flask import Blueprint

learning_xblueprint = Blueprint('learning', __name__)

@learning_xblueprint.route('/<string:name>')
def home(name):
    return(f"Hello, {name} World!")


