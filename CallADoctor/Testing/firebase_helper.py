from firebase_admin import credentials, initialize_app, db, get_app
import os

dir = os.path.dirname(__file__)

serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')  # Change the path to your own serviceAccountKey.json

try:
    app = get_app()
except ValueError:
    cred = credentials.Certificate(serviceAccountKeyFile)
    app = initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})

def get_clinics():
    clinics_ref = db.reference('clinicAdmins')
    return clinics_ref.get()

def get_user_data(role):
    ref = db.reference(role.lower() + 's')
    return ref.get()
