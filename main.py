from flask import Flask, request, jsonify, json
from werkzeug.exceptions import HTTPException
import random
import uuid
import yaml
import os.path
import numpy
import markdown.extensions.fenced_code

app = Flask(__name__)

DEBUG = True
MAX_USERS = 500
AGE_MIN = 0
AGE_MAX = 99

basedir = os.path.abspath(os.path.dirname(__file__))
femaleFirstNamePath = os.path.join(basedir, 'data/female_first_name.yaml')
maleFirstNamePath = os.path.join(basedir, 'data/male_first_name.yaml')
lastNamePath = os.path.join(basedir, 'data/last_name.yaml')

def printd(message):
    if(DEBUG):
        print(message)

def loadName(path):
    results = []
    if os.path.exists(path) and os.path.isfile(path):
        with open(path, 'r') as yaml_stream:
            data = yaml.load(yaml_stream, Loader=yaml.SafeLoader)['name']
            return sorted(data, key=lambda k: random.random())

def getGender(seed, args):

    if 'gender' in args and args["gender"] != "":
        if args["gender"] == "homme":
            return "homme"
        elif args["gender"] == "femme":
            return "femme"
        else:
            return args["gender"]

    return "homme" if seed % 2 else "femme"

def getName(seed, key, names, args):
    size = len(names)

    if key in args and args[key] != "":
        return args[key]    

    if size > 0:
        index = seed % size
        return names[index]
    
    return "XXX"

def getAge(seed, args):

    if "age" in args and args["age"] != "":

        ages = args.getlist("age")

        if len(ages) > 0:
            index = seed % len(ages)
            age = ages[index]
            if age.isdigit():
                return int(age)
    
    elif "age[]" in args and args["age[]"] != "":
        ages = args.getlist("age[]")

        if len(ages) > 0:

            ags = []
            for age in ages:
                if age.isdigit():
                    ags.append(int(age))

            return random.randrange(min(ags), max(ags))
            
    else:
        return random.randrange(AGE_MIN, AGE_MAX)

    return 0


def generateUser(seed, id, femaleFirstName, maleFirstName, lastnames, args):

    firstnames = []
    gender = getGender(seed, args)

    if gender == "femme":
        firstnames = femaleFirstName
    elif gender == "homme":
        firstnames = maleFirstName
    else:
        firstnames = numpy.append(firstnames, femaleFirstName)
        firstnames = numpy.append(firstnames, maleFirstName)

    result = {
        "id": id,
        "uuid": uuid.uuid4(),
        "gender": gender,
        "firstName": getName(seed, "firstname", firstnames, args),
        "lastName": getName(seed, "lastname", lastnames, args),
        "age": getAge(seed, args)
    }
    
    return result

@app.route('/api/male/firstname', methods=['GET'])
def allMaleFirstName():
    content = request.json
    return jsonify(loadName(maleFirstNamePath))

@app.route('/api/female/firstname', methods=['GET'])
def allFemaleFirstName():
    content = request.json
    return jsonify(loadName(femaleFirstNamePath))

@app.route('/api/lastname', methods=['GET'])
def allLastName():
    content = request.json
    return jsonify(loadName(lastNamePath))

@app.route('/api/users', methods=['GET'])
def allUsers():
    content = request.json

    args = request.args
    printd(args)

    femaleFirstName = loadName(femaleFirstNamePath)
    maleFirstName = loadName(maleFirstNamePath)
    lastName = loadName(lastNamePath)
    
    n = 0
    if 'n' in args and args["n"].isdigit():
        n = int(args["n"])

    if n > MAX_USERS:
        n = MAX_USERS

    users = []
    for i in range(0, n):
        seed = random.randrange(100000, 1000000)
        users.append(generateUser(seed, i, femaleFirstName, maleFirstName, lastName, args))

    return jsonify(users)

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

    
@app.route('/') 
def home():
    homePage = open("README.md", "r")
    return markdown.markdown(homePage.read(), extensions=["fenced_code"])

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=DEBUG)

