import uuid
from fastapi import APIRouter, Depends, Response, Header, Query
from fastapi.responses import JSONResponse
import src.logic.route as logic
import firebase_admin
import json
from .processing import occupancy_rate, revenue, calculate_distance
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter

router = APIRouter(
    prefix="/senehouse",
    tags=["senehouse"],
)

cred = credentials.Certificate("./senehouse-keys.json")
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
        formattedData['id'] = doc.id  
        lista.append(formattedData)
    return lista


@router.get("/users")
async def get_houses():
    some_data = db.collection('Users')
    docs = some_data.stream()
    lista = []
    for doc in docs:
        formattedData = doc.to_dict()
        formattedData['id'] = doc.id
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
        formattedData['id'] = doc.id  
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
    
@router.get("/stats/housesfilters")
async def get_user_filters_stats():
    doc = db.collection('FilterHouse').document('snF8sl1hqZpisoFQGXF7').get()
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
            formattedData = doc.to_dict()
            formattedData['id'] = doc.id  
            houses.append(formattedData)

        return houses
    else:
        return []


@router.get("/nearestoffers")
async def get_nearest_offers(latitude: float, longitude: float, maxDistance: int):
    data = db.collection('Houses')
    docs = data.stream()
    lista = []
    for doc in docs:
        formattedData = doc.to_dict()
        formattedData['id'] = doc.id  
        lista.append(formattedData)
    result = calculate_distance(latitude, longitude, lista, maxDistance)
    #response_json = json.dumps(result)
    return result

@router.post("/houses/filtered")
async def get_houses_by_filters(request_data: dict):
    query = db.collection('Houses').get()

    filtered_houses = []

    for doc in query:
        house = doc.to_dict()
        house['id'] = doc.id  
        
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
        if(match_times>=atributes*0.5):
            filtered_houses.append(house)

    return filtered_houses

@router.post("/users/ubication")
async def get_documents_within_radius(request_data:dict):

    users = []
    radius_in_degrees = 20
    longitude=request_data["longitude"]
    latitude=request_data["latitude"]
    min_lat = latitude - radius_in_degrees
    max_lat = latitude + radius_in_degrees
    min_lon = longitude - radius_in_degrees
    max_lon = longitude + radius_in_degrees

    users_collection = firestore.client().collection('Users')

    query = users_collection.where('latitude', '>=', min_lat).where('latitude', '<=', max_lat).get()

    for doc in query:
        formattedData = doc.to_dict()
        if min_lon <= formattedData["longitude"] <= max_lon:
            formattedData['id'] = doc.id
            users.append(formattedData)
            
    return users

@router.post("/users/filtered")
async def get_users_by_filters(request_data: dict):
    usuarios=[]
    query = db.collection('Users')
    pet_preference = request_data["likes_pet"]
    introverted_preference = request_data["personality"]
    cleaning_frequency = request_data["clean"]
    vape_preference = request_data["vape"]
    smoke_preference = request_data["smoke"]
    work_from_home_preference = request_data["work_home"]
    sleep_time = request_data["sleep_time"]
    external_people_frequency = request_data["bring_people"]
    city = request_data["city"]
    neighborhood = request_data["neighborhood"]
    
    if external_people_frequency is not None:
        query = query.where("bring_people", "==", external_people_frequency)
    if sleep_time is not None:
        query = query.where("sleep", "==", sleep_time)
    if smoke_preference is not None:
        query = query.where("smoke", "==", smoke_preference)
    if vape_preference is not None:
        query = query.where("vape", "==", vape_preference)
    if cleaning_frequency is not None:
        query = query.where("clean", "==", cleaning_frequency)
    if introverted_preference is not None:
        query = query.where("personality", "==", introverted_preference)
    if pet_preference is not None:
        query = query.where("likes_pets", "==", pet_preference)
    if city is not None:
        query = query.where("city", "==", city)
    if neighborhood is not None:
        query = query.where("locality", "==", neighborhood)

    query_snapshot = query.get()

    for doc in query_snapshot:
        formattedData = doc.to_dict()
        formattedData['id'] = doc.id
        usuarios.append(formattedData)
    return usuarios

@router.put("/stats/usersfilters")
async def put_user_filters_stats(times_data: dict):
    doc = db.collection('Stats').document('UsersFilters').get()
    user_filters_stats = doc.to_dict()
    for field, value in times_data.items():
        if field in user_filters_stats and value is not None:
            if value in user_filters_stats[field]:
                user_filters_stats[field][value] += 1
            else:
                user_filters_stats[field][value] = 1
        
    db.collection('Stats').document('UsersFilters').set(user_filters_stats)

