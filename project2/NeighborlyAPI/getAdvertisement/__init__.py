import azure.functions as func
import os
import pymongo
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:

    # example call http://localhost:7071/api/getAdvertisement/?id=5ec34b2265403b17d00ae864

    id = req.params.get('id')
    print("--------------->", id)
    
    if id:
        try:
            url = "mongodb://cosmodbudacity:DB2QnHNxzMB5m8z35x3nTnMtklCU4mTC9chDKL5CmLC5wsz4jyU3vLbEncDFxLHT6XHSua2cMbxH1d0WKE8eXQ==@cosmodbudacity.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cosmodbudacity@"
            client = pymongo.MongoClient(url)
            database = client['udacity']
            collection = database['advertisements']
           
            query = {'_id': ObjectId(id)}
            result = collection.find_one(query)
            print("----------result--------")

            result = dumps(result)
            print(result)

            return func.HttpResponse(result, mimetype="application/json", charset='utf-8')
        except:
            return func.HttpResponse("Database connection error.", status_code=500)

    else:
        return func.HttpResponse("Please pass an id parameter in the query string.", status_code=400)