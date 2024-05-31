import subprocess
import os

# Create relative file paths
dir = os.path.dirname(__file__)

def start_login():
    subprocess.call(["python", os.path.join(dir, "Login.py")])

def start_registration():
    subprocess.call(["python", os.path.join(dir, "Registration.py")])

def start_patient():
    subprocess.call(["python", os.path.join(dir, "PatientPage.py")])

def start_doctor():
    subprocess.call(["python", os.path.join(dir, "DoctorPage.py")])

def start_admin():
    subprocess.call(["python", os.path.join(dir, "ClinicAdministratorPage.py")])