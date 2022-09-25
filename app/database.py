from pymongo import mongo_client
import pymongo
from app.config import settings

client = mongo_client.MongoClient(settings.DATABASE_URL)
print('Connected to MongoDB...')

db = client[settings.MONGO_INITDB_DATABASE]

User = db.users
Post = db.posts
Role = db.roles

User.create_index([("email", pymongo.ASCENDING)], unique=True)
Post.create_index([("title", pymongo.ASCENDING)], unique=True)
Role.create_index([("name", pymongo.ASCENDING)], unique=True)
