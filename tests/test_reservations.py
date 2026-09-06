def test_create_reservations(client,create_equipment,header_user_2):
    response = client.post("/reservation/create",
                           json = {
                               "equipment_id":1,
                               "start_date":"2026-09-03T17:25:22.410Z",
                               "end_date": "2026-09-05T17:25:22.410Z"
                           },headers = header_user_2)
    assert response.status_code == 201

def test_equipment_none(client,header_user_2):
    response = client.post("/reservation/create",
                           json = {
                               "equipment_id":1,
                                "start_date":"2026-09-03T17:25:22.410Z",
                                "end_date": "2026-09-05T17:25:22.410Z",
                           },headers = header_user_2)
    assert response.status_code == 404

def test_equipment_owner_reservation(client,create_equipment,login_header):
    response = client.post("/reservation/create",
                           json = {
                                "equipment_id":1,
                                "start_date":"2026-09-03T17:25:22.410Z",
                                "end_date": "2026-09-05T17:25:22.410Z"
                           },headers = login_header)
    assert response.status_code == 403

def test_equipment_date_chk(client,create_equipment,header_user_2):
    response = client.post("reservation/create",
                           json = {
                                "equipment_id":1,
                                "start_date":"2026-09-03T17:25:22.410Z",
                                "end_date": "2026-09-02T17:25:22.410Z"
                                                      },headers=header_user_2)
    assert response.status_code == 403

def test_conflict_reservation(client,login_header_3,create_one_more_reservation,create_equipment,accept_reject):
    response = client.post("/reservation/create",
                           json = {
                               "equipment_id":1,
                               "start_date":"2026-09-04T17:25:22.410Z",
                               "end_date":"2026-09-06T17:25:22.410Z"
                           },headers = login_header_3)
    assert response.status_code == 409
                           
def test_my_reservation(client,create_one_more_reservation,header_user_2):
    response = client.get("/reservation/my",headers = header_user_2)
    assert response.status_code == 200

def test_owner_of_equipment(client,create_one_more_reservation,login_header):
    response = client.get("/reservation/owner",headers=login_header)
    assert response.status_code == 200

def test_return(client,header_user_2,create_one_more_reservation,accept_reject):
    response = client.patch("/reservation/1/return",
                            json = {
                                "status" : "completed"
                            },headers=header_user_2)
    assert response.status_code == 200
def test_return_nofound(client,header_user_2):
    response = client.patch("/reservation/1/return",
                            json = {
                                "status" : "completed"
                            },headers=header_user_2)
    assert response.status_code == 404
def test_return_wrong_borrower(client,accept_reject,login_header):
    response = client.patch("/reservation/1/return",
                            json = {
                                "status" : "completed"
                            },headers=login_header)
    assert response.status_code == 403

def test_return_wrong_status(client,accept_reject_2,header_user_2):
    response = client.patch("/reservation/1/return",
                          headers=header_user_2)
    assert response.status_code == 400

def test_cancel_reservation(client,pending_status,header_user_2):
    response = client.patch("/reservation/1/cancel"
                           
                            ,headers=header_user_2)
    assert response.status_code == 200

def test_cancel_no_reservation(client,header_user_2):
    response = client.patch("reservation/1/cancel",headers=header_user_2)
    assert response.status_code == 404

def test_accept_reject(client,login_header,create_one_more_reservation):
    response = client.patch("/reservation/1/status",
                            json ={
                                "status" : "accepted"
                            },headers=login_header)
    assert response.status_code == 200

def test_accept_reject_no_reservation(client,login_header):
    response = client.patch("/reservation/1/status",
                            json ={
                                "status" : "accepted"
                            },headers=login_header)
    assert response.status_code == 404

def test_no_other_status(client,login_header,create_one_more_reservation):
    response = client.patch("/reservation/1/status",
                            json ={
                                "status" : "pending"
                            },headers=login_header)
    assert response.status_code == 422

def test_available_equipment(client,create_equipment):
    response = client.get("/reservation/available")
    assert response.status_code == 200

def test_my_borrowed_reservations(client,create_one_more_reservation,header_user_2):
    response = client.get("/reservation/my",headers=header_user_2)
    assert response.status_code == 200

def test_owner_no_reservations(client,header_user_2):
    response = client.get("/reservation/owner",headers=header_user_2)
    
    
    assert response.status_code == 404

def test_owner_reservations(client,login_header,create_one_more_reservation):
    response = client.get("/reservation/owner",headers=login_header)
    
    
    assert response.status_code == 200

def test_reservation_details_owner(client,login_header,create_one_more_reservation):
    response = client.get("/reservation/1",headers=login_header)
    assert response.status_code == 200

def test_reservation_details_borrower(client,header_user_2,create_one_more_reservation):
    response = client.get("/reservation/1",headers=header_user_2)
    assert response.status_code == 200

def test_reservation_details_no_one(client,login_header_3,create_one_more_reservation):
    response = client.get("/reservation/1",headers=login_header_3)
    assert response.status_code == 403

def test_no_reservation_in_details(client,header_user_2):
    response = client.get("/reservation/1",headers=header_user_2)
    assert response.status_code == 404










