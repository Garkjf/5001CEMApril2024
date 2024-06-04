import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from firebase_admin import credentials, initialize_app ,db
from tkinter.font import BOLD, Font
from tkcalendar import Calendar
from datetime import datetime
import pytz
import os
import subprocess
import PatientPage
from SharePath import start_login

# Create relative file paths
dir = os.path.dirname(__file__)

serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')   # Change the path to your own serviceAccountKey.json
logoImageFile = os.path.join(dir, '../Images/CallADoctor-logo-small.png')  # Change the path to your own logo image
backIconImage = os.path.join(dir, '../Images/back-icon.png') # Change the path to your own logo image

def start_login():
    subprocess.Popen(["python", os.path.join(dir, 'Login.py')])

class PatientPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F6F6E9")
        self.pack(fill=tk.BOTH, expand=True)
        cred = credentials.Certificate(serviceAccountKeyFile)
        initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})

    def searchClinic(self):
        self.clearClinicInfo()  
        self.clearFilters()

        # Create font style
        bold14 = Font(self.master, size=14, weight=BOLD) 
        bold10 = Font(self.master, size=10, weight=BOLD) 
        
        row = tk.Frame(self, bg="#F6F6E9")
        row.grid(sticky="w")

        clinic_filter_frame = tk.Frame(row, borderwidth=2, relief="groove", width=300, height=100)
        clinic_filter_frame.grid(row=0, column=0, padx=10, pady=30, sticky="w")

        label = tk.Label(self, text="Search For Clinics", bg="#F6F6E9", font=bold14)
        label.grid(row=0, column=0, pady=20, padx=10,  sticky="w")

        # Get a reference to the clinics node in the database
        clinics_ref = db.reference('clinicAdmins')

        # Retrieve the clinic data
        clinics = clinics_ref.get()

        # Clinic selection
        clinic_options = ["All Clinic"]
        clinic_names = set()
        clinic_state_options = ["All State"]
        clinic_states = set()

        for _, clinic_data in clinics.items():
            clinic_name = clinic_data.get('clinic_name')
            clinic_state = clinic_data.get('clinic_state')
            if clinic_name not in clinic_names:
                clinic_options.append(clinic_name)
                clinic_names.add(clinic_name)

            if clinic_state not in clinic_states:
                clinic_state_options.append(clinic_state)
                clinic_states.add(clinic_state)

        # Clinic state Selection
        self.clinic_state_var = tk.StringVar()
        self.label = tk.Label(self, text="Filter by Clinic State", bg="#F6F6E9", font=bold10)
        self.label.grid(row=1, column=0, pady=10, padx=10,  sticky="w")  
        self.clinic_state_dropdown = ttk.Combobox(self, textvariable=self.clinic_state_var, values=clinic_state_options, state="readonly")
        self.clinic_state_dropdown.current(0)  # Set the default value to "All State"
        self.clinic_state_dropdown.grid(row=2, column=0, pady=10, padx=10, sticky="w") 

        # Clinic name Selection
        self.clinic_var = tk.StringVar()
        self.label = tk.Label(self, text="Filter by Clinic Name", bg="#F6F6E9", font=bold10)
        self.label.grid(row=1, column=0, pady=10, padx=200, sticky="w")
        self.clinic_dropdown = ttk.Combobox(self, textvariable=self.clinic_var, values=clinic_options, state="readonly", width=35)
        self.clinic_dropdown.current(0)  # Set the default value to "All Clinic"
        self.clinic_dropdown.grid(row=2, column=0, pady=10, padx=200, sticky="w")

        submit_button = tk.Button(self, text="Search", bg="#0275DD", fg="#ffffff", command=self.displayClinicInfo)
        submit_button.grid(row=2, column=0, pady=10, padx=480, sticky="w")

        # initialize the total clinic found label
        self.total_label = tk.Label(self, text="Total clinics found: 0", bg="#F6F6E9", font=bold10)
        self.total_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")

        self.displayClinicInfo()

    def displayClinicInfo(self):
        # Clear the clinic information
        self.clearClinicInfo()

        #  create font style
        bold12 = Font(self.master, size=12, weight=BOLD, family="Helvetica")

        # Get the selected clinic state and clinic name
        selected_state = self.clinic_state_var.get()
        selected_clinic = self.clinic_var.get()

        # Get a reference to the clinics node in the database
        clinics_ref = db.reference('clinicAdmins')

        # Retrieve the clinic data
        clinics = clinics_ref.get()

        # Create a set to store unique clinic names and states
        unique_clinics = set()

        # Display the clinic information
        count = 0
        row = tk.Frame(self, bg="#F6F6E9")
        row.grid()

        for clinic_id, clinic_data in clinics.items():
            clinic_name = clinic_data.get('clinic_name')
            clinic_state = clinic_data.get('clinic_state')

            # Check if the clinic name and state combination is unique
            if (clinic_name, clinic_state) not in unique_clinics:
                unique_clinics.add((clinic_name, clinic_state))

                # Check if the selected clinic state matches
                if selected_state != "All State" and selected_state != clinic_state:
                    continue

                # Check if the selected clinic name matches
                if selected_clinic != "All Clinic" and selected_clinic != clinic_name:
                    continue

                # Frame for the clinic
                clinic_frame = tk.Frame(row, borderwidth=2, relief="groove", width=200, height=100)
                clinic_frame.grid(row=count//4, column=count%4, padx=10, pady=30, sticky="w")

                # Clinic Name
                name_label_text = tk.Label(clinic_frame, text="Clinic Name: ", font= bold12)
                name_label_text.grid(row=0, column=count, sticky="w", padx=5, pady=5)
                name_label_value = tk.Label(clinic_frame, text=clinic_name)
                name_label_value.grid(row=0, column=count+1, sticky="w", padx=5, pady=5)

                # Clinic State
                state_label_text = tk.Label(clinic_frame, text="Clinic State: ", font= bold12)
                state_label_text.grid(row=1, column=count, sticky="w", padx=5, pady=5)
                state_label_value = tk.Label(clinic_frame, text=clinic_state)
                state_label_value.grid(row=1, column=count+1, sticky="w", padx=5, pady=5)

                view_more_button = tk.Button(clinic_frame, text="View More",bg="#0275DD", fg="#ffffff", command=lambda clinic_id=clinic_id, clinic_name=clinic_name, clinic_state=clinic_state : [self.doctorListFilter(clinic_id, clinic_name, clinic_state), my_canvas.yview_moveto(0)])
                view_more_button.grid(row=2, column=count, columnspan=2, padx=5, pady=5)

                count += 1

        # Update the total number of clinics found
        self.total_label.config(text=f"Total clinics found: {count}")        

    def clearClinicInfo(self):
        # Clear the clinic information
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()
    
    def clearFilters(self):
        # Clear the filters and search button from the searchClinic function/ ViewDoctorList function
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Combobox) or isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                widget.destroy()

    def doctorListFilter(self, clinic_id, selected_clinic, selected_state):
        self.clearClinicInfo()
        self.clearFilters()

         # Start Filter Part - Filter by Doctor Specialty
        bold14 = Font(self.master, size=14, weight=BOLD) 
        bold10 = Font(self.master, size=10, weight=BOLD) 

        row = tk.Frame(self, bg="#F6F6E9")
        row.grid(sticky="w")

        doctor_filter_frame = tk.Frame(row, borderwidth=2, relief="groove", width=300, height=100)
        doctor_filter_frame.grid(row=0, column=0, padx=10, pady=30, sticky="w")

        label = tk.Label(self, text=f"Search For {selected_clinic} - {selected_state} Doctors", bg="#F6F6E9", font=bold14)
        label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Load the back icon
        back_icon = tk.PhotoImage(file=backIconImage)
        back_icon = back_icon.subsample(20, 20)

        # Back button
        back_button = tk.Button(self, image=back_icon, command=self.searchClinic)
        back_button.image = back_icon 
        back_button.grid(row=0, columnspan=5, pady=10, padx=1000, sticky="e")

        # Get a reference to the doctors node in the database
        docotrs_ref = db.reference('doctors')

        # Retrieve the clinic data
        doctors = docotrs_ref.get()

        # Doctor selection
        doctor_specialty_options = ["All Specialty"]
        doctor_specialties = set()

        for doctor_id, doctor_data in doctors.items():
            specialist = doctor_data.get('specialist')
            if doctor_data.get('clinic_state')  == selected_state and doctor_data.get('clinic_name') == selected_clinic:
                if specialist not in doctor_specialties:
                    doctor_specialty_options.append(specialist)
                    doctor_specialties.add(specialist)

        # Doctor Specialty Selection
        self.doctor_specialty_var = tk.StringVar()
        self.label = tk.Label(self, text="Filter by Doctor Specialty", bg="#F6F6E9", font=bold10)
        self.label.grid(row=1, column=0, pady=10, padx=10, sticky="w")  
        self.clinic_state_dropdown = ttk.Combobox(self, textvariable=self.doctor_specialty_var, values=doctor_specialty_options, state="readonly")
        self.clinic_state_dropdown.current(0)  # Set the default value to "All specialty"
        self.clinic_state_dropdown.grid(row=2, column=0, pady=10, padx=10, sticky="w") 

        submit_button = tk.Button(self, text="Search", bg="#0275DD", fg="#ffffff", command=lambda: self.viewDoctorList(clinic_id, selected_clinic, selected_state, self.doctor_specialty_var.get()))
        submit_button.grid(row=2, column=0, pady=10, padx=200, sticky="w")
        # End Filter Part - Filter by Doctor Specialty

        # initialize the total doctor found label
        self.total_label = tk.Label(self, text="Total doctor found: 0", bg="#F6F6E9", font=bold10)
        self.total_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")

        self.viewDoctorList(clinic_id, selected_clinic, selected_state, self.doctor_specialty_var.get())

    def viewDoctorList(self, clinic_id, selected_clinic, selected_state, selected_specialty):
        # Clear the clinic information
        self.clearClinicInfo()

        #  create font style
        bold12 = Font(self.master, size=12, weight=BOLD, family="Helvetica")
        
        # Get the selected clinic state and clinic name
        print(f"Selected state: {selected_state}, Selected clinic: {selected_clinic}")  # Debugging print statement

        # Get a reference to the doctors node in the database
        doctors_ref = db.reference('doctors')

        # Retrieve the doctors data
        doctors = doctors_ref.get()

        # Display the clinic information
        count = 0
        row = tk.Frame(self, bg="#F6F6E9")
        row.grid()
        
        # Display the related doctors
        for doctor_id, doctor_data in doctors.items():
            if doctor_data.get('clinic_state')  == selected_state and doctor_data.get('clinic_name') == selected_clinic and (doctor_data.get('specialist') == selected_specialty or selected_specialty == "All Specialty"):
                print(f"Match found for doctor {doctor_id}")  # Debugging print statement

                clinic_frame = tk.Frame(row, borderwidth=2, relief="groove", width=300, height=100)
                clinic_frame.grid(row=count//4, column=count%4, padx=10, pady=30, sticky="w")

                doctor_name = doctor_data.get('username')
                doctor_specialty = doctor_data.get('specialist')

                # Clinic Name
                doctor_label_text = tk.Label(clinic_frame, text="Doctor: ", font= bold12)
                doctor_label_text.grid(row=0, column=count, sticky="w", padx=10, pady=5)
                doctor_label_value = tk.Label(clinic_frame, text=doctor_name)
                doctor_label_value.grid(row=0, column=count+1, sticky="w", padx=10, pady=5)

                # Clinic State
                specialty_label_text = tk.Label(clinic_frame, text="Specialty: ", font= bold12)
                specialty_label_text.grid(row=1, column=count, sticky="w", padx=10, pady=5)
                specialty_label_value = tk.Label(clinic_frame, text=doctor_specialty)
                specialty_label_value.grid(row=1, column=count+1, sticky="w", padx=10, pady=5)

                view_more_button = tk.Button(clinic_frame, text="View More",bg="#0275DD", fg="#ffffff", command=lambda doctor_id=doctor_id: self.viewDoctorInformation(doctor_id, selected_clinic, selected_state))
                view_more_button.grid(row=2, column=count, columnspan=2, padx=10, pady=5)

                count += 1

        # Update the total number of doctor found
        try:
            self.total_label.config()
        except tk.TclError:
            self.total_label = tk.Label(self, text="Total doctor found: 0", bg="#F6F6E9", font=Font(self.master, size=10, weight=BOLD))
            self.total_label.grid(row=3, column=0, padx=10, sticky="w")

        # Update the total number of clinics found
        self.total_label.config(text=f"Total doctors found: {count}")  

    def viewDoctorInformation(self, search_doctor_id, selected_clinic, selected_state):          
        # Clear the doctor information
        for widget in self.winfo_children():
            widget.destroy()
        print("viewDoctorInformation called")  # Debugging print statement

        # Get a reference to the doctors node in the database
        doctors_ref = db.reference('doctors')

        # Retrieve the clinic data
        doctors = doctors_ref.get()

        # Retrieve the clinic data
        for doctor_id, doctor_data in doctors.items():
            if doctor_id == search_doctor_id:
                doctor_name = doctor_data.get('username')
                doctor_phone = doctor_data.get('phone')
                doctor_email = doctor_data.get('email')
                doctor_specialty = doctor_data.get('specialist')
                clinic_name = doctor_data.get('clinic_name')
                clinic_state = doctor_data.get('clinic_state')

        # Create font style
        bold14 = Font(self.master, size=14, weight=BOLD) 
        bold12 = Font(self.master, size=12, weight=BOLD)
        label = tk.Label(self, text=f"Search For {selected_clinic} - {selected_state}'s Doctor Detail", bg="#F6F6E9", font=bold14)
        label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Back button
        back_icon = tk.PhotoImage(file=backIconImage)
        back_icon = back_icon.subsample(20, 20)
        # Load the back icon
        back_button = tk.Button(self, image=back_icon, command=lambda clinic_id=doctor_id: self.doctorListFilter(clinic_id, selected_clinic, selected_state))
        back_button.image = back_icon 
        back_button.grid(row=0, columnspan=5, pady=10, padx=1000, sticky="w")

        label = tk.Label(self, text=f"Dr. {doctor_name}:", bg="#F6F6E9", font=bold12)
        label.grid(row=2, column=0, padx=40, pady=5, sticky="w")

        info_frame = tk.Frame(self, bg="#d9d9d9", width=400, height=300)
        info_frame.grid(row=3, column=0)

        labels = [
            ("Doctor Name :", doctor_name),
            ("Doctor Phone :", doctor_phone),
            ("Doctor Email :", doctor_email),
            ("Doctor Specialty :", doctor_specialty),
            ("Clinic Name :", clinic_name),
            ("Clinic State :", clinic_state),
        ]

        for i, (label, value) in enumerate(labels):
            tk.Label(info_frame, text=label, font=("Helvetica", 12, "bold"), bg="#d9d9d9", padx=30, pady=10).grid(row=i, column=0, sticky="w")
            tk.Label(info_frame, text=value, font=("Helvetica", 10), bg="#d9d9d9", padx=30, pady=10).grid(row=i, column=1, sticky="w")

    def makeAppointment(self):
        self.clearClinicInfo()  
        self.clearFilters()

        # Create font style
        bold14 = Font(self.master, size=14, weight=BOLD) 
        bold12 = Font(self.master, size=12, weight=BOLD)
        bold10 = Font(self.master, size=10, weight=BOLD)
        label = tk.Label(self, text="Reserve Your Time Slot", bg="#F6F6E9", font=bold14)
        label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        with open('login_data.txt', 'r') as f:
            ic_passport_id = f.read().strip()

        # get patient information
        patient_ref = db.reference('patients/' + ic_passport_id)
        patient_data = patient_ref.get()

        label = tk.Label(self, text="Patient Information", bg="#F6F6E9", font=bold12)
        label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        if isinstance(patient_data, dict):
            username = patient_data['username']
            email = patient_data['email']
            phone = patient_data['phone']

            self.label = tk.Label(self, text="Name:", bg="#f6f6e9", font=bold10)
            self.label.grid(row=2, column=0, padx=20, sticky="w") 
            self.username_entry = tk.Entry(self, width=30)
            self.username_entry.insert(0, username)
            self.username_entry.grid(row=3, column=0, padx=20, pady=10, sticky="w")

            self.label = tk.Label(self, text="Email:", bg="#f6f6e9", font=bold10)
            self.label.grid(row=4, column=0, padx=20, sticky="w") 
            self.email_entry = tk.Entry(self, width=30)
            self.email_entry.insert(0, email)
            self.email_entry.grid(row=5, column=0, padx=20, pady=10, sticky="w")

            self.label = tk.Label(self, text="Phone Number:", bg="#f6f6e9", font=bold10)
            self.label.grid(row=2, column=1, padx=20, sticky="w") 
            self.phone_entry = tk.Entry(self, width=30)
            self.phone_entry.insert(0, phone)
            self.phone_entry.grid(row=3, column=1, padx=20, pady=10, sticky="w")

            clinic_ref = db.reference('clinicAdmins')
            clinics = clinic_ref.get()

        # get clinic information
        clinics_ref = db.reference('clinicAdmins')

        clinics = clinics_ref.get()

        clinic_options = ["Choose Clinic"]
        clinic_names = set()

        clinic_state_options = ["Choose Clinic State"]
        clinic_states = set()
        
        for clinic_id, clinic_data in clinics.items():
            clinic_name = clinic_data.get('clinic_name')
            clinic_state = clinic_data.get('clinic_state')
            if clinic_name not in clinic_names:
                clinic_options.append(clinic_name)
                clinic_names.add(clinic_name)
            if clinic_state not in clinic_states:
                clinic_state_options.append(clinic_state)
                clinic_states.add(clinic_state)

        label = tk.Label(self, text="Clinic Information", bg="#f6f6e9", font=bold12)
        label.grid(row=7, column=0, padx=20, pady=10, sticky="w")

        # clinic name selection
        self.clinic_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Clinic", bg="#f6f6e9", font=bold10)
        self.label.grid(row=8, column=0, padx=20, sticky="w")
        self.clinic_dropdown = ttk.Combobox(self, textvariable=self.clinic_var, values=clinic_options, state="readonly", width=30)
        self.clinic_dropdown.current(0)  
        self.clinic_dropdown.grid(row=9, column=0, padx=20, sticky="w")
        self.clinic_dropdown.bind("<<ComboboxSelected>>", self.check_clinic_selection)

        # Clinic state Selection
        self.clinic_state_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Clinic State", bg="#f6f6e9", font=bold10)
        self.label.grid(row=8, column=1, padx=20, sticky="w")  # Changed column to 1
        self.clinic_state_dropdown = ttk.Combobox(self, textvariable=self.clinic_state_var, values=clinic_state_options, state="readonly")
        self.clinic_state_dropdown.current(0)  #
        self.clinic_state_dropdown.grid(row=9, column=1, padx=20, sticky="w") 
        self.clinic_state_dropdown.bind("<<ComboboxSelected>>", self.check_clinic_state_selection)

        # Get doctor information
        doctors_ref = db.reference('doctors')

        doctors = doctors_ref.get()

        # get the doctor data based on the selected clinic state and clinic name
        selected_clinic_state = self.clinic_state_var.get()
        selected_clinic_name = self.clinic_var.get()

        filtered_doctors = [doctor for doctor in doctors.values() if doctor['clinic_state'] == selected_clinic_state and doctor['clinic_name'] == selected_clinic_name]

        label = tk.Label(self, text="Doctor Information", bg="#f6f6e9", font=bold12)
        label.grid(row=1, column=3, padx=20, pady=10, sticky="w")

        # Get the names and specialties of the filtered doctors
        doctor_names = [doctor['username'] for doctor in filtered_doctors]
        doctor_names = ["Choose Doctor"]
        doctor_specialties = [doctor['specialist'] for doctor in filtered_doctors]
        doctor_specialties = ["Choose Specialty"]

        self.doctor_name_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Doctor", bg="#f6f6e9", font=bold10)
        self.label.grid(row=2, column=3, padx=20, sticky="w")
        self.doctor_name_dropdown = ttk.Combobox(self, textvariable=self.doctor_name_var, values=doctor_names, state="readonly")
        self.doctor_name_dropdown.current(0)
        self.doctor_name_dropdown.grid(row=3, column=3, padx=20, pady=10, sticky="w", font=bold10)
        self.doctor_name_dropdown.bind("<<ComboboxSelected>>", self.check_doctor_name_selection)

        self.doctor_specialty_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Doctor Specialty", bg="#f6f6e9")
        self.label.grid(row=2, column=4, padx=20, sticky="w")
        self.doctor_specialty_dropdown = ttk.Combobox(self, textvariable=self.doctor_specialty_var, values=doctor_specialties, state="readonly")
        self.doctor_specialty_dropdown.current(0)
        self.doctor_specialty_dropdown.grid(row=3, column=4, padx=20, pady=10, sticky="w")
        self.doctor_specialty_dropdown.bind("<<ComboboxSelected>>", self.check_doctor_specialty_selection)
        
        self.label = tk.Label(self, text="Select Appointment Date", bg="#f6f6e9", font=bold10)
        self.label.grid(row=4, column=3, padx=20, sticky="w")
        self.appointment_date_entry = Calendar(self)
        self.appointment_date_entry.grid(row=5, column=3, padx=20, pady=10, sticky="w", rowspan=5)

        self.label = tk.Label(self, text="Select Appointment Time Slot", bg="#f6f6e9", font=bold10)
        self.label.grid(row=4, column=4, padx=20, sticky="w")
        self.appointment_time_entry = ttk.Combobox(self, values=["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"])
        self.appointment_time_entry.current(0)
        self.appointment_time_entry.grid(row=5, column=4, padx=20, pady=10, sticky="w")

        
        # Create save button
        save_button = tk.Button(self, text="submit", command=self.save_appointment, width=20, bg="#0275DD", fg="#ffffff")
        save_button.grid(row=10, columnspan=5, pady=20, padx=20)

    def check_clinic_selection(self, event):
        selected_clinic = self.clinic_var.get()
        selected_clinic_state = self.clinic_state_var.get()
        if selected_clinic == "Choose Clinic":
            messagebox.showerror("Error", "Please select a clinic")
        else:
            self.update_doctor_dropdown(selected_clinic, selected_clinic_state)

    def check_clinic_state_selection(self, event):
        selected_clinic = self.clinic_var.get()
        selected_clinic_state = self.clinic_state_var.get()
        if selected_clinic_state == "Choose Clinic State":
            messagebox.showerror("Error", "Please select a clinic state")
        else:
            self.update_doctor_dropdown(selected_clinic, selected_clinic_state) 
    
    def check_doctor_name_selection(self, event):
        selection = self.doctor_name_var.get()
        if selection == "Choose Doctor":
            messagebox.showerror("Error", "Please select a doctor")
        elif selection == "No doctors available":
            messagebox.showerror("Error", "No doctors available for the selected clinic")
    
    def check_doctor_specialty_selection(self, event):
        selection = self.doctor_specialty_var.get()
        if selection == "Choose Specialty":
            messagebox.showerror("Error", "Please select a doctor specialty")
        elif selection == "No specialties available":
            messagebox.showerror("Error", "No specialties available for the selected clinic")

    def update_doctor_dropdown(self, selected_clinic_name, selected_clinic_state):
        doctors_ref = db.reference('doctors')
        doctors = doctors_ref.get()

        filtered_doctors = [doctor for doctor in doctors.values() if doctor['clinic_state'] == selected_clinic_state and doctor['clinic_name'] == selected_clinic_name]

        # Get the doctor names and specialties of the filtered doctors
        doctor_names = [doctor['username'] for doctor in filtered_doctors]
        doctor_specialties = list(set(doctor['specialist'] for doctor in filtered_doctors))

        # Update the doctor name dropdown
        self.doctor_name_dropdown['values'] = doctor_names if doctor_names else ["No doctors available"]
        self.doctor_name_dropdown.current(0)

        # Update the doctor specialty dropdown
        self.doctor_specialty_dropdown['values'] = doctor_specialties if doctor_specialties else ["No specialties available"]
        self.doctor_specialty_dropdown.current(0)

    def save_appointment(self):
        try:
            timestamp = datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
            formatted_timestamp = timestamp.strftime('%d/%m/%Y %H:%M')
            username = self.username_entry.get()
            email = self.email_entry.get()
            phone = self.phone_entry.get()
            clinic_name = self.clinic_var.get()
            clinic_state = self.clinic_state_var.get()
            doctor_name = self.doctor_name_var.get()
            specialty = self.doctor_specialty_var.get()
            appointment_date = self.appointment_date_entry.get()
            appointment_time = self.appointment_time_entry.get()

            ref = db.reference('appointment')
            new_appointment_ref = ref.push()  # generate a unique key and return a new reference

            new_appointment_ref.set({
                'appointmentNo': new_appointment_ref.key,  # unique key as the appointmentNo
                'username': username,
                'email': email,
                'phone': phone,
                'clinic_name': clinic_name,
                'clinic_state': clinic_state,
                'doctor_name': doctor_name,
                'specialty': specialty,
                'appointment_date': appointment_date,
                'appointment_time': appointment_time,
                'created_at': formatted_timestamp,
                'updated_at': formatted_timestamp,
                'status': 'Pending'
            }) 
            messagebox.showinfo("Success", "Appointment saved successfully")  
        except Exception as e:
            print(f"An error occurred: {e}")
            messagebox.showerror("Error", "An error occurred while saving the appointment")

    def viewPrescriptionHistory(self):
        pass

    def appointmentRequest(self):
        pass      

    def logout(self):
        start_login()
        self.master.quit()

# Main Execution
if __name__ == "__main__":
    root = tk.Tk()  # Create a new Tk root window
    root.title("Call a Doctor - Patient Page")  # Set the title of the window
    root.geometry("1200x600")
    root.configure(background='#f6f6e9')

    # Load the logo image
    logo = tk.PhotoImage(file=logoImageFile)
    logo = logo.subsample(4, 4)

    # get logo image size
    logo_width = logo.width()
    logo_height = logo.height()

    # navigation bar
    nav_bar = tk.Frame(background='#f6f6e9', height= logo_height, width= logo_width)
    nav_bar.pack(side="top", fill="x", padx=250, pady=10)
    
    # Create a main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)

    # Create a canvas inside the main frame
    my_canvas = tk.Canvas(main_frame, bg="#f6f6e9")
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # Add a vertical scrollbar to the canvas
    my_scrollbar_vertival = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar_vertival.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas
    my_canvas.configure(yscrollcommand=my_scrollbar_vertival.set)

    # Create another frame inside the canvas
    second_frame = tk.Frame(my_canvas, bg="#f6f6e9", width=1200)

    # Add that new frame to a window in the canvas
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")

    # Update the scrollregion of the canvas to include the entire second_frame
    second_frame.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    # display image
    logo_label = tk.Label(nav_bar, image=logo)
    logo_label.pack(side="left", fill="x")   
 
    # Body
    app = PatientPage(second_frame)  # Pass the second_frame window to your LoginPage class

    search_clinics_btn = tk.Button(nav_bar, text="Search Clinics", command=app.searchClinic)
    search_clinics_btn.pack(side="left", fill="x")

    make_appointment_btn = tk.Button(nav_bar, text="Make Appointment", command=app.makeAppointment)
    make_appointment_btn.pack(side="left", fill="x")

    prescription_btn = tk.Button(nav_bar, text="Prescription", command=app.viewPrescriptionHistory)
    prescription_btn.pack(side="left", fill="x")

    appointment_request_btn = tk.Button(nav_bar, text="Appointment Request", command=app.appointmentRequest)
    appointment_request_btn.pack(side="left", fill="x")

    logout_btn = tk.Button(nav_bar, text="Logout", command=app.logout)
    logout_btn.pack(side="left", fill="x")

    app.pack(fill="both", expand=True)  # Make the LoginPage fill the entire window
    app.searchClinic()
    root.mainloop()  