from distutils.log import debug
from traceback import print_exc
from turtle import pd
from flask import Flask
from flask.views import MethodView
import marshmallow as ma
from flask_rest_api import Api, Blueprint, abort
from pip import main


app = Flask('My API')
app.config['OPENAPI_VERSION'] = '3.0.2'
api = Api(app)


class VoitureSchema(ma.Schema):
    marque = ma.fields.String()
    modele = ma.fields.String()
    prix = ma.fields.String()


class PredictionPrixSchema(ma.Schema):
    prix = ma.fields.Int()


blp = Blueprint(
    'voiture', 'prediction', url_prefix='/carprediction',
    description="prediction vente voiture d'ocasion"
)


@blp.route('/')
class Prediction(MethodView):
    @blp.response(PredictionPrixSchema(many=True))
    def get(self):
        print("bonjour")
        return "bonjour"


api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(debug=True)
