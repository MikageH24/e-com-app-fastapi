from fastapi import FastAPI
from app.routers import category, products, auth, permission, review
from .log import log_middleware

app = FastAPI()
app.middleware("http")(log_middleware)

@app.get('/')
async def welcome() -> dict:
    return {'message': 'My e-commerce app'}

app.include_router(category.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(permission.router)
app.include_router(review.router)

# uvicorn app.main:app --reload