@router.get("/houses/{id}")
async def get_houses_by_user(id: str):
    houses = (db.collection('Houses')
              .where(filter=FieldFilter('idUser', '==', id))
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

@router.get("/reviews/{house_id}")
async def get_reviews_by_house(house_id: str, skip: int = Query(0, ge=0), limit: int = Query(5, le=50)):

    # Ajustar la consulta para incluir paginación
    doc = db.collection('Reviews').where('houseId', '==', house_id).limit(limit).offset(skip).stream()

    lista = []
    for reg in doc:
        formattedData = reg.to_dict()
        formattedData['id'] = reg.id
        lista.append(formattedData)
    return lista

@router.get("/reviews/user/{user_id}")
async def get_reviews_by_user(user_id: str, skip: int = Query(0, ge=0), limit: int = Query(5, le=50)):

    # Ajustar la consulta para incluir paginación
    doc = db.collection('Reviews').where('userId', '==', user_id).limit(limit).offset(skip).stream()

    lista = []
    for reg in doc:
        formattedData = reg.to_dict()
        formattedData['id'] = reg.id
        lista.append(formattedData)
    return lista

@router.post("/reviews")
async def post_reviews(review: dict):
    db.collection('Reviews').add(review)
    return {"message": "Review added successfully"}

@router.put("/houses/{house_id}")
async def update_rating(house_id: str):
    doc = db.collection('Houses').document(house_id).get()
    house = doc.to_dict()
    rating = db.collection('Reviews').where(filter=FieldFilter('houseId', '==', house_id)).get()

    if (house is None):
        return {"message": "House not found", "raiting": 0}
    sum = 0
    count = 0
    for reg in rating:
        formattedData = reg.to_dict()
        sum += formattedData['rating']
        count += 1

    if (count == 0):
        return {"message": "No reviews for this house", "raiting": house['rating']}
    raiting = sum/count
    house['rating'] = raiting
    db.collection('Houses').document(house_id).set(house)
    return {"message": "Rating updated successfully", "raiting": raiting}


@router.get("/best/houses")
async def get_best_houses():
    houses_collection = db.collection('Houses')
    stats_collection = db.collection('Stats').document('appartmentsViewCount').get().to_dict()

    # Obtener todos los documentos ordenados por rating en orden descendente
    docs = houses_collection.order_by('rating', direction=firestore.Query.DESCENDING).stream()
    lista = []
    count = 0
    print(stats_collection)
    for doc in docs:
        house_data = doc.to_dict()
        house_id = doc.id

        # Obtener el número de vistas desde la colección 'Stats'
        views_count = stats_collection.get(house_id, 0)  # Si no hay vistas, establecer en 0

        # Calcular la suma ponderada (70% rating, 30% número de vistas)
        weighted_sum = 0.7 * house_data.get('rating', 0) + 0.3 * views_count

        # Añadir el valor ponderado al diccionario de datos
        house_data['weighted_sum'] = weighted_sum

        # Añadir el id del documento al diccionario de datos
        house_data['id'] = house_id

        lista.append(house_data)
        count += 1

        if count >= 5:
            break

    # Ordenar la lista por la suma ponderada en orden descendente
    lista = sorted(lista, key=lambda x: x['weighted_sum'], reverse=True)

    return lista


@router.get("/best/users")
async def get_best_users():
    some_data = db.collection('Users')
    
    docs = some_data.order_by('stars', direction=firestore.Query.DESCENDING).stream()
    
    lista = []
    count = 0
    
    for doc in docs:
        formattedData = doc.to_dict()
        formattedData['id'] = doc.id  
        lista.append(formattedData)
        count += 1
        
        if count >= 5:
            break
    
    return lista

@router.post("/houses")
async def post_house(house: dict):
    if 'id' in house:
        del house['id']
    db.collection('Houses').add(house)
    return {"message": "House added successfully"}

@router.put("/houses/{house_id}/views")
async def update_appartment_views(house_id: str):
    doc = db.collection('Stats').document('appartmentsViewCount').get()
    appartment_views = doc.to_dict()
    if house_id in appartment_views:
        appartment_views[house_id] += 1
    else:
        appartment_views[house_id] = 1
        
    db.collection('Stats').document('appartmentsViewCount').set(appartment_views)

@router.get("/bestdescriptions")
async def get_best_descriptions():
    descriptions = []

    # Retrieve appartment views document
    doc = db.collection('Stats').document('appartmentsViewCount').get()

    # Check if the document exists
    if doc.exists:
        appartment_views = doc.to_dict()

        # Sort appartment views
        sorted_appartments = sorted(appartment_views.items(), key=lambda x: x[1], reverse=True)

        # Get top 3 apartments
        top_3_appartments = sorted_appartments[:3]

        # Retrieve descriptions for top 3 apartments
        for appartment in top_3_appartments:
            house = db.collection('Houses').document(appartment[0]).get()

            # Check if the house document exists
            if house.exists:
                house_data = house.to_dict()

                # Check if "description" key exists in house_data
                if "description" in house_data:
                    descriptions.append(house_data["description"])

    return descriptions
