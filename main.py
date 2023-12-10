from fastapi import FastAPI
from schematics.models import Model
from schematics.types import StringType, EmailType 
import database
from bson import ObjectId

class User(Model):
    user_id= ObjectId()
    user_email = EmailType(required=True)
    user_name = StringType(required=True)
    user_password = StringType(required=True)

user = User()
    
def create_user(email, username, password):
    user.user_id = ObjectId()
    user.user_email = email
    user.user_name = username
    user.user_password = password
    return dict(user)

def user_format(user) -> dict:
    return {
        "user_email": user["user_email"],
        "user_name": user["user_name"],
        "user_password": user["user_password"]
    }

app = FastAPI()

@app.get("/")
def index():
    print (database.db.users.find({'user_email':'user@email.com'}))
    users= []
    for user in database.db.users.find():
        users.append(user_format(user))
    return users

@app.get("/users/")
def read_users():
    users= []
    for user in database.db.users.find():
        users.append(user_format(user))
    return users
    

@app.post("/register/{email}/{username}/{password}")
def register(email, username: str, password: str):
    user_exists = False
    data = create_user(email, username, password)
    dict(data)
    if database.db.users.count_documents({'user_email': data['user_email']}) > 0:
        user_exists = True
        print("User Exists")
        return {"message":"User Exists"}
    elif user_exists == False:
        database.db.users.insert_one(data)
        return {"message":"User Created", 'email': data['user_email']}

@app.delete("/users/{email}")
def delete_user(user_email):
    deleted_item = database.db.users.find_one_and_delete({"user_email": user_email})
    if deleted_item:
        return {"message":"User Deleted"}
    else:
        return {"message":"User Not Found"}

@app.put("/users/{email}")
def edit_user(user_email, user_name, user_password):
    data = create_user(user_email, user_name, user_password)
    dict(data)
    updated_item = database.db.users.find_one_and_update({"user_email": user_email},{"$set": data})
    if updated_item:
        return {"message":"User Updated"}
    else:
        return {"message":"User Not Found"}