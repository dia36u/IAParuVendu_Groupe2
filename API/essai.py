from fastapi import FastAPI
from matplotlib.pyplot import get

app = FastAPI()

donnees = {'voiture':
           [
               'citroen',
               'bmw',
               'mercedes', ]
           }


@app.get("/voitureSchema")
async def get_voitureSchema():
    return {'donnes': donnees}, 200
