import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# fetch the service account key JSON file path
cred = credentials.Certificate("calladoctor-serviceAccountKey.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# save data
ref = db.reference('py/')
users_ref = ref.child('users')
users_ref.set({
    'alanisawesome': {
        'date_of_birth': 'June 23, 1912',
        'full_name': 'Alan Turing'
    },
    'gracehop': {
        'date_of_birth': 'December 9, 1906',
        'full_name': 'Grace Hopper'
    }
})

# update data
hopper_ref = users_ref.child('gracehop')
hopper_ref.update({
    'nickname': 'Amazing Grace'
})

# read data
handle = db.reference('py/users/gracehop/alanisawesome')

# Read the data at the posts reference (this is a blocking operation)
print(ref.get())