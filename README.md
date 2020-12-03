# Random French User Generator

## Version

v0.5

## Install

```
sudo pip install Flask Werkzeug PyYAML numpy markdown
```

### Optional for tests

```
sudo pip install pytest
```

## Run

```
./run.sh
```

## Tests

```
./test.sh
```

## Usage

0. With URL: <a target="_blank" href="http://localhost:5000/api/users?n=10">link</a>

1. With curl:<br/>
    ```curl -i http://localhost:5000/api/users?n=10```


2. With AJAX:<br/>
```javascript
  function generateUsers(n) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) { 
          console.log(this.responseText);
      }
    };
    xhttp.open("GET", "http://localhost:5000/api/users?n="+n, true);
    xhttp.send();
  }
  
  generateUsers(10);
```

3. With Python:<br/>
```Python
import requests

response = requests.get("http://localhost:5000/api/users?n=10")
if response.status_code == 200:
  print(response.json())
```

## Parameters

1. **n** (int) : The number of users generate.

2. **gender** (string) : If you want specific gender (other gender are accepted).
<br/> If not use the result it's a random choice beetween "homme" and "femme". 

3. **firstname** (string): If you want specific firstname.

4. **lastname** (string): If you want specific lastname.

5. **age** (int) : The age of users. We accept multiple value.

6. **age[]** (array) : The age range for users with min & max value in array.

7. **region** (int||string): If you want specific region. Id or name is accepted.

8. **email** (string): If you want specific email host.

9. **familysituation** (string): If you want specific family situation (code or value accepted).


## Output exemple

```
[
  {
    "age": 52, 
    "cellphone": "07-06-98-48-08", 
    "city": {
      "INSEE": "31193", 
      "id": "fousseret", 
      "name": "Le Fousseret", 
      "postalcode": "31430"
    }, 
    "country": "France", 
    "email": "charly.bouvier@sfr.fr", 
    "family": {
      "children": 1, 
      "situation": {
        "code": "V", 
        "value": "veuf"
      }
    }, 
    "firstName": "Charly", 
    "gender": "homme", 
    "id": 9, 
    "lastName": "Bouvier", 
    "phone": "05-82-60-11-02", 
    "region": {
      "id": "31", 
      "name": "Haute-Garonne"
    }, 
    "uuid": "19545001-1e92-4abb-8723-dd5541a694c3"
  }
]
```

## Other routes

1. All male first name: <br/>
    ```/api/male/firstname```

2. All female first name: <br/>
    ```/api/female/firstname```

3. All female first name: <br/>
    ```/api/lastname```

4. All regions: <br/>
    ```/api/regions```

5. All cities: <br/>
    ```/api/cities```<br/>
    
    With department id : ```/api/cities?dep=30```

6. All family situation: <br/>
```/api/family/situation```