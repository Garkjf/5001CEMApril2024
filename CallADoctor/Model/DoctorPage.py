import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import BOLD, Font
from PIL import Image, ImageTk
import os
from firebase_admin import credentials, initialize_app, db
dir = os.path.dirname(__file__)

serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')

class DoctorPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#9AB892")
        cred = credentials.Certificate(serviceAccountKeyFile)
        initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})

        # Get a reference to the clinics node in the database
        patients_ref = db.reference('patients')

        # Retrieve the clinic data
        patients = patients_ref.get()

        # navigation bar
        nav_bar = tk.Frame(bg="#6B9778")
        nav_bar.pack()

        search_clinics_btn = tk.Button(nav_bar, text="Search Patients")
        search_clinics_btn.pack(side="left")

        make_appointment_btn = tk.Button(nav_bar, text="Assigned Request")
        make_appointment_btn.pack(side="left")

        bold14 = Font(self.master, size=14, weight=BOLD) 
        label = tk.Label(self, text="Search For Patient", bg="#F6F6E9", font=bold14)
        label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

        patient_name_entry = tk.Entry(self)
        patient_name_entry.grid(row=3, column=0, columnspan=30, padx=20, pady=(10, 0), sticky="w")

        submit_button = tk.Button(self, text="Search", bg="#0275DD", fg="#ffffff")
        submit_button.grid(row=3, column=1, pady=(10, 0), sticky="w")

        self.listPatients(patients)

        # Ensure the patient_frame expands correctly
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

    def listPatients(self, patients):
         for row, (_, patient) in enumerate(patients.items(), 4):
            # Create a frame with a white background to display patient details
            patient_frame = tk.Frame(self, bg='white', width=400, height=30)
            patient_frame.grid(row=row, column=0, padx=20, pady=20, sticky="w")
            self.grid_rowconfigure(row, weight=1)

            name_label = tk.Label(patient_frame, text=f"Patient Name: {patient.get('username')}", 
                                  bg="white")
            name_label.grid(row=0, column=0, padx=20, sticky="w")

            view_button = tk.Button(patient_frame, text="View", bg="#0275DD", fg="#ffffff")
            view_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

            email_label = tk.Label(patient_frame, text=f"Email: {patient.get('email')}", bg="white")
            email_label.grid(row=1, column=0, padx=20, sticky="w")

    # def search_patient(self):
    #     # Function to handle the search functionality
    #     patient_name = self.patient_name_entry.get()
    #     messagebox.showinfo("Search", f"Searching for patient: {patient_name}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Call a Doctor - Doctor Page")
    root.geometry("750x550")
    app = DoctorPage(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
