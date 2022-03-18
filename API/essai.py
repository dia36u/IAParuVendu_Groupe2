from fastapi import FastAPI
from matplotlib.pyplot import get

app = FastAPI()


@app.get("/")
async def get_Home():
    return {'message': "bienvenu sur la page de prediction"}, 200


@app.post("/prediction")
async def post_prediction(version: str,

                          marque: str,

                          modele: str,

                          date_fabrication: str,

                          kilometrage: str,

                          couleur: str,

                          carrosserie: str,

                          code_postal: str,

                          energie: str,

                          emission: str,

                          consommation: str,

                          transmission: str,

                          portes: str,

                          cv_fiscaux: str,

                          cv_reels: str,

                          prix_vente: str):
    return {"prix": 2300}
