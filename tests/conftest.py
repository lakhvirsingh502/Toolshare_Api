import os
import pytest
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.database import Base,get_db
from fastapi.testclient import TestClient
from app.rate_limiter import rate_limiter 
from app.services.notifications import send_notification
from app.tasks import send_reservation_email

load_dotenv()


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(TEST_DATABASE_URL)
TestSessionlocal = sessionmaker(bind=engine)

def override_get_db():
    db = TestSessionlocal()
    try:
        yield db
    finally:
        db.close()

def override_redis():
    return None

def override_send_notification():
    return None

def override_send_reservation_email():
    return None

@pytest.fixture
def client():
    
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[rate_limiter] = override_redis
    
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def register_user(client):
    user_detail = client.post("/users/register",
                               json={
                                   "name":"Lakhvir",
                                   "email":"lakhvir@gmail.com",
                                   "password":"123456" 
                                     })
    return user_detail
    

@pytest.fixture
def login(client,register_user):
    response = client.post("/users/login",
                json={
                    "email":"lakhvir@gmail.com",
                    "password":"123456"
                }
                )
    return response
@pytest.fixture
def incorrect_login(client,register_user):
    response = client.post("/users/login",
                json={
                    "email":"lakhvir@gmail.com",
                    "password":"12345"
                }
                )
    return response

@pytest.fixture
def login_header(client,register_user):
    data = client.post("/users/login",
                json={
                    "email":"lakhvir@gmail.com",
                    "password":"123456"
                }

                )
    token1 = data.json()["Token"]
    return {
        "Authorization" : f"Bearer {token1}"
        }
@pytest.fixture
def create_equipment(client,login_header):
    response = client.post("/equipment/create",
                    json = {
                        "name" : "drill",
                        "description" : "good for heavy drilling",
                        "category" : "powertool",
                        "condition" : "very good"
                    },headers = login_header)
    return response
@pytest.fixture
def header_user_2(client):
     client.post("/users/register",
                json={
                    "name":"Krishna",
                    "email":"krish@gmail.com",
                    "password":"123456"
                })
     response = client.post("/users/login",
                            json = {
                                "email":"krish@gmail.com",
                                "password":"123456"
                            })
     data = response.json()["Token"]
     return{
         "Authorization":f"Bearer {data}"
     }
@pytest.fixture
def login_header_3(client):
    client.post("/users/register",
                json = {
                    "name":"vasudev",
                    "email":"vasudev@gmail.com",
                    "password":"123456"
                })
    response = client.post("/users/login",
                json = {
                    "email":"vasudev@gmail.com",
                    "password":"123456"
                })
    data = response.json()["Token"]
    return {
        "Authorization":f"Bearer {data}"
    }



@pytest.fixture
def create_one_more_reservation(client,header_user_2,create_equipment):
    client.post("/reservation/create",
                json={
                    "equipment_id":1,
                    "start_date":"2026-09-03T17:25:22.410Z",
                    "end_date":"2026-09-08T17:25:22.410Z"
                },headers = header_user_2)
@pytest.fixture
def accept_reject(client,create_one_more_reservation,create_equipment,login_header):
    client.patch("/reservation/1/status",
                 json = {
                     "status":"accepted"
                 },headers = login_header)
    
@pytest.fixture
def accept_reject_2(client,create_one_more_reservation,create_equipment,login_header):
    client.patch("/reservation/1/status",
                 json = {
                     "status":"rejected"
                 },headers = login_header)

@pytest.fixture
def pending_status(client,create_one_more_reservation,create_equipment,login_header):
    client.patch("/reservation/1/status",
                 json = {
                     "status":"pending"
                 },headers = login_header)
@pytest.fixture
def return_equipment(client,create_one_more_reservation,accept_reject,header_user_2):
    client.patch("/reservation/1/return",headers = header_user_2)

@pytest.fixture
def return_equipment_reject(client,create_one_more_reservation,accept_reject_2,header_user_2):
    client.patch("/reservation/1/return",headers = header_user_2)
    
@pytest.fixture
def create_review(client,create_one_more_reservation,header_user_2,return_equipment):
    response = client.post("/review/post",
                           json = {
                               "reservation_id":1,
                               "rating":5,
                               "comment":"Very good equipment"
                           },headers = header_user_2)





