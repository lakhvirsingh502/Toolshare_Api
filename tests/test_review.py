def test_create_review(client,create_one_more_reservation,header_user_2,return_equipment):
    response = client.post("/review/post",
                           json = {
                               "reservation_id":1,
                               "rating":5,
                               "comment":"Very good equipment"
                           },headers = header_user_2)
    assert response.status_code == 200

def test_reservation_none(client,header_user_2):
    response = client.post("/review/post",
                    json = {
                            "reservation_id":1,
                            "rating":5,
                            "comment":"Very good equipment"
                        },headers = header_user_2)
    assert response.status_code == 404

def test_reservation_no_borrower(client,login_header_3,create_one_more_reservation):
    response = client.post("/review/post",
                    json = {
                            "reservation_id":1,
                            "rating":5,
                            "comment":"Very good equipment"
                        },headers = login_header_3)
    assert response.status_code == 403

def test_reservation_complete_status(client,accept_reject_2,header_user_2):
    response = client.post("/review/post",
                           json = {
                               "reservation_id":1,
                               "rating":5,
                               "comment":"good"
                           },headers=header_user_2)
    assert response.status_code == 409

def test_equipment_reviews(client,create_review,header_user_2):
    response = client.get("/review/equipment/1")
    assert response.status_code == 200

def test_my_reviews(client,create_review,login_header):
    response = client.get("review/my",headers=login_header)
    assert response.status_code == 404

def test_my_reviews(client,create_review,header_user_2):
    response = client.get("review/my",headers=header_user_2)
    assert response.status_code == 200

def test_delete_reviews(client,create_review,header_user_2):
    response = client.delete("review/delete/1",headers=header_user_2)
    assert response.status_code == 200

def test_delete_no_review(client,header_user_2):
    response = client.delete("/review/delete/1",headers=header_user_2)
    assert response.status_code == 404

def test_delete_wrong_user(client,create_review,login_header):
    response = client.delete("/review/delete/1",headers=login_header)
    assert response.status_code == 403

def test_update_review(client,create_review,header_user_2):
    response = client.patch("/review/update/1",
                            json = {
                                "comment":"very nice"
                            },headers = header_user_2)
    assert response.status_code == 200

def test_update_no_review(client,header_user_2):
    response = client.patch("/review/update/1",
                            json = {
                                "comment":"yes"
                            },headers = header_user_2)
    assert response.status_code == 404

def test_update_wrong_user(client,create_review,login_header):
    response = client.patch("review/update/1",
                            json = {
                                "comment":"yo"
                            },headers = login_header)
    assert response.status_code == 403