from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from db import pool, database

app = FastAPI(lifespan=pool)

class Customer(BaseModel):
    customer_id: str

@app.exception_handler(Exception)
async def exception_handler(req, exc):
    return JSONResponse(
        status_code=400,
        content={'message': 'Algo deu errado'}
    )

@app.post('/customers')
async def post(customer: Customer):
    customer_id = customer.customer_id

    query = """
        INSERT INTO customers (customer_id)
        VALUES (:customer_id)
        ON CONFLICT (customer_id) DO UPDATE SET date = now()
    """
    record = await database.execute(query, values={'customer_id': customer_id})
    print(record)

    return True