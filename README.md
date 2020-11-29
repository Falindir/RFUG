# Random French User Generator

## Version

v0.2

## Install

```
sudo pip install Flask Werkzeug PyYAML numpy markdown
```

## Run

```
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
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
    "age": 27, 
    "cellphone": "06-74-05-37-74", 
    "firstName": "Nolan", 
    "gender": "homme", 
    "id": 9, 
    "lastName": "Menard", 
    "phone": "03-84-61-80-47", 
    "region": {
      "id": "39", 
      "name": "Jura"
    }, 
    "uuid": "a4fb20d5-a349-4772-8110-da6a9d17da0b"
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
