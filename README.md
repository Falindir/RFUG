# Random French User Generator

## Version

v0.3

## Install

```
sudo pip install Flask Werkzeug PyYAML numpy markdown
```

## Run

```
./run.sh
```

## Usage

0. With URL: <a target="_blank" href="http://localhost:5000/api/users?n=10">link</a>

1. With curl:<br/>
    ```curl -i http://localhost:5000/api/users?n=10```


## Parameters

1. **n** (int) : The number of users generate.

2. **gender** (string) : If you want specific gender (other gender are accepted).
<br/> If not use the result it's a random choice beetween "homme" and "femme". 

3. **firstname** (string): If you want specific firstname.

4. **lastname** (string): If you want specific lastname.

5. **age** (int) : The age of users. We accept multiple value.

6. **age[]** (array) : The age range for users with min & max value in array.

7. **region** (int||string): If you want specific region. Id or name is accepted.

## Output exemple

```
[
  {
    "age": 71, 
    "cellphone": "06-80-62-37-20", 
    "city": {
      "INSEE": "93055", 
      "id": "pantin", 
      "name": "Pantin", 
      "postalcode": "93500"
    }, 
    "firstName": "Gaspard", 
    "gender": "homme", 
    "id": 9, 
    "lastName": "Bertin", 
    "phone": "01-43-84-76-18", 
    "region": {
      "id": "93", 
      "name": "Seine-Saint-Denis"
    }, 
    "uuid": "40c670fc-cb2d-497a-b60a-30f99f20b269"
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