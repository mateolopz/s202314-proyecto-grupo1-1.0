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

@router.get("/data")
async def get_data():
    some_data = db.collection('Houses')
    docs = some_data.stream()
    lista = []
    for doc in docs:
        formattedData = doc.to_dict()
        lista.append(formattedData)
    return lista
      