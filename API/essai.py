from pydantic import BaseModel
import pandas as pd
from fastapi import FastAPI
from joblib import load
app = FastAPI()

with open("tree.joblib", "rb") as f:
    model = load(f)
    f.close()


class Car(BaseModel):
    marque: str
    modele: str
    date_fabrication: int
    kilometrage: int
    carrosserie: str
    code_postal: str
    energie: str
    emission: int
    consommation: float
    transmission: str
    portes: int
    sieges: int
    cv_fiscaux: int
    cv_reels: int

    class Config:
        schema_extra = {
            "example": {
                "marque": "fiat",
                "modele": "500",
                "date_fabrication": 2013,
                "kilometrage": 82100,
                "carrosserie": "berline",
                "code_postal": 87000,
                "energie": "essence",
                "emission": 92,
                "consommation": 4.0,
                "transmission": "manuelle",
                "portes": 2,
                "sieges": 4,
                "cv_fiscaux": 4,
                "cv_reels": 85
            }
        }

class Prediction(BaseModel):
    prix:int
    class Config:
        schema_extra = {
            "example": {
                "prix": "11290",
            }
        }

@app.get('/')
def welcome():
    """This api was made for scholar training and provide a prediction about second hand car price in France
    """
    return


@app.post('/prediction/',response_model=Prediction)
async def pred(data: Car):
    """
    Make a prediction
    """
    car = pd.DataFrame(data.dict(), index=[0])
    price = Prediction(**{"prix":model.predict(car)[0]})
    
    return price.dict()
