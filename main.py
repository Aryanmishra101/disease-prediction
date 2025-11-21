from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import joblib
import numpy as np
from fastapi import Body
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(
    "mongodb+srv://aryanmishraa18_db_user:Peace%4001@cluster0.qigxmce.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    tls=True,
    tlsAllowInvalidCertificates=True
)


db = client["disease_prediction"]
collection = db["predictions"]



# load model
model = joblib.load("diabetes_best_model.pkl")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# JSON endpoint for fetch
@app.post("/predict")
async def predict(data: dict = Body(...)):
    values = [
        data["Pregnancies"],
        data["Glucose"],
        data["BloodPressure"],
        data["SkinThickness"],
        data["Insulin"],
        data["BMI"],
        data["DiabetesPedigreeFunction"],
        data["Age"]
    ]
    pred = model.predict([values])[0]
    return {"prediction": int(pred)}

@app.post("/predict")
async def predict(data: dict):
    values = [
        data["Pregnancies"],
        data["Glucose"],
        data["BloodPressure"],
        data["SkinThickness"],
        data["Insulin"],
        data["BMI"],
        data["DiabetesPedigreeFunction"],
        data["Age"]
    ]

    result = model.predict([values])[0]

    # Save record in MongoDB
    record = {
        "input_data": data,
        "prediction": int(result),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    collection.insert_one(record)

    return {"prediction": int(result)}

@app.get("/test_db")
def test_db():
    try:
        collection.insert_one({"test": "connection_ok"})
        return {"status": "Connected to MongoDB!"}
    except Exception as e:
        return {"status": "Failed", "error": str(e)}

record = {
    "input_data": data,
    "prediction": int(result),
    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

collection.insert_one(record)
    