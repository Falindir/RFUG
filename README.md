# Random French User Generator

## Version

v0.4.1

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

## Output exemple

```
[
  {
    "age": 55, 
    "cellphone": "07-77-89-18-38", 
    "city": {
      "INSEE": "73258", 
      "id": "saint-martin-de-la-porte", 
      "name": "Saint-Martin-de-la-Porte", 
      "postalcode": "73140"
    }, 
    "country": "France", 
    "email": "pablo.breton@yahoo.fr", 
    "firstName": "Pablo", 
    "gender": "homme", 
    "id": 9, 
    "lastName": "Breton", 
    "phone": "04-57-27-19-09", 
    "region": {
      "id": "73", 
      "name": "Savoie"
    }, 
    "uuid": "f1011c8a-1559-4c14-b5fc-fcd8f924986b"
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

4. All cities: <br/>
    ```/api/cities```<br/>
    
    With department id : ```/api/cities?dep=30```