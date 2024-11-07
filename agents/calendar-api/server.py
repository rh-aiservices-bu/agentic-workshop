from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import configparser
import database_handler
import method
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

config = configparser.ConfigParser()
config.read('db.conf')
info = config['DEFAULT']

dbh = database_handler.DatabaseHandler(db_name=info['db_name'], check_same_thread=False)
m = method.Method(conf_file='db.conf')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Schedule(BaseModel):
    sid: str
    name: str
    content: str
    category: str
    level: int
    status: float
    creation_time: str
    start_time: str
    end_time: str

@app.get('/')
def index():
    return {'app_name': 'calendar'}

@app.get('/schedules')
def get_schedules():
    return dbh.fetch_data(info['table_name'])

@app.get('/schedules/{schedule_id}')
def get_schedule(schedule_id: str):
    schedule = m.get(dbh, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@app.post('/schedules')
def create_schedule(schedule: Schedule):
    if not m.post(dbh, schedule):
        raise HTTPException(status_code=400, detail="Schedule already exists or invalid data")
    return schedule

@app.put('/schedules/{schedule_id}')
def update_schedule(schedule_id: str, schedule: Schedule):
    if not m.update(dbh, schedule_id, schedule):
        raise HTTPException(status_code=404, detail="Schedule not found or invalid data")
    return schedule

@app.delete('/schedules/{schedule_id}')
def delete_schedule(schedule_id: str):
    if not m.delete(dbh, schedule_id):
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "Schedule deleted successfully"}
