from flask import Flask, request, jsonify, json
from werkzeug.exceptions import HTTPException
import random
import uuid
import yaml
import os.path
import numpy
import markdown.extensions.fenced_code
import csv

app = Flask(__name__)

DEBUG = True
MAX_USERS = 500
AGE_MIN = 0
AGE_MAX = 99

basedir = os.path.abspath(os.path.dirname(__file__))
femaleFirstNamePath = os.path.join(basedir, 'data/female_first_name.yaml')
maleFirstNamePath = os.path.join(basedir, 'data/male_first_name.yaml')
lastNamePath = os.path.join(basedir, 'data/last_name.yaml')
regionPath = os.path.join(basedir, 'data/region.csv')
cityPath = os.path.join(basedir, 'data/city.csv')
EMAIL_HOSTS = ["gmail.com", "orange.fr", "yahoo.fr", "laposte.net", "club-internet.fr", "sfr.fr", "neuf.fr"]
FAMILY_SITUATION = [{"value": "marié", "code": "M"},{"value": "pacsé", "code": "O"},{"value": "divorcé", "code": "D"},{"value": "séparé", "code": "D"},{"value": "célibataire", "code": "C"},{"value": "veuf", "code": "V"}]

def printd(message):
    if(DEBUG):
        print(message)

def loadName(path):
    if os.path.exists(path) and os.path.isfile(path):
        with open(path, 'r') as yaml_stream:
            data = yaml.load(yaml_stream, Loader=yaml.SafeLoader)['name']
            return sorted(data, key=lambda k: random.random())
    return []

def loadRegion(path):
    data = []
    if os.path.exists(path) and os.path.isfile(path):
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader, None)  # skip the headers
            for row in reader:
                data.append(row)
    
    return data

def loadCity(path):
    data = {}
    if os.path.exists(path) and os.path.isfile(path):
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader, None)  # skip the headers
            for row in reader:
                key = str(row[0])

                if len(key) == 1:
                    key = "0"+key

                if key not in data:
                    data[key] = []

                data[key].append(row)
    
    return data

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

def getRegion(seed, regions, args):

    region = []
    size = len(regions)

    if "region" in args and args["region"] != "":
        for reg in regions:
            if reg[0] == args["region"] or reg[1] == args["region"]:
                return reg
    
    if size > 0:
        index = seed % size
        return regions[index]

    return region

def getPhoneNumber(seed, region, args):

    phone = region[2]
    indicatifs = region[3].split("-")
    size = len(indicatifs)

    indicatif = "00"

    if size > 0:
        index = seed % size
        indicatif = indicatifs[index]

    phone += "-" + indicatif

    for _ in range(3):
        
        number = random.randrange(0, 100)

        if number < 10:
            phone += "-0" + str(number) 
        else:
            phone += "-" + str(number)
    
    return phone

def getCellphoneNumber(seed, args):

    phone = "0" + str(random.randrange(6, 8))

    for _ in range(4):
    
        number = random.randrange(0, 100)

        if number < 10:
            phone += "-0" + str(number) 
        else:
            phone += "-" + str(number)

    return phone

def getCity(seed, cities, args):
    
    size = len(cities)

    if size > 0:
        index = seed % size
        return cities[index]

    return["0", "xxx", "XXX", "0", "0"]

def getEmail(seed, firstname, lastname, args):

    host = ""

    if "email" in args and args["email"] != "":
        host = args["email"]
    else:
        host = random.choice(EMAIL_HOSTS)

    return firstname.lower()+"."+lastname.lower()+"@"+host

def getFamilySituation(seed, args):

    if "familysituation" in args and args["familysituation"] != "":
        for fs in FAMILY_SITUATION:
            if fs["code"] == args["familysituation"] or fs["value"] == args["familysituation"]:
                return fs

    return random.choice(FAMILY_SITUATION)

def getProbaChildren(code, deep):

    if code == "M": 
        return 80 / deep
    
    elif code == "O": 
        return 30 / deep
    
    elif code == "D": 
        return 50 / deep
        
    elif code == "C": 
        return 10 / deep
    
    elif code == "V": 
        return 45 / deep

    return 0

def getNumberChildren(seed, code, deep, args):
    if random.randrange(1, 101) <= getProbaChildren(code, deep):
        return 1 + getNumberChildren(seed, code, deep+1, args)

    return 0

def generateUser(seed, id, femaleFirstName, maleFirstName, lastnames, regions, cities, args):

    firstnames = []
    gender = getGender(seed, args)

    if gender == "femme":
        firstnames = femaleFirstName
    elif gender == "homme":
        firstnames = maleFirstName
    else:
        firstnames = numpy.append(firstnames, femaleFirstName)
        firstnames = numpy.append(firstnames, maleFirstName)

    region = getRegion(seed, regions, args)

    city = getCity(seed, cities[region[0]], args)

    firstName = getName(seed, "firstname", firstnames, args)
    lastName = getName(seed, "lastname", lastnames, args)

    age = getAge(seed, args)
    familySituation = getFamilySituation(seed, args)
    children = getNumberChildren(seed, familySituation["code"], 1, args)

    if age < 16:
        familySituation = {"value": "célibataire", "code": "C"}
    
        if age < 12:
            children = 0

    result = {
        "id": id,
        "uuid": uuid.uuid4(),
        "gender": gender,
        "firstName": firstName,
        "lastName": lastName,
        "age": age,
        "region": {"id": region[0], "name": region[1]},
        "city": {"id": city[1], "name": city[2], "postalcode": city[3], "INSEE": city[4]},
        "phone": getPhoneNumber(seed, region, args),
        "cellphone": getCellphoneNumber(seed, args),
        "email": getEmail(seed, firstName, lastName, args),
        "family": {"situation": familySituation, "children": children},
        "country": "France"
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

@app.route('/api/regions', methods=['GET'])
def allRegions():
    content = request.json
    return jsonify(loadRegion(regionPath))

@app.route('/api/cities', methods=['GET'])
def allCities():
    content = request.json
    args = request.args

    cities = loadCity(cityPath)

    if 'dep' in args and args["dep"] != "":
        if args["dep"] in cities:
            return jsonify(cities[args["dep"]])

    return jsonify(cities)

@app.route('/api/emails', methods=['GET'])
def allEmails():
    content = request.json
    return jsonify(EMAIL_HOSTS)


@app.route('/api/family/situation', methods=['GET'])
def allFamilySituation():
    content = request.json
    return jsonify(FAMILY_SITUATION)



@app.route('/api/users', methods=['GET'])
def allUsers():
    content = request.json

    args = request.args
    printd(args)

    femaleFirstName = loadName(femaleFirstNamePath)
    maleFirstName = loadName(maleFirstNamePath)
    lastName = loadName(lastNamePath)
    regions = loadRegion(regionPath)
    cities = loadCity(cityPath)

    n = 0
    if 'n' in args and args["n"].isdigit():
        n = int(args["n"])

    if n > MAX_USERS:
        n = MAX_USERS

    users = []
    for i in range(0, n):
        seed = random.randrange(100000, 1000000)
        users.append(generateUser(seed, i, femaleFirstName, maleFirstName, lastName, regions, cities, args))

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

