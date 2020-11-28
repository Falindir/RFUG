# Random French User Generator

## Version

v0.1

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

6. **age[]** (array) : The age range for users withmin & max value in array.


## Output exemple

```
[
  {
    "age": 30, 
    "firstName": "Emmy", 
    "gender": "femme", 
    "id": 0, 
    "lastName": "Michel", 
    "uuid": "f9f3e42c-a879-4f99-9cbb-04f75d48dfa8"
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
