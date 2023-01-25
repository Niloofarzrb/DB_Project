from typing import List
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import sqlalchemy as db
import warnings

warnings.filterwarnings("ignore")


class ResponseModel(BaseModel):
    result: List
    result_count: int


app = FastAPI(title="DB_Project")

engine = db.create_engine('mysql+pymysql://root:8676299@localhost:3306/DB_0101?charset=utf8mb4')
connection = engine.connect()

IS_LOGGED_IN = False
IS_ADMIN = False


@app.post("/login", response_model=ResponseModel)
def login(username, password):
    query = db.text('SELECT * FROM user WHERE username = :username AND password = :password')
    raw_result = connection.execute(query, username=username, password=password)
    result = raw_result.fetchall()
    if len(result) == 1:
        global IS_LOGGED_IN
        IS_LOGGED_IN = True
        if result[0][2] == 'admin':
            global IS_ADMIN
            IS_ADMIN = True

        result = ['You are logged in!']
    else:
        result = ['Wrong username or password! Please try again.']

    return {'result': result, 'result_count': len(result)}


@app.get("/")
async def root():
    return {"message": "The webserver is running..."}


@app.get("/products", response_model=ResponseModel)
async def get_products():
    if IS_LOGGED_IN:
        query = db.text('SELECT idproduct, color, available, price, name, model, ph_date FROM product')
        raw_result = connection.execute(query)
        result = raw_result.fetchall()
    else:
        result = ['You are not logged in! Please login first!']
    return {'result': result, 'result_count': len(result)}


uvicorn.run(app)
