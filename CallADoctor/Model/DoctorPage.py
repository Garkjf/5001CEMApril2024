import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import BOLD, Font
import os
from firebase_admin import credentials, initialize_app, db
dir = os.path.dirname(__file__)

serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')
logoImageFile = os.path.join(dir, '../Images/CallADoctor-logo-small.png')

class DoctorPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#9AB892")
        cred = credentials.Certificate(serviceAccountKeyFile)
        initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})

        # Get a reference to the clinics node in the database
        patients_ref = db.reference('patients')

        # Retrieve the clinic data
        self.patients = patients_ref.get()

        # Load the logo image
        logo = tk.PhotoImage(file=logoImageFile)
        logo = logo.subsample(4, 4)

        # navigation bar
        nav_bar = tk.Frame(background='#f6f6e9', height=logo.width(), width=logo.height())
        nav_bar.pack(side="top", fill="x", padx=450, pady=10)

        # display image
        logo_label = tk.Label(nav_bar, image=logo)
        logo_label.pack(side="left", fill="x")

        search_clinics_btn = tk.Button(nav_bar, text="Search Patients")
        search_clinics_btn.pack(side="left", fill="x")

        make_appointment_btn = tk.Button(nav_bar, text="Assigned Request")
        make_appointment_btn.pack(side="left", fill="x")

        bold14 = Font(self.master, size=14, weight=BOLD) 
        label = tk.Label(self, text="Search For Patient", font=bold14)
        label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.patient_name_entry = tk.Entry(self)
        self.patient_name_entry.grid(row=1, column=0, padx=20, pady=10, sticky="W")

        submit_button = tk.Button(self, text="Search", bg="#0275DD", fg="#ffffff", command=self.search_patient)
        # command=self.search_patient
        submit_button.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.listPatients(self.patients)

    def listPatients(self, patients):
        # Clear the clinic information
        self.clearPatientInfo()

        row = tk.Frame(self, bg="#9AB892")
        row.grid()

        for count, (_, patient) in enumerate(patients.items(), 0):
            # Frame for the patient
            patient_frame = tk.Frame(row, borderwidth=2, relief="groove", width=200, height=100)
            patient_frame.grid(row=count//4, column=count%4, padx=10, pady=30, sticky="w")

            name_label = tk.Label(patient_frame, text=f"Patient Name: {patient.get('username')}")
            name_label.grid(row=0, column=0, padx=20, sticky="w")

            view_button = tk.Button(patient_frame, text="View", bg="#0275DD", fg="#ffffff")
            view_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

            email_label = tk.Label(patient_frame, text=f"Email: {patient.get('email')}")
            email_label.grid(row=1, column=0, padx=20, sticky="w")

    def clearPatientInfo(self):
        # Clear the patient information
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

    def search_patient(self):
        # Function to handle the search functionality
        search_key = self.patient_name_entry.get()
        if not search_key:
            self.listPatients(self.patients)
            return
        
        patients = dict(filter(lambda patient: search_key in patient[1].get('username'), self.patients.items()))
        self.listPatients(patients)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Call a Doctor - Doctor Page")
    root.geometry("1200x600")
    app = DoctorPage(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
