from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():

    from pymongo import MongoClient
    client = MongoClient('172.17.0.2', 27017)
    db = client.test
    collection = db.gRPC
    consulta = collection.find_one()

    return consulta

app.run(host='0.0.0.0', port=8080)
