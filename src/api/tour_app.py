from typing import List
import uuid
from fastapi import FastAPI, Request
import pymongo
from pydantic import BaseModel
import uvicorn



client=pymongo.MongoClient("mongodb+srv://gayathri:Sairambaba@cluster1.davwpcs.mongodb.net/?retryWrites=true&w=majority")
db=client['suriya_db']



def get_Collection():
    return db['tour_registry']

app=FastAPI()

class Tour(BaseModel):
    tour_id:int
    place:str
    country:str
    is_visa_needed:bool
    budget:float


class TourList(BaseModel):
    data: List [ Tour ]


def tour_list_serialiazer(tour_list):
    return [tour.dict() for tour in tour_list]

@app.get('/api', tags=['Tour Registry'])
def index():
    try:
        col = get_Collection()
        resp = list(col.find({},{"_id":0}))
        return {"data": resp}
    except Exception as e:
        print(e)
        return {"error":str(e)}

@app.get('/api/get_tour_by_place', tags=['Tour Registry'])
def get_tour_by_place(place):
    try:
        col = get_Collection()
        resp = list(col.find({"place": place},{"_id":0}))
        return {"data": resp}
    except Exception as e:
        print(e)
        return {"error":str(e)}

@app.post('/api/add_tour', tags=['Tour Registry'])
def add_tour(data: Tour):
    try:
        col = get_Collection()
        col.insert_one(data.dict())
        return {"status": "success"}
    except Exception as e:
        print(e)
        return {"error":str(e)}


@app.post('/api/add_tour_list', tags=['Tour Registry'])
def add_tour_list(request : TourList):
    try:
        col = get_Collection()
        tour_list = tour_list_serialiazer(request.data)
        print(tour_list)
        print(type(tour_list))
        col.insert_many(tour_list)
        return {"status": "success"}
    except Exception as e:
        print(e)
        return {"error":str(e)}


@app.put('/api/update_tour_by_place', tags=['Tour Registry'])
def update_tour_by_place(place: str, data: Tour):
    try:
        col = get_Collection()
        col.update_one({"place":place}, {"$set": data.dict()})
        return {"status": "success"}
    except Exception as e:
        print(e)
        return {"error":str(e)}


@app.delete('/api/delete_tour_by_place', tags=['Tour Registry'])
def delete_tour_by_place(place: str):
    try:
        col = get_Collection()
        col.delete_one({"place":place})
        return {"status": "success"}
    except Exception as e:
        print(e)
        return {"error":str(e)}


if __name__=='__main__':
    uvicorn.run("tour_app:app",reload=True,access_log=False)