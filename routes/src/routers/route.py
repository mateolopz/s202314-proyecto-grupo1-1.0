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

@router.get("/stats/usersfilters")
async def get_user_filters_stats():
    doc = db.collection('Stats').document('UsersFilters').get()
    if doc.exists:
        user_filters_stats = doc.to_dict()
        return user_filters_stats
    else:
        return []

@router.get("/users/{user_id}/houseliking")
async def get_liking_houses_by_user(user_id: str):
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
    
@router.post("/houses/filtered")
async def get_houses_by_filters(request_data: dict):
    query = db.collection('Houses').get()

    filtered_houses = []

    for house in query:
        house = house.to_dict()
        match_times = 0
        atributes = 0
        for field, value in request_data.items():
            if(value != "" and value != 0):
                atributes+=1
                if(type(value)=='int' or type(value)=='float' or field=='rentPrice'):
                    lower_bound = float(value) * 0.9
                    upper_bound = float(value) * 1.1
                    if(float(house[field])>=lower_bound and float(house[field])<=upper_bound):
                        match_times+=1
                else:
                    if(value == house[field]):
                        match_times+=1
        if(match_times>=atributes*0.7):
            filtered_houses.append(house)

    return filtered_houses

@router.put("/stats/usersfilters")
async def get_houses_by_filters(times_data: dict):
    doc = db.collection('Stats').document('UsersFilters').get()
    user_filters_stats = doc.to_dict()
    for field, value in times_data.items():
        if field in user_filters_stats:
            if value in user_filters_stats[field]:
                user_filters_stats[field][value] += 1
            else:
                user_filters_stats[field][value] = 1
        
    db.collection('Stats').document('UsersFilters').set(user_filters_stats)

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