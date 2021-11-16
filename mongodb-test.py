import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://DFGProject:zxc212345@cluster0.xiytb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster["QuizBot"]
collection = db["Test"]

post1 = {
	"name": "Tim",
	"age": 17
}

post2 = {
	"name": "Bill",
	"age": 31
}

collection.insert_many([post1, post2])
