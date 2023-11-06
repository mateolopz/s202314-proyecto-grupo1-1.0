import uuid
from fastapi import APIRouter, Depends, Response, Header, Query
from fastapi.responses import JSONResponse
import src.logic.route as logic
import firebase_admin
from firebase_admin import credentials, firestore

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

@router.get("/users/{user_id}/houseliking")
async def get_user_houses(user_id: str):
    doc = db.collection('HouseLiking').document(user_id).get()
    if doc.exists:
        user_house_liking = doc.to_dict()

        query = db.collection('Houses')

        for field, value in user_house_liking.items():
            query = query.where(field, "==", value)
        query = query.limit(3)

        houses = []

        docs = query.get()
        for doc in docs:
            houses.append(doc.to_dict())

        return houses
    else:
        return []