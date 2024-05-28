import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, initialize_app ,db
from tkinter.font import BOLD, Font
import os
import subprocess
import Patient

# Create relative file paths
dir = os.path.dirname(__file__)

serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')   # Change the path to your own serviceAccountKey.json
logoImageFile = os.path.join(dir, '../Images/CallADoctor-logo.png')  # Change the path to your own logo image
backIconImage = os.path.join(dir, '../Images/back-icon.png') # Change the path to your own logo image

class Patient(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#9AB892")
        cred = credentials.Certificate(serviceAccountKeyFile)
        initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})

    def searchClinic(self):
        self.clearClinicInfo()  
        self.clearFilters()
        bold14 = Font(self.master, size=14, weight=BOLD) 
        bold10 = Font(self.master, size=10, weight=BOLD) 
        label = tk.Label(self, text="Search For Clinics", bg="#F6F6E9", font=bold14)
        label.pack(padx=20, pady=(10, 0), anchor="w")

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
        self.label = tk.Label(self, text="Filter by Clinic State", bg="#9AB892", font=bold10)
        self.label.pack(pady=(10), padx=(10), anchor="w")  
        self.clinic_state_dropdown = ttk.Combobox(self, textvariable=self.clinic_state_var, values=clinic_state_options, state="readonly")
        self.clinic_state_dropdown.current(0)  # Set the default value to "All State"
        self.clinic_state_dropdown.pack(pady=(10), padx=(10), anchor="w") 

        # Clinic name Selection
        self.clinic_var = tk.StringVar()
        self.label = tk.Label(self, text="Filter by Clinic Name", bg="#9AB892", font=bold10)
        self.label.pack(pady=(10), padx=(10), anchor="w")
        self.clinic_dropdown = ttk.Combobox(self, textvariable=self.clinic_var, values=clinic_options, state="readonly")
        self.clinic_dropdown.current(0)  # Set the default value to "All Clinic"
        self.clinic_dropdown.pack(pady=(10), padx=(10), anchor="w")

        submit_button = tk.Button(self, text="Search", bg="#0275DD", fg="#ffffff", command=self.displayClinicInfo)
        submit_button.pack(pady=(10), padx=(10), anchor="w")

        # initialize the total clinic found label
        self.total_label = tk.Label(self, text="Total clinics found: 0")
        self.total_label.pack(pady=(5), padx=(10), anchor="w")

        self.displayClinicInfo()

    def displayClinicInfo(self):
        # Clear the clinic information
        self.clearClinicInfo()

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
        row = tk.Frame(self, bg="#9AB892")
        row.pack()

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
                clinic_frame = tk.Frame(row, borderwidth=2, relief="groove", width=300, height=100)
                clinic_frame.pack(side="left", padx=10, pady=30)

                name_label = tk.Label(clinic_frame, text=f"Clinic Name: {clinic_name}")
                name_label.pack()

                state_label = tk.Label(clinic_frame, text=f"Clinic State: {clinic_state}")
                state_label.pack()

                view_more_button = tk.Button(clinic_frame, text="View More",bg="#0275DD", fg="#ffffff", command=lambda clinic_id=clinic_id, clinic_name=clinic_name, clinic_state=clinic_state : self.doctorListFilter(clinic_id, clinic_name, clinic_state))
                view_more_button.pack()

                count += 1

            if count % 4 == 0:
                row = tk.Frame(self, bg="#9AB892")
                row.pack()

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
        label = tk.Label(self, text=f"Search For {selected_clinic} - {selected_state} Doctors", bg="#F6F6E9", font=bold14)
        label.pack(padx=20, pady=(10, 0), anchor="w")

        # Load the back icon
        back_icon = tk.PhotoImage(file=backIconImage)
        back_icon = back_icon.subsample(20, 20)

        # Back button
        back_button = tk.Button(self, image=back_icon, command=self.searchClinic)
        back_button.image = back_icon  # Keep a reference to the image to prevent it from being garbage collected
        back_button.pack(pady=(5), padx=(320), anchor="w")

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
        self.label = tk.Label(self, text="Filter by Doctor Specialty", bg="#9AB892", font=bold10)
        self.label.pack(pady=(10), padx=(10), anchor="w")  
        self.clinic_state_dropdown = ttk.Combobox(self, textvariable=self.doctor_specialty_var, values=doctor_specialty_options, state="readonly")
        self.clinic_state_dropdown.current(0)  # Set the default value to "All specialty"
        self.clinic_state_dropdown.pack(pady=(10), padx=(10), anchor="w") 

        submit_button = tk.Button(self, text="Search", bg="#0275DD", fg="#ffffff", command=lambda: self.viewDoctorList(clinic_id, selected_clinic, selected_state, self.doctor_specialty_var.get()))
        submit_button.pack(pady=(10), padx=(10), anchor="w")
        # End Filter Part - Filter by Doctor Specialty

        # initialize the total doctor found label
        self.total_label = tk.Label(self, text="Total doctor found: 0")
        self.total_label.pack(padx=(10), anchor="w")

        self.viewDoctorList(clinic_id, selected_clinic, selected_state, self.doctor_specialty_var.get())

    def viewDoctorList(self, clinic_id, selected_clinic, selected_state, selected_specialty):
        # Clear the clinic information
        self.clearClinicInfo()
        print("viewDoctorList called")  # Debugging print statement

        # Get the selected clinic state and clinic name
        print(f"Selected state: {selected_state}, Selected clinic: {selected_clinic}")  # Debugging print statement

        # Get a reference to the doctors node in the database
        doctors_ref = db.reference('doctors')

        # Retrieve the doctors data
        doctors = doctors_ref.get()
        print(f"doctors: {doctors}") # Debugging print statement

        # Display the clinic information
        count = 0
        row = tk.Frame(self, bg="#9AB892")
        row.pack()
        
        # Display the related doctors
        for doctor_id, doctor_data in doctors.items():
            if doctor_data.get('clinic_state')  == selected_state and doctor_data.get('clinic_name') == selected_clinic and (doctor_data.get('specialist') == selected_specialty or selected_specialty == "All Specialty"):
                print(f"Match found for doctor {doctor_id}")  # Debugging print statement

                clinic_frame = tk.Frame(row, borderwidth=2, relief="groove", width=300, height=100)
                clinic_frame.pack(side="left", padx=10, pady=30)

                doctor_name = doctor_data.get('username')
                doctor_specialty = doctor_data.get('specialist')

                doctor_label = tk.Label(clinic_frame, text=f"Doctor: {doctor_name}")
                doctor_label.pack()

                specialty_label = tk.Label(clinic_frame, text=f"Specialty: {doctor_specialty}")
                specialty_label.pack()

                view_more_button = tk.Button(clinic_frame, text="View More", bg="#0275DD", fg="#ffffff", command=lambda clinic_id=doctor_id: self.viewDoctor(doctor_id, selected_clinic, selected_state))
                view_more_button.pack()

                count += 1

            if count % 4 == 0:
                row = tk.Frame(self, bg="#9AB892")
                row.pack()

        # Update the total number of doctor found
        self.total_label.config(text=f"Total doctors found: {count}")   

    def viewDoctorInformation(self, doctor_id):          
        # Clear the doctor information
        self.viewDoctorList()
        self.clearFilters()
        print("viewDoctorInformation called")  # Debugging print statement

        # Start Filter Part - Filter by Doctor Specialty
        bold14 = Font(self.master, size=14, weight=BOLD) 
        bold10 = Font(self.master, size=10, weight=BOLD) 
        label = tk.Label(self, text=f"Search For {selected_clinic} {selected_state} Doctors", bg="#F6F6E9", font=bold14)
        label.pack(padx=20, pady=(10, 0), anchor="w")

        # Load the back icon
        back_icon = tk.PhotoImage(file=backIconImage)
        back_icon = back_icon.subsample(15, 15)

        # Back button
        back_button = tk.Button(self, image=back_icon, command=self.searchClinic)
        back_button.image = back_icon  # Keep a reference to the image to prevent it from being garbage collected
        back_button.pack(padx=(300), anchor="w")

        # Get a reference to the doctors node in the database
        docotrs_ref = db.reference('doctors')

        # Retrieve the clinic data
        doctors = docotrs_ref.get()

        # Doctor selection
        doctor_specialty_options = ["All Specialty"]
        doctor_specialties = set()

        for doctor_id, doctor_data in doctors.items():
            specialist = doctor_data.get('specialist')
            if specialist not in doctor_specialties:
                doctor_specialty_options.append(specialist)
                doctor_specialties.add(specialist)
           
        # Doctor Specialty Selection
        self.doctor_specialty_var = tk.StringVar()
        self.label = tk.Label(self, text="Filter by Doctor Specialty", bg="#9AB892", font=bold10)
        self.label.pack(pady=(10), padx=(10), anchor="w")  
        self.clinic_state_dropdown = ttk.Combobox(self, textvariable=self.doctor_specialty_var, values=doctor_specialty_options, state="readonly")
        self.clinic_state_dropdown.current(0)  # Set the default value to "All specialty"
        self.clinic_state_dropdown.pack(pady=(10), padx=(10), anchor="w") 

        submit_button = tk.Button(self, text="Search", bg="#0275DD", fg="#ffffff", command=self.viewDoctorList)
        submit_button.pack(pady=(10), padx=(10), anchor="w")
        # End Filter Part - Filter by Doctor Specialty

        # initialize the total doctor found label
        self.total_label = tk.Label(self, text="Total doctor found: 0")
        self.total_label.pack(pady=(5), padx=(10), anchor="w")

        # Get the selected clinic state and clinic name
        # selected_state = clinic_state
        # selected_clinic = clinic_name
        print(f"Selected state: {selected_state}, Selected clinic: {selected_clinic}")  # Debugging print statement

        # Get a reference to the doctors node in the database
        doctors_ref = db.reference('doctors')

        # Retrieve the doctors data
        doctors = doctors_ref.get()
        print(f"doctors: {doctors}") # Debugging print statement

        # Display the clinic information
        count = 0
        row = tk.Frame(self, bg="#9AB892")
        row.pack()
        
        # Display the related doctors
        for doctor_id, doctor_data in doctors.items():
            if doctor_data.get('clinic_state')  == selected_state and doctor_data.get('clinic_name') == selected_clinic:
                print(f"Match found for doctor {doctor_id}")  # Debugging print statement

                clinic_frame = tk.Frame(row, borderwidth=2, relief="groove", width=300, height=100)
                clinic_frame.pack(side="left", padx=10, pady=30)

                doctor_name = doctor_data.get('username')
                doctor_specialty = doctor_data.get('specialist')

                doctor_label = tk.Label(clinic_frame, text=f"Doctor: {doctor_name}")
                doctor_label.pack()

                specialty_label = tk.Label(clinic_frame, text=f"Specialty: {doctor_specialty}")
                specialty_label.pack()

                view_more_button = tk.Button(clinic_frame, text="View More", bg="#0275DD", fg="#ffffff", command=lambda clinic_id=doctor_id: self.viewDoctor(doctor_id))
                view_more_button.pack()

                count += 1

            if count % 4 == 0:
                row = tk.Frame(self, bg="#9AB892")
                row.pack()

        # Update the total number of doctor found
        self.total_label.config(text=f"Total doctors found: {count}") 
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
    root.geometry("750x550")
    
    # Body
    app = Patient(root)  # Pass the root window to your LoginPage class
       # Header
    logo = tk.PhotoImage(file=logoImageFile)
    logo = logo.subsample(4, 4)
    logo_label = tk.Label(image=logo, bg="#F6F6E9")
    # navigation bar
    nav_bar = tk.Frame(bg="#6B9778")
    nav_bar.pack()

    search_clinics_btn = tk.Button(nav_bar, text="Search Clinics", command=app.searchClinic)
    search_clinics_btn.pack(side="left")

    make_appointment_btn = tk.Button(nav_bar, text="Make Appointment", command=app.makeAppointment)
    make_appointment_btn.pack(side="left")

    prescription_btn = tk.Button(nav_bar, text="Prescription", command=app.viewPrescriptionHistory)
    prescription_btn.pack(side="left")

    appointment_request_btn = tk.Button(nav_bar, text="Appointment Request", command=app.appointmentRequest)
    appointment_request_btn.pack(side="left")
    app.pack(fill="both", expand=True)  # Make the LoginPage fill the entire window
    app.searchClinic()
    root.mainloop()  