from pymongo import MongoClient



def start_client():
    client = MongoClient("mongodb+srv://logistics_now:logistics_now@cluster0.waer0pj.mongodb.net/")
    return client

