 
def test_register(register_user):
    response = register_user

          
    assert response.status_code == 201

def test_login(login):
    response = login
    assert response.status_code == 200

def test_incorrect_login_password(incorrect_login):
    response = incorrect_login

    assert response.status_code == 401