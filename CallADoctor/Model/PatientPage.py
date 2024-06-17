import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from firebase_admin import credentials, initialize_app ,db
from tkinter.font import BOLD, Font
from tkcalendar import Calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
import os
import subprocess
import sys
import PatientPage

# Create relative file paths
dir = os.path.dirname(__file__)

serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')   # Change the path to your own serviceAccountKey.json
logoImageFile = os.path.join(dir, '../Images/CallADoctor-logo-small.png')  # Change the path to your own logo image
backIconImage = os.path.join(dir, '../Images/back-icon.png') # Change the path to your own logo image

def start_login():
    subprocess.Popen(["python", os.path.join(dir, 'Login.py')])

class PatientPage(tk.Frame):
    def __init__(self, parent, patient_id):
        self.patient_id = patient_id

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
            status = clinic_data.get('status')
            if status == "Approved":
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
            if isinstance(widget, ttk.Combobox) or isinstance(widget, tk.Label) or isinstance(widget, tk.Button) or isinstance(widget, Calendar) or isinstance(widget, tk.Entry):
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
            status = doctor_data.get('status')
            if status == "Approved":
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
            if doctor_data.get('status') == "Approved":
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
        
        make_appointment_btn = tk.Button(self, text="Reserve Your Appointment", bg="#0275DD", fg="#ffffff", command=lambda :self.makeAppointment(clinic_name, clinic_state, doctor_name, doctor_specialty))
        make_appointment_btn.grid(columnspan=1, pady=10)    

    def makeAppointment(self, clinic_name, clinic_state, doctor_name, doctor_specialty):
        self.clearClinicInfo()  
        self.clearFilters()

        # Create font style
        bold14 = Font(self.master, size=14, weight=BOLD) 
        bold12 = Font(self.master, size=12, weight=BOLD)
        bold10 = Font(self.master, size=10, weight=BOLD)
        label = tk.Label(self, text="Reserve Your Time Slot", bg="#F6F6E9", font=bold14)
        label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # get patient information
        patient_ref = db.reference('patients/' + self.patient_id)
        patient_data = patient_ref.get()

        label = tk.Label(self, text="Patient Information", bg="#F6F6E9", font=bold12)
        label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        if isinstance(patient_data, dict):
            username = patient_data['username']
            email = patient_data['email']
            phone = patient_data['phone']

            self.label = tk.Label(self, text="Name:", bg="#f6f6e9", font=bold10)
            self.label.grid(row=2, column=0, padx=20, sticky="w") 
            self.user_label = tk.Label(self, text=username, bg="#ffffff", width=30, border=2, relief="groove", state="disabled")
            self.user_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

            self.label = tk.Label(self, text="Email:", bg="#f6f6e9", font=bold10)
            self.label.grid(row=4, column=0, padx=20, sticky="w") 
            self.email_label = tk.Label(self, text=email, bg="#ffffff", width=30, border=2, relief="groove", state="disabled")
            self.email_label.grid(row=5, column=0, padx=20, pady=10, sticky="w")

            self.label = tk.Label(self, text="Phone Number:", bg="#f6f6e9", font=bold10)
            self.label.grid(row=2, column=1, padx=20, sticky="w") 
            self.phone_label = tk.Label(self, text=phone, bg="#ffffff", width=30, border=2, relief="groove", state="disabled")
            self.phone_label.grid(row=3, column=1, padx=20, pady=10, sticky="w")

            clinic_ref = db.reference('clinicAdmins')
            clinics = clinic_ref.get()

        # get clinic information
        clinics_ref = db.reference('clinicAdmins')

        clinics = clinics_ref.get()

        clinic_options = ["Choose Clinic"]
        clinic_names = set()

        clinic_state_options = ["Choose Clinic State"]
        clinic_states = set()
    
        if clinic_name is not None and clinic_state is not None:
            clinic_options = [clinic_name]
            clinic_state_options = [clinic_state]
        else:
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

        if doctor_name is not None and doctor_specialty is not None:
            doctor_names = [doctor_name]
            doctor_specialties = [doctor_specialty]
        else:
            # Get the names and specialties of the filtered doctors
            doctor_names = [doctor['username'] for doctor in filtered_doctors if doctor['status']=="Approved"]
            doctor_names = ["Choose Doctor"]
            doctor_specialties = [doctor['specialist'] for doctor in filtered_doctors if doctor['status']=="Approved"]
            doctor_specialties = ["Choose Specialty"]

        self.doctor_specialty_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Doctor Specialty", bg="#f6f6e9", font=bold10)
        self.label.grid(row=2, column=3, padx=20, sticky="w")
        self.doctor_specialty_dropdown = ttk.Combobox(self, textvariable=self.doctor_specialty_var, values=doctor_specialties, state="readonly")
        self.doctor_specialty_dropdown.current(0)
        self.doctor_specialty_dropdown.grid(row=3, column=3, padx=20, pady=10, sticky="w")
        self.doctor_specialty_dropdown.bind("<<ComboboxSelected>>", self.check_doctor_specialty_selection)

        self.doctor_name_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Doctor", bg="#f6f6e9", font=bold10)
        self.label.grid(row=2, column=4, padx=20, sticky="w")
        self.doctor_name_dropdown = ttk.Combobox(self, textvariable=self.doctor_name_var, values=doctor_names, state="readonly")
        self.doctor_name_dropdown.current(0)
        self.doctor_name_dropdown.grid(row=3, column=4, padx=20, pady=10, sticky="w")
        self.doctor_name_dropdown.bind("<<ComboboxSelected>>", self.check_doctor_name_selection)

        self.label = tk.Label(self, text="Select Appointment Date", bg="#f6f6e9", font=bold10)
        self.label.grid(row=4, column=3, padx=20, sticky="w")
        self.appointment_date_entry = Calendar(self)
        self.appointment_date_entry.grid(row=5, column=3, padx=20, pady=10, sticky="w", rowspan=5)
        self.appointment_date_entry.bind("<<CalendarSelected>>", self.check_date_selection)

        # set the available time slots
        current_time = datetime.now(pytz.timezone('Asia/Kuala_Lumpur')).time()
        if current_time.hour >= 17:
            available_times = ["No Time Slot Available"]
        else:
            available_times = ["Choose Time Slot"]
            for i in range(9, 18):
                if current_time.hour < i:
                    if i < 10:
                        available_times.append(f"0{i}:00")
                    else:
                        available_times.append(f"{i}:00")

        self.appointment_time_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Appointment Time Slot", bg="#f6f6e9", font=bold10)
        self.label.grid(row=4, column=4, padx=20, sticky="w")
        self.appointment_time_entry = ttk.Combobox(self, textvariable=self.appointment_time_var, values=available_times, state="readonly")
        self.appointment_time_entry.current(0)
        self.appointment_time_entry.grid(row=5, column=4, padx=20, pady=10, sticky="w")
        self.appointment_time_entry.bind("<<DateEntrySelected>>", self.check_time_selection)

        # Create save button
        save_button = tk.Button(self, text="submit", command=lambda : self.save_appointment(username, email, phone), width=20, bg="#0275DD", fg="#ffffff")
        save_button.grid(row=10, columnspan=5, pady=20, padx=20)

    def check_clinic_selection(self, event):
        selected_clinic = self.clinic_var.get()
        selected_clinic_state = self.clinic_state_var.get()
        if selected_clinic == "Choose Clinic":
            messagebox.showerror("Error", "Please select a clinic")
        else:
            self.update_doctor_specialty_dropdown(selected_clinic, selected_clinic_state)

    def check_clinic_state_selection(self, event):
        selected_clinic = self.clinic_var.get()
        selected_clinic_state = self.clinic_state_var.get()
        if selected_clinic_state == "Choose Clinic State":
            messagebox.showerror("Error", "Please select a clinic state")
        else:
            self.update_doctor_specialty_dropdown(selected_clinic, selected_clinic_state) 
    
    def check_doctor_specialty_selection(self, event):
        selected_clinic = self.clinic_var.get()
        selected_clinic_state = self.clinic_state_var.get()
        selected_specialty = self.doctor_specialty_var.get()
        if selected_specialty == "Choose Specialty":
            messagebox.showerror("Error", "Please select a doctor specialty")
            self.doctor_name_dropdown['values'] = ["Choose Doctor"]
            self.doctor_name_dropdown.current(0)
        elif selected_specialty == "No specialties available":
            messagebox.showerror("Error", "No specialties available for the selected clinic")
        else:
            self.update_doctor_dropdown(selected_clinic, selected_clinic_state, selected_specialty)
    
    def check_doctor_name_selection(self, event):
        doctor_name = self.doctor_name_var.get()
        if doctor_name == "Choose Doctor":
            messagebox.showerror("Error", "Please select a doctor")
        elif doctor_name == "No doctors available":
            messagebox.showerror("Error", "No doctors available for the selected clinic")

    def update_doctor_specialty_dropdown(self, selected_clinic_name, selected_clinic_state):
        doctors_ref = db.reference('doctors')
        doctors = doctors_ref.get()
        
        # Get the doctor specialties
        filtered_specialties = [doctor for doctor in doctors.values() if doctor['clinic_state'] == selected_clinic_state and doctor['clinic_name'] == selected_clinic_name]
        doctor_specialties = sorted(set(doctor['specialist'] for doctor in filtered_specialties if doctor['status'] == "Approved"))
        self.doctor_specialty_dropdown['values'] = ["Choose Specialty", *doctor_specialties] if doctor_specialties else ["No specialties available"]
        self.doctor_specialty_dropdown.current(0)

    def update_doctor_dropdown(self, selected_clinic_name, selected_clinic_state, selected_specialty):
        doctors_ref = db.reference('doctors')
        doctors = doctors_ref.get()

        # Get the doctor names
        filtered_doctors = [doctor for doctor in doctors.values() if doctor['clinic_state'] == selected_clinic_state and doctor['clinic_name'] == selected_clinic_name and doctor['specialist'] == selected_specialty]
        doctor_names = sorted(set(doctor['username'] for doctor in filtered_doctors if doctor['status'] == "Approved"))
        self.doctor_name_dropdown['values'] = doctor_names if doctor_names else ["No doctors available"]
        self.doctor_name_dropdown.current(0)

    def check_date_selection(self, event):
        doctor_name = self.doctor_name_var.get()
        specialty = self.doctor_specialty_var.get()
        appointment_date = datetime.strptime(self.appointment_date_entry.get_date(), '%m/%d/%y').date()
        current_date = datetime.now(pytz.timezone('Asia/Kuala_Lumpur')).date()
        current_datetime = datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
        
        # Check if the selected date and time is in the past
        if appointment_date < current_date:
            messagebox.showerror("Error", "Past dates are not allowed. Please select a future date.")
            self.appointment_date_entry.selection_set(datetime.now())
            return
        elif appointment_date > current_date + relativedelta(months=6):
            messagebox.showerror("Error", "Appointments can only be booked within 6 months from the current date.")
            self.appointment_date_entry.selection_set(datetime.now())
            return

        if appointment_date == current_datetime.date() and current_datetime.time().hour >= 17:
            available_times = ["No Time Slot available"]
        
        elif appointment_date == current_datetime.date() and current_datetime.time().hour < 17:
            available_times = ["Choose Time Slot"]
            for i in range(9, 18):
                if current_datetime.time().hour < i:
                    if i < 10:
                        available_times.append(f"0{i}:00")
                    else:
                        available_times.append(f"{i}:00")
        else:
            available_times = ["Choose Time Slot"]
            for i in range(9, 18):
                if i < 10:
                    available_times.append(f"0{i}:00")
                else:
                    available_times.append(f"{i}:00")
        try:
            # Get the selected date
            appointment_date = datetime.strptime(self.appointment_date_entry.get_date(), '%m/%d/%y').date()

            # Query the database for appointments on the selected date with status "approved"
            appointments_ref = db.reference('appointment')
            appointments = appointments_ref.get()

            if appointments is not None:
                booked_times = []
                for appointment in appointments.values():
                    if appointment['appointment_date'] == appointment_date.strftime('%m/%d/%y') and appointment['status'] == 'Pending' and appointment['doctor_name'] == doctor_name and appointment['specialty'] == specialty:
                        booked_times.append(appointment['appointment_time'])

                # Remove the booked times from the list of available times
                for booked_time in booked_times:
                    if booked_time in available_times:
                        available_times.remove(booked_time)

            else:
                print("No appointments found for the selected date")

            # Update the values of self.appointment_time_entry with the updated list of available times
            self.appointment_time_entry['values'] = available_times
            self.appointment_time_entry.current(0)
        
        except Exception as e:
            print(f"An error occurred check date Selection: {e}")
            messagebox.showerror("Error", "An error occurred while checking the time selection")

    def check_time_selection(self, event):
        selected_time_slot = self.appointment_time_entry.get()

        current_time = datetime.now(pytz.timezone('Asia/Kuala_Lumpur')).time()
        if current_time.hour >= 17:
            available_times = ["No Time Slot Available"]
        else:
            available_times = ["Choose Time Slot"]
            for i in range(9, 18):
                if current_time.hour < i:
                    if i < 10:
                        available_times.append(f"0{i}:00")
                    else:
                        available_times.append(f"{i}:00")

        if selected_time_slot == "Choose Time Slot":
            messagebox.showerror("Error", "Please select an appointment time slot")
        
    def save_appointment(self, username, email, phone):
        try:
            tz = pytz.timezone('Asia/Kuala_Lumpur')
            current_date = datetime.now(tz)
            formatted_current_date = current_date.strftime('%m/%d/%Y %H:%M')
            username = username
            email = email
            phone = phone
            clinic_name = self.clinic_var.get()
            clinic_state = self.clinic_state_var.get()
            doctor_name = self.doctor_name_var.get()
            specialty = self.doctor_specialty_var.get()
            # convert the appointment date to a string dmy format
            appointment_date = datetime.strptime(self.appointment_date_entry.get_date(), '%m/%d/%y').date()
            appointment_date_str = appointment_date.strftime('%m/%d/%y')
            appointment_time = self.appointment_time_entry.get()            
            
            if appointment_time == "Choose Time Slot":
                messagebox.showerror("Error", "Please select an appointment time slot")
                return

            elif appointment_time == "No Time Slot Available":
                messagebox.showerror("Error", "No time slot available for the selected date. Please select another date.")
                return
            
            else: 
                # Check if the selected date and time is in the past
                selected_datetime = datetime.combine(appointment_date, datetime.strptime(appointment_time, '%H:%M').time(), tzinfo=tz)            
                if selected_datetime < current_date:
                    messagebox.showerror("Error", "Past dates are not allowed. Please select a future date.")
                    return
                elif selected_datetime > current_date + relativedelta(months=6):
                    messagebox.showerror("Error", "Appointments can only be booked within 6 months from the current date.")
                    return
            
            # Check if the selected date and time is already booked
            appointments_ref = db.reference('appointment')
            appointments = appointments_ref.get()

            if appointments is None:
                print("No appointments found for the selected date")
            else:
                for appointment in appointments.values():
                    if appointment['appointment_date'] == appointment_date.strftime('%m/%d/%y') and appointment['appointment_time'] == appointment_time and appointment['status'] == 'Pending' and appointment['doctor_name'] == doctor_name and appointment['specialty'] == specialty:
                        messagebox.showerror("Error", "This appointment date and time is already booked")
                        return
            
            matching_doctor_found = False

            doctors_ref = db.reference('doctors')

            # Retrieve the clinic data to check if the selected doctor belongs to the selected specialty
            doctors = doctors_ref.get()
            for doctor_id, doctor_data in doctors.items():
                if doctor_data.get('username')  == doctor_name and doctor_data.get('specialist') == specialty:
                    matching_doctor_found = True

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
                        'appointment_date': appointment_date_str,
                        'appointment_time': appointment_time,
                        'created_at': formatted_current_date,
                        'updated_at': formatted_current_date,
                        'status': 'Pending'
                    }) 
                    print("Appointment saved successfully")
                    messagebox.showinfo("Success", "Appointment apply successfully") 
                    
                    # clear the form
                    self.clinic_var.set("Choose Clinic")
                    self.clinic_state_var.set("Choose Clinic State")
                    self.doctor_name_var.set("Choose Doctor")
                    self.doctor_specialty_var.set("Choose Specialty")
                    self.appointment_date_entry.selection_set(datetime.now())
                    self.appointment_time_entry.set("Choose Time Slot")
                    break

            if not matching_doctor_found:
                print("Doctor not belong to the selected specialty.")
                messagebox.showerror("Error", "The Selected Doctor is not belong to the selected specialty. Please select the correct doctor and the specialty.")

        except Exception as e:
            print(f"An error occurred Save Appointment: {e}")
            messagebox.showerror("Error", "An error occurred while applying the appointment")

    def viewPrescriptionHistory(self):
        self.clearClinicInfo()
        self.clearFilters()

        # Create font style
        bold14 = Font(self.master, size=14, weight=BOLD) 
        bold12 = Font(self.master, size=12, weight=BOLD, family="Helvetica")
        bold10 = Font(self.master, size=10, weight=BOLD) 
        
        row = tk.Frame(self, bg="#F6F6E9")
        row.grid(sticky="w")

        label = tk.Label(self, text="Prescription History", bg="#F6F6E9", font=bold14)
        label.grid(row=0, column=0, pady=20, padx=10, sticky="w")

        # Get a reference to the prescriptions node in the database
        prescriptions_ref = db.reference('prescriptions')
        

        # Get the patienID
        patient_ref = db.reference('patients/' + self.patient_id)
        patient_data = patient_ref.get()
        patient_id = patient_data.get('patientID')

        # Retrieve the prescription data
        prescriptions = prescriptions_ref.order_by_child('patientID').get()
        # equal_to(str(self.patient_id))

        count = 0
        row = tk.Frame(self, bg="#F6F6E9")
        row.grid()

        # doctors.get(doctor_id).get('doctorName')

        for prescription, prescription_data in prescriptions.items():
            if prescription_data.get('patientID') == patient_id:
                prescrip_date = prescription_data.get('created_at')
                doctor_id = prescription_data.get('doctorID')
                doctor_ref = db.reference('doctors/' + doctor_id)
                doctor_data = doctor_ref.get()
                doctor_name = doctor_data.get('username')
                
                treatment = prescription_data.get('treatment')
                symptoms = prescription_data.get('symptoms')
                remark = prescription_data.get('remark')
                print(prescription_data)

                # Frame for each prescription
                prescrip_frame = tk.Frame(row, borderwidth=2, relief="groove", width=300, height=150)
                prescrip_frame.grid(row=count//2, column=count%2, padx=10, pady=30, sticky="w")

                # Prescription Date
                date_label_text = tk.Label(prescrip_frame, text="Date: ", font=bold12)
                date_label_text.grid(row=0, column=0, sticky="w", padx=5, pady=5)
                date_label_value = tk.Label(prescrip_frame, text=prescrip_date)
                date_label_value.grid(row=0, column=1, sticky="w", padx=5, pady=5)

                # Doctor 
                doctor_label_text = tk.Label(prescrip_frame, text="Doctor: ", font=bold12)
                doctor_label_text.grid(row=1, column=0, sticky="w", padx=5, pady=5)
                doctor_label_value = tk.Label(prescrip_frame, text=doctor_name)
                doctor_label_value.grid(row=1, column=1, sticky="w", padx=5, pady=5)

                # Treatement
                treatment_label_text = tk.Label(prescrip_frame, text="Treatment: ", font=bold12)
                treatment_label_text.grid(row=2, column=0, sticky="w", padx=5, pady=5)
                treatment_label_value = tk.Label(prescrip_frame, text=treatment)
                treatment_label_value.grid(row=2, column=1, sticky="w", padx=5, pady=5)

                # Symtomps
                symptoms_label_text = tk.Label(prescrip_frame, text="Symptoms: ", font=bold12)
                symptoms_label_text.grid(row=3, column=0, sticky="w", padx=5, pady=5)
                symptoms_label_value = tk.Label(prescrip_frame, text=symptoms)
                symptoms_label_value.grid(row=3, column=1, sticky="w", padx=5, pady=5)

                # Remark
                remark_label_text = tk.Label(prescrip_frame, text="Remark: ", font=bold12)
                remark_label_text.grid(row=4, column=0, sticky="w", padx=5, pady=5)
                remark_label_value = tk.Label(prescrip_frame, text=remark)
                remark_label_value.grid(row=4, column=1, sticky="w", padx=5, pady=5)

                count += 1

        # Update the total number of prescriptions found
        total_label = tk.Label(self, text=f"Total prescriptions found: {count}", bg="#F6F6E9", font=bold10)
        total_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")

    def appointmentRequest(self):
        status_window = tk.Toplevel(self)
        status_window.title("Appointment Status")
        
        status_window.configure(bg="#F6F6E9")

        status_label = tk.Label(status_window, text="Appointment Status", bg="#F6F6E9", font=("Arial", 14, "bold"))
        status_label.pack(pady=10)

        status_var = tk.StringVar()
        status_var.set("Pending")

        status_display = tk.Label(status_window, textvariable=status_var, bg="#FFFFFF", width=30, border=2, relief="groove")
        status_display.pack(pady=10)


        def update_status(self,appointmentNo):
            appointment_ref = db.reference('appointments/' + appointmentNo)
            appointment_data = appointment_ref.get()
            if appointment_data:
                status = appointment_data.get('status')
                status_var.set(status)
            status_window.after(10000, update_status)  

        update_status()     

    def logout(self):
        start_login()
        self.master.quit()

# Main Execution
if __name__ == "__main__":

    patient_id = sys.argv[1]

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
    app = PatientPage(second_frame, patient_id)  # Pass the second_frame window to your LoginPage class

    search_clinics_btn = tk.Button(nav_bar, text="Search Clinics", command=app.searchClinic)
    search_clinics_btn.pack(side="left", fill="x")

    make_appointment_btn = tk.Button(nav_bar, text="Make Appointment", command=lambda :app.makeAppointment(None, None, None, None))
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