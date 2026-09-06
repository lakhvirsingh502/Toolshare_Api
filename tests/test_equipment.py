def test_create_equipment(create_equipment):
    
    response = create_equipment
    
    
    assert response.status_code == 201

def test_get_all_equipment(client,create_equipment):
    response = client.get("equipment/all")
    assert response.status_code == 200
               
def test_get_by_id_equipment(client,create_equipment):
    response = client.get("equipment/1")
    assert response.status_code == 200

def test_get_by_id_equipment_none(client):
    response = client.get("/equipment/1")
    assert response.status_code == 404

def test_update_equipment(client,create_equipment,login_header):
    response = client.patch("/equipment/update/1",
                            json = {
                                "description":"Tool is for heavyduty use only.",
                                
                                
                            },headers = login_header)
    assert response.status_code == 200

def test_update_none_equipment(client,login_header):
    response = client.patch("/equipment/update/1", 
                            json = {
                                "description":"ok"
                            },headers = login_header)
    assert response.status_code == 404

def test_update_owner_test_equipment(client,header_user_2,create_equipment):
    response = client.patch("/equipment/update/1",
                            json = {
                                "description" : "very nice"
                            },headers = header_user_2)
    assert response.status_code == 403

def test_delete_equipment(client,create_equipment,login_header):
    response = client.delete("equipment/1",headers=login_header)
    assert response.status_code == 200

def test_delete_none_equipment(client,login_header):
    response = client.delete("equipment/1",headers=login_header)
    assert response.status_code == 404

def test_delete_owner_equipment(client,create_equipment,header_user_2):
    response = client.delete("/equipment/1",headers=header_user_2)
    assert response.status_code == 403

def test_get_all_equipments(client,create_equipment,login_header):
    response = client.get("/equipment/my",headers = login_header)
    assert response.status_code == 200

