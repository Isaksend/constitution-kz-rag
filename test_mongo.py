from pymongo import MongoClient

# Direct connection string (replace with your actual connection string)
MONGODB_URI = "mongodb+srv://constitution_user:qwerty123456@cluster0.wsrvjwf.mongodb.net/constitution_db?retryWrites=true&w=majority"

client = MongoClient(MONGODB_URI)

try:
    # Test the connection
    client.admin.command('ping')
    print("Connection to MongoDB Atlas successful!")

    # List databases
    databases = client.list_database_names()
    print(f"Available databases: {databases}")
except Exception as e:
    print(f"Connection failed: {e}")