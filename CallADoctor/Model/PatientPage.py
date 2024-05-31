import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, initialize_app ,db
from tkinter.font import BOLD, Font
import os
import subprocess
import PatientPage

# Create relative file paths
dir = os.path.dirname(__file__)

serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')   # Change the path to your own serviceAccountKey.json
logoImageFile = os.path.join(dir, '../Images/CallADoctor-logo-small.png')  # Change the path to your own logo image
backIconImage = os.path.join(dir, '../Images/back-icon.png') # Change the path to your own logo image

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

        for clinic_id, clinic_data in clinics.items():
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
        self.clinic_dropdown = ttk.Combobox(self, textvariable=self.clinic_var, values=clinic_options, state="readonly")
        self.clinic_dropdown.current(0)  # Set the default value to "All Clinic"
        self.clinic_dropdown.grid(row=2, column=0, pady=10, padx=200, sticky="w")

        submit_button = tk.Button(self, text="Search", bg="#0275DD", fg="#ffffff", command=self.displayClinicInfo)
        submit_button.grid(row=2, column=0, pady=10, padx=400, sticky="w")

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

                view_more_button = tk.Button(clinic_frame, text="View More",bg="#0275DD", fg="#ffffff", command=lambda clinic_id=clinic_id, clinic_name=clinic_name, clinic_state=clinic_state : self.doctorListFilter(clinic_id, clinic_name, clinic_state))
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
        print("doctorListFilter called")

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
        
        print("viewDoctorList called")  # Debugging print statement

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
        docotrs_ref = db.reference('doctors')

        # Retrieve the clinic data
        doctors = docotrs_ref.get()

        # Retrieve the clinic data
        for doctor_id, doctor_data in doctors.items():
            if doctor_id == search_doctor_id:
                doctor_name = doctor_data.get('username')
                doctor_phone = doctor_data.get('phone')
                doctor_email = doctor_data.get('email')
                doctor_specialty = doctor_data.get('specialist')
                clinic_name = doctor_data.get('clinic_name')
                clinic_state = doctor_data.get('clinic_state')

        # Start Filter Part - Filter by Doctor Specialty
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
        pass

    def viewPrescriptionHistory(self):
        pass

    def appointmentRequest(self):
        pass      

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
    my_canvas = tk.Canvas(main_frame, bg="#f6f6e9", height=600)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # Add a vertical scrollbar to the canvas
    my_scrollbar_vertival = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar_vertival.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas
    my_canvas.configure(yscrollcommand=my_scrollbar_vertival.set)

    # Create another frame inside the canvas
    second_frame = tk.Frame(my_canvas, bg="#f6f6e9", width=1200, height=600)

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

    app.pack(fill="both", expand=True)  # Make the LoginPage fill the entire window
    app.searchClinic()
    root.mainloop()  