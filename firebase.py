import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('secretkey.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://welcometoatriauniversity-default-rtdb.firebaseio.com/"
})

ref = db.reference('index')
ref.child("welcome").set(0)
print(ref.get())