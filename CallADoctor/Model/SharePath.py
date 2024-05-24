import subprocess
import os

# Create relative file paths
dir = os.path.dirname(__file__)

def start_login():
    subprocess.call(["python", os.path.join(dir, "login.py")])

def start_registration():
    subprocess.call(["python", os.path.join(dir, "registration.py")])

def start_patient():
    subprocess.call(["python", os.path.join(dir, "Patient.py")])