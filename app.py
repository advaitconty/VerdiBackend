from flask import Flask, request, redirect, url_for, abort
from pymongo import MongoClient
import certifi

app = Flask(__name__)

client = MongoClient("mongodb+srv://oddysey:advaitconty@leaflogic.44pa0.mongodb.net/?retryWrites=true&w=majority&appName=LeafLogic",
                     tlsCAFile=certifi.where())

db = client["leaflogic"]
collection = db["leaflogic"]

@app.route('/')
def main():
    return "server is up!"

@app.route('/leaderboard')
def leaderboard():
    items = list(collection.find())
    for index, _ in enumerate(items):
        del items[index]["_id"]

    return sorted(items, key=lambda x: x["credits"], reverse=True) # can reverse sort by adding reverse=True at back

@app.route('/add', methods=["POST"])
def add():
    data = request.json

    if len(list(data.keys())) == 2:
        print("verified!")
    else:
        return "error!"

    for index in range(len(list(collection.find()))):
        print(data)
        if list(collection.find())[index]["username"] == data["username"]:
            collection.delete_one({"username": data["username"]})
            print("deleted old one!")

    collection.insert_one(data)

    return "done!"

@app.route('/existing')
def existing():
    items = list(collection.find())
    names = []
    for _, item in enumerate(items):
        names.append(item["username"])

    return names

if __name__ == "__main__":
    app.run(debug=True)
