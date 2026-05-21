from fastapi import FastAPI, Body
from contextlib import asynccontextmanager
from clickhouse import CH
from scheme import ClickHouseModel
from json import loads
from datetime import datetime

ch = CH()

@asynccontextmanager
async def lifespan(app: FastAPI):
	ch.connect()
	yield
	ch.close()

app = FastAPI(lifespan=lifespan, title="Evo")


@app.get("/")
def read_root():
	return {"message": "Hello, Docker with FastAPI!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
	return {"item_id": item_id, "q": q}


# @app.post("/clickhouse")
# def clickhouse_query(query: ClickHouseModel):
# 	print(query)
# 	data = loads(query)
# 	return ch.query(data)

@app.post("/clickhouse")
def clickhouse_query(body: str = Body(..., media_type='text/plain')):
	data = loads(body)
	return ch.query(data)
