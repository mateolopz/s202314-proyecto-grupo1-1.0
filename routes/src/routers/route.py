import uuid
from fastapi import APIRouter, Depends, Response, Header, Query
from fastapi.responses import JSONResponse
import src.logic.route as logic
import firebase_admin
import json
from .processing import occupancy_rate, revenue
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter

router = APIRouter(
    prefix="/senehouse",
    tags=["senehouse"],
)

cred = credentials.Certificate("senehouse-keys.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@router.get("/ping")
def ping():
    return "pong"

@router.get("/houses")
async def get_houses():
    some_data = db.collection('Houses')
    docs = some_data.stream()
    lista = []
    for doc in docs:
        formattedData = doc.to_dict()
        lista.append(formattedData)
    return lista

@router.get("/users")
async def get_houses():
    some_data = db.collection('Users')
    docs = some_data.stream()
    lista = []
    for doc in docs:
        formattedData = doc.to_dict()
        lista.append(formattedData)
    return lista

@router.get("/searchs")
async def get_houses():
    some_data = db.collection('Searchs')
    docs = some_data.stream()
    lista = []
    for doc in docs:
        formattedData = doc.to_dict()
        lista.append(formattedData)
    return lista

@router.get("/houseliking")
async def get_houses():
    some_data = db.collection('HouseLiking')
    docs = some_data.stream()
    lista = []
    for doc in docs:
        formattedData = doc.to_dict()
        lista.append(formattedData)
    return lista

@router.get("/houses/{email}")
async def get_houses_by_user(email: str):
    houses = (db.collection('houses2')
              .where(filter=FieldFilter('idUser', '==', email))
                .stream())    
    lista = []
    for doc in houses:
        formattedData = doc.to_dict()
        lista.append(formattedData)

    rate = occupancy_rate(lista)
    revenue_map = revenue(lista)

    response_data = {
        "occupancyRate": rate,
        "revenue": revenue_map
    }
    response_json = json.dumps(response_data)
    return response_json