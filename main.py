from fastapi import FastAPI, Request
import asyncpg
from asyncpg import Pool

app = FastAPI()

DATABASE_URL = "postgresql://postgres:1234@127.0.0.1:5432/fastapi"

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/gpt")
async def read_item():
    async with app.state.pool.acquire() as connection:
        query = "SELECT * FROM answers"
        result2 = await connection.fetch(query)
        return {"answers":result2}

@app.get("/gpt/{item_id}")
async def read_item(item_id: int, request: Request, q: str = None):
    async with app.state.pool.acquire() as connection:
        query = "SELECT answer FROM answers WHERE answer_id = $1"
        result = await connection.fetchval(query, item_id)
        return {"answer":result}
    

@app.on_event("startup")
async def startup():
    app.state.pool = await create_pool(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close()

async def create_pool(dsn: str) -> Pool:
    pool = await asyncpg.create_pool(dsn)
    print('PostgresDB Connection Made')
    return pool
