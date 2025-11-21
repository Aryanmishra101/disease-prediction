from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
import joblib
import numpy as np

# ----------------------------------------
# FASTAPI APP SETUP
# ----------------------------------------
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ----------------------------------------
# LOAD ML MODEL
# ----------------------------------------
model = joblib.load("diabetes_best_model.pkl")

# ----------------------------------------
# CONNECT TO MONGODB
# ----------------------------------------
client = MongoClient(
    "mongodb+srv://aryanmishraa18_db_user:Peace%4001@cluster0.qigxmce.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    tls=True,
    tlsAllowInvalidCertificates=True
)

db = client["diseaseDB"]
collection = db["predictions"]

# ----------------------------------------
# HOME PAGE (Frontend)
# ----------------------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ----------------------------------------
# PREDICTION API
# ----------------------------------------
@app.post("/predict")
async def predict(request: Request):
    data = await request.json()

    # Convert values to numpy array
    input_values = np.array(list(data.values())).reshape(1, -1)

    # ML prediction
    prediction = int(model.predict(input_values)[0])

    # Save to MongoDB
    collection.insert_one({
        "input_data": data,
        "prediction": prediction
    })

    return {"prediction": prediction}
