
import requests

def test_get_200_status_code():

     response = requests.get("http://localhost:5000/api/users?n=10")
     assert response.status_code == 200

     assert response.headers["Content-Type"] == "application/json"

def test_get_good_number_users():

     response = requests.get("http://localhost:5000/api/users?n=10")
     assert response.status_code == 200

     assert len(response.json()) == 10

     response = requests.get("http://localhost:5000/api/users?n=23")
     assert response.status_code == 200

     assert len(response.json()) == 23

def test_get_all_fields():

     response = requests.get("http://localhost:5000/api/users?n=10")
     assert response.status_code == 200

     users = response.json()

     user = users[0]

     if "age" not in user or user["age"] == "" or type(user["age"]) != int:
          assert False

     if "cellphone" not in user or user["cellphone"] == "":
          assert False

     if "country" not in user or user["country"] != "France":
          assert False

     if "email" not in user or user["email"] == "":
          assert False

     if "firstName" not in user or user["firstName"] == "":
          assert False

     if "gender" not in user or user["gender"] == "":
          assert False

     if "id" not in user or user["id"] == "" or type(user["id"]) != int:
          assert False
     
     if "lastName" not in user or user["lastName"] == "":
          assert False

     if "phone" not in user or user["phone"] == "":
          assert False

     if "uuid" not in user or user["uuid"] == "":
          assert False

     if "city" not in user or user["city"] == "" or len(user["city"]) != 4:
          assert False

     if "region" not in user or user["region"] == "" or len(user["region"]) != 2:
          assert False

     assert True
