import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, initialize_app ,db
import os
import subprocess
import Patient

# Create relative file paths
dir = os.path.dirname(__file__)

serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')   # Change the path to your own serviceAccountKey.json
logoImageFile = os.path.join(dir, '../Images/CallADoctor-logo.png')  # Change the path to your own logo image

class Patient(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#9AB892")

        self.label = tk.Label(self, text="Patient Page", bg="#9AB892")
        self.label.pack()

        self.patient_id = None
        self.record_id = None
        self.doctor_id = None
        self.email = None
        self.phone_number = None
        self.address = None
        self.username = None
        self.password = None
        self.visit_date = None
        self.create_at = None
        self.updated_at = None
        
        # Create the navigation bar
        self.nav_bar = tk.Frame(self, bg="#6B9778")
        self.nav_bar.pack()

        # Create the navigation buttons
        self.search_clinics_btn = tk.Button(self.nav_bar, text="Search Clinics", command=self.searchClinic)
        self.search_clinics_btn.pack(side="left")

        self.make_appointment_btn = tk.Button(self.nav_bar, text="Make Appointment", command=self.makeAppointment)
        self.make_appointment_btn.pack(side="left")

        self.prescription_btn = tk.Button(self.nav_bar, text="Prescription", command=self.viewPrescriptionHistory)
        self.prescription_btn.pack(side="left")

        self.appointment_request_btn = tk.Button(self.nav_bar, text="Appointment Request", command=self.sendRequest)
        self.appointment_request_btn.pack(side="left")

    def searchClinic(self):

        # Initialize Firebase
        cred = credentials.Certificate(serviceAccountKeyFile)
        initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})

        # Get a reference to the clinics node in the database
        clinics_ref = db.reference('clinicAdmins')

        # Retrieve the clinic data
        clinics = clinics_ref.get()

        # Display the clinic information
        for clinic_id, clinic_data in clinics.items():
            clinic_name = clinic_data.get('clinic_name')
            clinic_state = clinic_data.get('clinic_state')

            # Create a new frame for the clinic
            clinic_frame = tk.Frame(self, borderwidth=2, relief="groove")
            clinic_frame.pack(pady=10)

            # Create a label for the clinic name and add it to the frame
            name_label = tk.Label(clinic_frame, text=f"Clinic Name: {clinic_name}")
            name_label.pack()

            # Create a label for the clinic state and add it to the frame
            state_label = tk.Label(clinic_frame, text=f"Clinic State: {clinic_state}")
            state_label.pack()

    def sendRequest(self):
        pass

    def viewClinic(self):
        pass

    def makeAppointment(self):
        pass

    def viewPrescriptionHistory(self):
        pass

# Main Execution
if __name__ == "__main__":
    root = tk.Tk()  # Create a new Tk root window
    root.title("Call a Doctor - Patient Page")  # Set the title of the window
    root.geometry("750x550")
    app = Patient(root)  # Pass the root window to your LoginPage class
    app.pack(fill="both", expand=True)  # Make the LoginPage fill the entire window
    app.searchClinic()
    root.mainloop()  