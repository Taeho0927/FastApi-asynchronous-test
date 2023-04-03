from fastapi import FastAPI
import asyncpg
from asyncpg import Pool
from pydantic import BaseModel


class Question(BaseModel):
    question: str


app = FastAPI()

DATABASE_URL = "postgresql://postgres:1234@127.0.0.1:5432/ondo_lite_local"

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/gpt")
async def read_all_answer():
    async with app.state.pool.acquire() as connection:
        query = "SELECT * FROM datas"
        result = await connection.fetch(query)
        return result

@app.post("/gpt")
async def create_answer(q: Question):
    async with app.state.pool.acquire() as connection:
        query = "SELECT * FROM datas where id =1"
        result = await connection.fetch(query)
    response = q.question + "<의 답변입니다>"
    return response,result

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
