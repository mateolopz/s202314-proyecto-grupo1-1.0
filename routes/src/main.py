from fastapi import FastAPI
from src.routers import route
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return Response(status_code=400)


app.include_router(route.router)
