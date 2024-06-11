import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
from tkinter.font import BOLD, Font
import os
from firebase_admin import credentials, initialize_app, db
import subprocess

dir = os.path.dirname(__file__)

# Create relative path to image files
serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')
logoImageFile = os.path.join(dir, '../Images/CallADoctor-logo-small.png')
backIconImage = os.path.join(dir, '../Images/back-icon.png')

def start_login():
    subprocess.Popen(["python", os.path.join(dir, 'Login.py')])

class DoctorPage(tk.Frame):
    def __init__(self, parent, doctor_id):
        super().__init__(parent, bg="#9AB892")
        self.pack(fill=tk.BOTH, expand=True)

        self.doctor_id = doctor_id
        # Connect to database
        cred = credentials.Certificate(serviceAccountKeyFile)
        initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})
        
        self.doctors = db.reference('doctors').get()
        self.patients = self.getDefaultPatients()
        self.prescriptions = db.reference('prescriptions').get()

        self.bold14 = Font(self.master, size=14, weight=BOLD)

        self.showMainPage(self.patients)

    # Get patients that have appointments in the same clinic as the doctor
    def getDefaultPatients(self):
        clinic = self.doctors.get(self.doctor_id).get("clinic_name")

        appointments = db.reference('appointment').get()
        patient_names = set()

        for appointment in appointments.values():
            if appointment.get('clinic_name') == clinic:
                patient_names.add(appointment.get('username'))
        
        db_patients = db.reference('patients').get()
        res_patients = dict(filter(lambda patient: patient[1].get('username') in patient_names, 
                                  db_patients.items()))
        return res_patients

    # Generate Main Page
    def showMainPage(self, patients):        
        self.clearPage()

        top_frame = tk.Frame(self, bg="#9AB892")
        top_frame.grid(column=0, row=0, sticky="w")
        label = tk.Label(top_frame, text="Search For Patient", font=self.bold14, background="#9AB892")
        label.grid(row=0, column=0, sticky="w")

        self.patient_name_entry = tk.Entry(top_frame)
        self.patient_name_entry.grid(row=1, column=0, pady=10, sticky="W")

        submit_button = tk.Button(top_frame, text="Search", bg="#0275DD", fg="#ffffff", 
                                  command=self.search_patient)
        submit_button.grid(row=1, column=1, pady=10, sticky="w")

        patients_list = tk.Frame(self, bg="#9AB892")
        patients_list.grid(row=1, column=0, columnspan=2)

        self.listPatients(patients_list, patients)

    # List Patients
    def listPatients(self, frame, patients):
        for count, (patient_id, patient) in enumerate(patients.items()):
            # Frame for the patient
            patient_frame = tk.Frame(frame, borderwidth=2, relief="groove", 
                                     width=200, height=100)
            patient_frame.grid(row=count//4, column=count%4, padx=10, pady=30, sticky="w")

            name_label = tk.Label(patient_frame, text=f"Patient Name: {patient.get('username')}")
            name_label.grid(row=0, column=0, padx=20, sticky="w")

            view_button = tk.Button(patient_frame, text="View", bg="#0275DD", fg="#ffffff", command= 
                                    self.handleViewPatient(patient_id))
            view_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

            email_label = tk.Label(patient_frame, text=f"Email: {patient.get('email')}")
            email_label.grid(row=1, column=0, padx=20, sticky="w")

    # Clear page
    def clearPage(self):
        # Clear the patient information
        [widget.destroy() for widget in self.winfo_children() if isinstance(widget, tk.Frame)]

    # Filter patients by search term
    def search_patient(self):
        # Function to handle the search functionality
        search_key = self.patient_name_entry.get()
        if not search_key:
            self.listPatients(self.patients)
            return
        
        patients_ref = db.reference('patients')
        self.patients = patients_ref.get()
        patients = dict(filter(lambda patient: search_key in patient[1].get('username'), 
                               self.patients.items()))
        
        self.showMainPage(patients)

    # Create back button with command
    def placeBackButton(self, frame, command):
        # Load the back icon
        back_icon = tk.PhotoImage(file=backIconImage)
        back_icon = back_icon.subsample(20, 20)

        back_button = tk.Button(frame, image=back_icon, command=command)
        back_button.image = back_icon
        back_button.grid(row=0, column=0, sticky="w")

        patient_info_frame = tk.Frame(frame, bg="#ffffff")
        patient_info_frame.grid(row=1, column=0, pady=10)

    # Redirect to patient prescription page
    def handleViewPatient(self, patient_id):
        return lambda: self.showPatientInfoPage(patient_id)

    def showPatientInfoPage(self, patient_id):
        self.clearPage()

        top_frame = tk.Frame(self, bg="#9AB892")
        top_frame.grid(column=0, row=0, sticky="w")
        self.placeBackButton(top_frame, lambda: self.showMainPage(self.patients))

        patient_info_frame = tk.Frame(top_frame, bg="#ffffff")
        patient_info_frame.grid(row=1, column=0, pady=20)

        # Get patient from patient_id
        patient = self.patients.get(patient_id)
        
        title_label = tk.Label(patient_info_frame, text="Patient Information", padx=10, pady=10,
                               font=self.bold14, bg="#ffffff")
        title_label.grid(row=0, column=0, sticky="w")

        patient_info = [f"Patient Name: {patient.get('username')}", 
                        f"Email: {patient.get('email')}",
                        f"Phone Number: {patient.get('phone')}"]
        
        for row, patient_info in enumerate(patient_info, 1):
            tk.Label(patient_info_frame, text=patient_info, bg="#ffffff")\
            .grid(row=row, column=0, padx=10, sticky="w")
        
        tk.Label(patient_info_frame, text="Generate New Prescription", padx=50, font=self.bold14,
                 bg="#ffffff").grid(row=0, column=1)
        
        tk.Button(patient_info_frame, text="Add New Prescription",
                  bg="#5FCF37", fg="#ffffff",
                  command= self.handleAddPrescription(patient_id)).grid(row=1, column=1)
        
        prescriptions = dict(filter(lambda entry: str(entry[1].get('patientID')) == patient_id, 
                                    self.prescriptions.items()))
        self.generatePrescriptionTable(prescriptions)
    
    # Create prescriptions table
    def generatePrescriptionTable(self, prescriptions):
        prescription_table = tk.Frame(self)
        prescription_table.grid(row=2, column=0, pady=20, sticky="w")

        columnNames = ["Doctor Name", "Specialist", "Action"]
        for column, name in enumerate(columnNames):
            e = tk.Label(prescription_table, highlightbackground="black", highlightthickness=1,
                         padx=20, borderwidth=2, text=name, font=("Arial", 12, BOLD))
            e.grid(row=0, column=column)
        
        for row, (prescription_id, prescription) in enumerate(prescriptions.items(), 1):
            doctor = self.doctors.get(prescription.get('doctorID'))
            e = tk.Label(prescription_table, padx=20, text=doctor.get('username'))
            e.grid(row=row, column=0)

            e = tk.Label(prescription_table, padx=20, text=doctor.get('specialist'))
            e.grid(row=row, column=1)

            view_button = tk.Button(prescription_table, padx=20, pady=5, text="View", 
                                    bg="#0275DD", fg="#ffffff",
                                    command=self.handleViewPrescription(prescription_id))
            view_button.grid(row=row, column=2)
    
    # Prescription info page
    def handleViewPrescription(self, prescription_id):
        return lambda: self.showPrescriptionInfoPage(prescription_id)
    
    def showPrescriptionInfoPage(self, prescription_id):
        self.clearPage()

        prescription = self.prescriptions.get(prescription_id)
        patient_id = str(prescription.get('patientID'))
        patient = self.patients.get(patient_id)
        doctor = self.doctors.get(prescription.get('doctorID'))

        top_frame = tk.Frame(self, bg="#9AB892")
        top_frame.grid(column=0, row=0, sticky="w")

        self.placeBackButton(top_frame, self.handleViewPatient(patient_id))

        main_frame = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        main_frame.grid(row=1, column=0, pady=10)

        tk.Label(main_frame, text="Patient Information", font=self.bold14, bg="#ffffff",
                 pady=10).grid(row=0, column=0, sticky="w")

        self.fillPrescriptionInfo(main_frame, patient, doctor, prescription)

    def fillPrescriptionInfo(self, main_frame, patient, doctor, prescription):
        info_frame = tk.Frame(main_frame, bg="#ffffff")
        info_frame.grid(row=1, column=0, sticky="w")

        prescription_info = [
            ("Patient Name", patient.get('username')), ("Email", patient.get('email')),
            ("Phone Number", patient.get('phone')), ("Clinic Name", doctor.get('clinic_name')),
            ("Doctor Name", doctor.get('username')), ("Doctor Phone Number", doctor.get('phone')),
            ("Specialist", doctor.get('specialist'))
        ]
        
        for i, (label, value) in enumerate(prescription_info):
            column, row = divmod(i, 4)

            label = tk.Label(info_frame, text=f"{label}: {value}", padx=5, pady=5, 
                             bg="#ffffff")
            label.grid(row=row+1, column=column, sticky="w")
        
        # Fill information for middle frame
        middle_frame = tk.Frame(main_frame, bg="#D9D9D9", padx=10, pady=10)
        middle_frame.grid(row=4, column=0, sticky="w", pady=10)

        prescription_info = [
            ("Symptoms", prescription.get('symptoms')),
            ("Diagnosis", prescription.get('diagnosis')),
            ("Treatment", prescription.get('treatment'))
        ]

        for i, (label, value) in enumerate(prescription_info):
            label = tk.Label(middle_frame, text=f"{label}: {value}", padx=5, pady=5, bg="#D9D9D9")
            label.grid(row=i, column=0, sticky="w")
        
        tk.Label(main_frame, text="Doctor's Remark", font=self.bold14, bg="#ffffff")\
            .grid(row=5, column=0, sticky="w")
        
        remark_frame = tk.Frame(main_frame, bg="#D9D9D9", padx=10, pady=10)
        remark_frame.grid(row=6, column=0, sticky="w")

        tk.Label(remark_frame, text=prescription.get("remark"), bg="#D9D9D9")\
            .grid(row=0, column=0, sticky="w")
    
    # Add New Prescription page
    def handleAddPrescription(self, patient_id):
        return lambda: self.showAddPrescriptionPage(patient_id)

    def showAddPrescriptionPage(self, patient_id):
        self.clearPage()

        top_frame = tk.Frame(self, bg="#9AB892")
        top_frame.grid(column=0, row=0, sticky="w")

        self.placeBackButton(top_frame, self.handleViewPatient(patient_id))
        
        patient = self.patients.get(patient_id)

        main_frame = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        main_frame.grid(row=1, column=0, pady=10)

        tk.Label(main_frame, text="Patient Information", font=self.bold14, bg="#ffffff",
                 pady=10).grid(row=0, column=0, sticky="w")
        
        info_frame = tk.Frame(main_frame, bg="#ffffff")
        info_frame.grid(row=1, column=0, columnspan=2, sticky="w")

        doctor = self.doctors.get(str(self.doctor_id))

        prescription_info = [
            ("Patient Name", patient.get('username')), 
            ("Email", patient.get('email')),
            ("Phone Number", patient.get('phone')), 
            ("Clinic Name", doctor.get('clinic_name')),
            ("Doctor Name", doctor.get('username')), 
            ("Doctor Phone Number", doctor.get('phone')),
            ("Specialist", doctor.get('specialist'))
        ]
        
        for i, (label, value) in enumerate(prescription_info):
            column, row = divmod(i, 4)

            label = tk.Label(info_frame, text=f"{label}: {value}", padx=5, pady=5, 
                             bg="#ffffff")
            label.grid(row=row+1, column=column, sticky="w")

        tk.Label(main_frame, text="Symptoms", bg="#ffffff").grid(row=2, column=0, 
                                                                 padx=10, sticky="w")
        self.symptoms_entry = tk.Entry(main_frame)
        self.symptoms_entry.grid(row=2, column=1, pady=10, sticky="w")

        tk.Label(main_frame, text="Diagnosis", bg="#ffffff").grid(row=3, column=0, 
                                                                 padx=10, sticky="w")
        self.diagnosis_entry = tk.Entry(main_frame)
        self.diagnosis_entry.grid(row=3, column=1, pady=10, sticky="w")

        tk.Label(main_frame, text="Treatment", bg="#ffffff").grid(row=3, column=0, 
                                                                 padx=10, sticky="w")
        self.treatment_entry = tk.Entry(main_frame)
        self.treatment_entry.grid(row=3, column=1, pady=10, sticky="w")

        tk.Label(main_frame, text="Doctor's Remark", bg="#ffffff").grid(row=4, column=0, 
                                                                 padx=10, sticky="w")
        self.remark_entry = tk.Text(main_frame, height=5, width=50)
        self.remark_entry.grid(row=5, column=0, pady=10, columnspan=2, sticky="w")

        submit_button = tk.Button(main_frame, padx=20, pady=5, text="View", 
                                    bg="#0275DD", fg="#ffffff", 
                                    command = lambda: self.addPrescription(patient_id))
        submit_button.grid(row=6, column=0, pady=10, sticky="w")

    # Add new prescription function
    def addPrescription(self, patient_id):
        newPrescription = {
            "diagnosis": self.diagnosis_entry.get(),
            "treatment": self.treatment_entry.get(),
            "remark": self.remark_entry.get(),
            "symptoms": self.diagnosis_entry.get(),
            "patientID": patient_id,
            "doctorID": doctor_id
        }
        db.reference('prescriptions').push(newPrescription)
        messagebox.showinfo("Success", "Created new prescription!")
        self.showAddPrescriptionPage(patient_id)

    # Assigned Reuqest Page
    def showAssignedRequestPage(self):
        self.clearPage()

        top_frame = tk.Frame(self, bg="#9AB892")
        top_frame.grid(column=0, row=0, sticky="w")
        tk.Label(top_frame, text="Assigned Request", bg="#9AB892", font=self.bold14)\
            .grid(row=0, column=0, padx=10, sticky='w')
        
        filter_frame = tk.Frame(top_frame, bg="#9AB892")
        filter_frame.grid(row=1, column=0, sticky='w', pady=10)

        tk.Label(filter_frame, text="Filter By Doctor Name", bg="#9AB892")\
            .grid(row=0, column=0, sticky='w', padx=10)

        doctor_name_options = ["All"]
        self.doctor_name_var = tk.StringVar()
        self.doctor_name_dropdown = ttk.Combobox(filter_frame, 
                                                  textvariable=self.doctor_name_var, 
                                                  values=doctor_name_options, 
                                                  state="readonly")
        self.doctor_name_dropdown.current(0)
        self.doctor_name_dropdown.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        tk.Label(filter_frame, text="Filter By Speciality", bg="#9AB892")\
            .grid(row=0, column=1, sticky='w', padx=10)

        doctor_specialty_options = ["All Specialty"]
        self.doctor_specialty_var = tk.StringVar()
        self.doctor_specialty_dropdown = ttk.Combobox(filter_frame,
                                                  textvariable=self.doctor_specialty_var, 
                                                  values=doctor_specialty_options, 
                                                  state="readonly")
        self.doctor_specialty_dropdown.current(0)
        self.doctor_specialty_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        submit_button = tk.Button(filter_frame, padx=20, pady=5, text="Search", 
                                    bg="#0275DD", fg="#ffffff")
        submit_button.grid(row=1, column=2, padx=10, sticky="w")


    # Logout
    def logout(self):
        start_login()
        self.master.quit()

if __name__ == "__main__":
    # Get doctor_id from command argument
    doctor_id = sys.argv[1]
    
    root = tk.Tk()
    root.title("Call a Doctor - Doctor Page")
    root.geometry("1200x600")
    root.configure(background="#f6f6e9")

    # Navigation bar
    logo = tk.PhotoImage(file=logoImageFile)
    logo = logo.subsample(4, 4)

    nav_bar = tk.Frame(background='#f6f6e9', height=logo.width(), width=logo.height())
    nav_bar.pack(side="top", fill="x", padx=100, pady=10)

    logo_label = tk.Label(nav_bar, image=logo, padx=20)
    logo_label.pack(side="left")

    # Create a main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)

    # Create a canvas inside the main frame
    my_canvas = tk.Canvas(main_frame, bg="#9AB892")
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # Add a vertical scrollbar to the canvas
    my_scrollbar_vertical = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas
    my_canvas.configure(yscrollcommand=my_scrollbar_vertical.set)

    # Create another frame inside the canvas
    second_frame = tk.Frame(my_canvas, padx=20, pady=20, bg="#9AB892", width=1200)

    # Add that new frame to a window in the canvas
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")

    # Update the scrollregion of the canvas to include the entire second_frame
    second_frame.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
 
    # Body
    app = DoctorPage(second_frame, doctor_id)

    # Create buttons for navigation bar
    search_clinics_btn = tk.Button(nav_bar, text="Search Patients", 
                                   command=lambda: app.showMainPage(app.patients))
    search_clinics_btn.pack(side="left", fill="x")

    make_appointment_btn = tk.Button(nav_bar, text="Assigned Request", 
                                      command=app.showAssignedRequestPage)
    make_appointment_btn.pack(side="left", fill="x")

    logout_btn = tk.Button(nav_bar, text="Logout", command=app.logout,)
    logout_btn.pack(side="left", fill="x")

    app.pack(fill="both", expand=True)
    root.mainloop()
