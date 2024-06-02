import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import BOLD, Font
import os
from firebase_admin import credentials, initialize_app, db
dir = os.path.dirname(__file__)

serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')
logoImageFile = os.path.join(dir, '../Images/CallADoctor-logo-small.png')
backIconImage = os.path.join(dir, '../Images/back-icon.png')

class DoctorPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#9AB892")
        self.pack(fill=tk.BOTH, expand=True)
        cred = credentials.Certificate(serviceAccountKeyFile)
        initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})
        
        self.patients = db.reference('patients').get()
        self.bold14 = Font(self.master, size=14, weight=BOLD)

        self.listPatients(self.patients)

    def listPatients(self, patients):
        self.clearPage()

        top_frame = tk.Frame(self, bg="#9AB892")
        top_frame.grid(column=0, row=0, sticky="w")
        label = tk.Label(top_frame, text="Search For Patient", font=self.bold14, background="#9AB892")
        label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.patient_name_entry = tk.Entry(top_frame)
        self.patient_name_entry.grid(row=1, column=0, padx=20, pady=10, sticky="W")

        submit_button = tk.Button(top_frame, text="Search", bg="#0275DD", fg="#ffffff", 
                                  command=self.search_patient)
        submit_button.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        row = tk.Frame(self, bg="#9AB892")
        row.grid(row=1, column=0, columnspan=2)

        for count, (patient_id, patient) in enumerate(patients.items()):
            # Frame for the patient
            patient_frame = tk.Frame(row, borderwidth=2, relief="groove", width=200, height=100)
            patient_frame.grid(row=count//4, column=count%4, padx=10, pady=30, sticky="w")

            name_label = tk.Label(patient_frame, text=f"Patient Name: {patient.get('username')}")
            name_label.grid(row=0, column=0, padx=20, sticky="w")

            view_button = tk.Button(patient_frame, text="View", bg="#0275DD", fg="#ffffff", command = 
                                    lambda: self.showPatientPrescriptions(patient_id))
            view_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

            email_label = tk.Label(patient_frame, text=f"Email: {patient.get('email')}")
            email_label.grid(row=1, column=0, padx=20, sticky="w")

    def clearPage(self):
        # Clear the patient information
        [widget.destroy() for widget in self.winfo_children() if isinstance(widget, tk.Frame)]

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
        self.listPatients(patients)

    def handleViewPatient(self, patient_id):
        return lambda: self.showPatientPrescriptions(patient_id)

    def showPatientPrescriptions(self, patient_id):
        self.clearPage()

        top_frame = tk.Frame(self, bg="#9AB892")
        top_frame.grid(column=0, row=0, sticky="w")

        # Load the back icon
        back_icon = tk.PhotoImage(file=backIconImage)
        back_icon = back_icon.subsample(20, 20)

        back_button = tk.Button(top_frame, image=back_icon, 
                                command=lambda: self.listPatients(self.patients))
        back_button.image = back_icon
        back_button.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        patient_info_frame = tk.Frame(top_frame, bg="#ffffff")
        patient_info_frame.grid(row=1, column=0, padx=20)

        patient = self.patients.get(patient_id)
        
        title_label = tk.Label(patient_info_frame, text="Patient Information", padx=10, pady=10,
                               font=self.bold14, bg="#ffffff")
        title_label.grid(row=0, column=0, sticky="w")

        patient_info = [f"Patient Name: {patient.get('username')}", 
                        f"Email: {patient.get('email')}",
                        f"Phone Number: {patient.get('phone')}"]
        
        for row, patient_info in enumerate(patient_info, 1):
            tk.Label(patient_info_frame, text=patient_info, padx=10, bg="#ffffff")\
            .grid(row=row, column=0, sticky="w")


if __name__ == "__main__":
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

    search_clinics_btn = tk.Button(nav_bar, text="Search Patients")
    search_clinics_btn.pack(side="left", fill="x")

    make_appointment_btn = tk.Button(nav_bar, text="Assigned Request")
    make_appointment_btn.pack(side="left", fill="x")

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
    second_frame = tk.Frame(my_canvas, bg="#9AB892", width=1200)

    # Add that new frame to a window in the canvas
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")

    # Update the scrollregion of the canvas to include the entire second_frame
    second_frame.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
 
    # Body
    app = DoctorPage(second_frame)

    app.pack(fill="both", expand=True)
    root.mainloop()
