import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys
from firebase_admin import credentials, initialize_app, db
import firebase_admin

# Set up paths
dir = os.path.dirname(__file__)
serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')
logoImageFile = os.path.join(dir,'C:/Users/mwk02/OneDrive/Desktop/5001CEMApril2024-main/CallADoctor/Images/CallADoctor-logo-small.png')  # Change the path to your own logo image
backIconImage = os.path.join(dir, 'C:/Users/mwk02/OneDrive/Desktop/5001CEMApril2024-main/CallADoctor/Images/back-icon.png') # Change the path to your own logo image

# Initialize Firebase
cred = credentials.Certificate(serviceAccountKeyFile)
initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})

class PatientRequest(tk.Frame):
    def __init__(self, parent, logo_path, admin_id):
        super().__init__(parent)
        self.parent = parent
        self.logo_path = logo_path
        self.admin_id = admin_id
        self.clinic_name = ""
        self.clinic_state = ""
        self.create_widgets()

    def create_widgets(self):
        self.parent.title("Patient Request Page")

        # Load the logo image
        logo_image = tk.PhotoImage(file=self.logo_path)
        logo_image = logo_image.subsample(2, 2)

        # Load the back icon image and resize
        self.back_icon_image = tk.PhotoImage(file=backIconImage)
        self.back_icon_image = self.back_icon_image.subsample(30, 30)  # Resizing the image by subsampling

        # Create a frame for the header
        header_frame = tk.Frame(self.parent, bg='#f7f7eb')
        header_frame.pack(fill=tk.X)

        # Add the logo to the header
        logo_label = tk.Label(header_frame, image=logo_image, bg='#f7f7eb')
        logo_label.image = logo_image  # Keep a reference to avoid garbage collection
        logo_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a style for the buttons
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=10, background='White')
        style.map('TButton',
                  foreground=[('active', 'white')],
                  background=[('active', '#5cb85c')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        style.configure('unactive.TButton', background='#9AB892')
        style.map('unactive.TButton',
                  foreground=[('active', 'white')],
                  background=[('active', '#82a383')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        def open_doctor_list():
            self.refresh_appointments()  # Refresh appointments when returning from Doctor List page
            for widget in self.parent.winfo_children():
                widget.destroy()
            DoctorListPage(self.parent, self.logo_path, self.admin_id)

        def open_patient_request():
            self.refresh_appointments()  # Refresh appointments when returning to Patient Request page
            for widget in self.parent.winfo_children():
                widget.destroy()
            PatientRequest(self.parent, self.logo_path, self.admin_id)

        def start_login():
            self.parent.destroy()
            subprocess.Popen(["python", os.path.join(dir, 'Login.py')])

        btn_logout = ttk.Button(header_frame, text="Logout", style='TButton', command=start_login)
        btn_logout.pack(side=tk.RIGHT, padx=10, pady=10)
        btn_doctor_list = ttk.Button(header_frame, text="Doctor List", style='TButton', command=open_doctor_list)
        btn_doctor_list.pack(side=tk.RIGHT, padx=10, pady=10)
        btn_patient_request = ttk.Button(header_frame, text="Patient Request", style='unactive.TButton', command=open_patient_request)
        btn_patient_request.pack(side=tk.RIGHT, padx=10, pady=10)

        # Create a frame for the main content
        self.main_frame = tk.Frame(self.parent, bg='#f7f7eb')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=1)

        # Create a frame for the patient requests
        self.requests_frame = tk.Frame(self.main_frame, bg='#f7f7eb')
        self.requests_frame.pack(fill=tk.X)  # Pack only horizontally, not expanding vertically

        # Fetch clinic details from Firebase
        clinic_ref = db.reference('clinicAdmins/' + self.admin_id)
        clinic_data = clinic_ref.get()

        if clinic_data:
            # Extract clinic name and state
            self.clinic_name = clinic_data.get('clinic_name', '')
            self.clinic_state = clinic_data.get('clinic_state', '')

            # Add a label for patient requests with dynamically fetched text
            requests_label_text = f"{self.clinic_name} {self.clinic_state} Patient’s Request"
            requests_label = tk.Label(self.requests_frame, text=requests_label_text, font=("Arial", 16, "bold"), bg='#f7f7eb')
            requests_label.pack(pady=10, padx=20)  # Add padding to the sides to keep the text from expanding

        # Create a canvas widget and associate it with a scrollbar
        self.canvas = tk.Canvas(self.main_frame, bg='#f7f7eb')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the patient requests
        self.patientrequest_frame = tk.Frame(self.canvas, bg='#f7f7eb')
        self.patientrequest_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.patientrequest_frame, anchor="nw")

        # Fetch appointment data from Firebase and display
        self.refresh_appointments()

    def refresh_appointments(self):
        # Clear existing appointment boxes
        for widget in self.patientrequest_frame.winfo_children():
            widget.destroy()

        # Reset the canvas's scroll position to the top
        self.canvas.yview_moveto(0)

        # Fetch appointment data from Firebase
        appointments_ref = db.reference('appointment')
        appointments = appointments_ref.get()

        if appointments:
            for appointment_id, appointment_info in appointments.items():
                # Check if the appointment status is "Pending" and if it matches the current clinic
                if (appointment_info['status'] == 'Pending' and
                    appointment_info.get('clinic_name') == self.clinic_name and
                    appointment_info.get('clinic_state') == self.clinic_state):
                    
                    # Create a box/frame for each appointment
                    appointment_box = ttk.Frame(self.patientrequest_frame, borderwidth=2, relief="groove", padding=10)
                    appointment_box.pack(fill=tk.BOTH, padx=30, pady=5)

                    # Display appointment details in the box
                    appointment_details = (
                        f"Created at: {appointment_info['created_at']}\n"
                        f"Clinic Name: {appointment_info['clinic_name']}\n"
                        f"Doctor Name: {appointment_info['doctor_name']}\n"
                        f"Specialty: {appointment_info['specialty']}\n"
                        f"Appointment Date and Time: {appointment_info['appointment_date']} - {appointment_info['appointment_time']}\n"
                        f"Status: {appointment_info['status']}\n"
                    )

                    appointment_label = tk.Label(appointment_box, text=appointment_details, font=("Arial", 12), bg='#f7f7eb', justify=tk.LEFT)
                    appointment_label.pack(pady=5, padx=5, anchor="w", fill=tk.BOTH)  # Align text to the left and fill the label box

                    # Button to view detailed information
                    view_button = ttk.Button(appointment_box, text="View Details", style='TButton', command=lambda app_id=appointment_id: self.view_appointment_details(app_id))
                    view_button.pack(side=tk.LEFT, padx=5, pady=5)

                    # Buttons for accepting and rejecting appointment
                    accept_button = ttk.Button(appointment_box, text="Accept", style='TButton', command=lambda app_id=appointment_id: self.accept_appointment(app_id))
                    accept_button.pack(side=tk.LEFT, padx=5, pady=5)
                    reject_button = ttk.Button(appointment_box, text="Reject", style='TButton', command=lambda app_id=appointment_id: self.reject_appointment(app_id))
                    reject_button.pack(side=tk.LEFT, padx=5, pady=5)

    def accept_appointment(self, appointment_id):
        # Update appointment status to "Accepted" in Firebase
        appointments_ref = db.reference('appointment')
        appointments_ref.child(appointment_id).update({'status': 'Accepted'})

        # Refresh appointment list
        self.refresh_appointments()

    def reject_appointment(self, appointment_id):
        # Update appointment status to "Rejected" in Firebase
        appointments_ref = db.reference('appointment')
        appointments_ref.child(appointment_id).update({'status': 'Rejected'})

        # Refresh appointment list
        self.refresh_appointments()

        # Update the scroll region of the canvas
        self.parent.update_idletasks()
        self.patientrequest_frame.update_idletasks()

    def view_appointment_details(self, appointment_id):
        # Clear appointment boxes
        for widget in self.patientrequest_frame.winfo_children():
            widget.destroy()
    
        # Fetch appointment details
        appointments_ref = db.reference('appointment')
        appointment_info = appointments_ref.child(appointment_id).get()

        back_button = ttk.Button(self.patientrequest_frame, image=self.back_icon_image, style='TButton', command=self.refresh_appointments)
        back_button.image = self.back_icon_image  # Keep a reference to avoid garbage collection
        back_button.pack(side=tk.TOP, anchor='ne', pady=1, padx=40)

        # Display detailed information
        details_text = (
            f"Created at: {appointment_info.get('created_at', '')}\n"
            f"Patient Information:\n"
            f"Patient Name: {appointment_info.get('username', '')}\n"
            f"Patient Email Address: {appointment_info.get('email', '')}\n"
            f"Patient Contact: {appointment_info.get('phone', '')}\n"
            f"\n"
            f"Appointment Detail:\n"
            f"Clinic Name: {appointment_info.get('clinic_name', '')}\n"
            f"Doctor Name: {appointment_info.get('doctor_name', '')}\n"
            f"Specialty: {appointment_info.get('specialty', '')}\n"
            f"Appointment Date and Time: {appointment_info.get('appointment_date', '')} - {appointment_info.get('appointment_time', '')}\n"
        )

        details_label = tk.Label(self.patientrequest_frame, text=details_text, font=("Arial", 12), bg='#f7f7eb', justify=tk.LEFT)
        details_label.pack(pady=10, padx=0, anchor="w", fill=tk.BOTH)

        # Buttons for accepting and rejecting appointment
        accept_button = ttk.Button(self.patientrequest_frame, text="Accept", style='TButton', command=lambda: self.accept_appointment(appointment_id))
        accept_button.pack(side=tk.LEFT, padx=5, pady=5)
        reject_button = ttk.Button(self.patientrequest_frame, text="Reject", style='TButton', command=lambda: self.reject_appointment(appointment_id))
        reject_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Button to view doctor schedule
        view_schedule_button = ttk.Button(self.patientrequest_frame, text="View Doctor Schedule", style='TButton', command=lambda: self.view_doctor_schedule(appointment_id))
        view_schedule_button.pack(side=tk.LEFT, padx=5, pady=5)

    def view_doctor_schedule(self, appointment_id):
        # Clear appointment boxes
        for widget in self.patientrequest_frame.winfo_children():
            widget.destroy()

        # Fetch appointment details
        appointments_ref = db.reference('appointment')
        appointment_info = appointments_ref.child(appointment_id).get()

        # Fetch doctor details based on doctor_name from appointment_info
        doctor_name = appointment_info.get('doctor_name')
        doctors_ref = db.reference('doctors')
        doctor_data = None

        # Find the doctor with matching username (doctor_name)
        for doc_id, doc_info in doctors_ref.get().items():
            if doc_info.get('username') == doctor_name:
                doctor_data = doc_info
                break

        if doctor_data:
            # Button to go back to appointment details
            back_button = ttk.Button(self.patientrequest_frame, image=self.back_icon_image, style='TButton', command=lambda: self.view_appointment_details(appointment_id))
            back_button.image = self.back_icon_image  # Keep a reference to avoid garbage collection
            back_button.pack(side=tk.TOP, anchor='ne', pady=1, padx=1)

            # Display doctor information
            DoctorDetail_label = ttk.Label(self.patientrequest_frame, text=f"Doctor Detail: ", font=("Arial", 14), background="#f7f7eb")
            DoctorDetail_label.pack(pady=10, anchor="w")

            name_label = ttk.Label(self.patientrequest_frame, text=f"Doctor Name: {doctor_data.get('username')}", font=("Arial", 12), background="#f7f7eb")
            name_label.pack(pady=10, anchor="w")

            specialty_label = ttk.Label(self.patientrequest_frame, text=f"Speciality: {doctor_data.get('specialist')}", font=("Arial", 12), background="#f7f7eb")
            specialty_label.pack(pady=10, anchor="w")

            ContactDetail_label = ttk.Label(self.patientrequest_frame, text=f"Contact Detail: ", font=("Arial", 14), background="#f7f7eb")
            ContactDetail_label.pack(pady=10, anchor="w")

            email_label = ttk.Label(self.patientrequest_frame, text=f"Email Address: {doctor_data.get('email')}", font=("Arial", 12), background="#f7f7eb")
            email_label.pack(pady=10, anchor="w")

            phone_label = ttk.Label(self.patientrequest_frame, text=f"Phone Number: {doctor_data.get('phone')}", font=("Arial", 12), background="#f7f7eb")
            phone_label.pack(pady=10, anchor="w")

            # Create Treeview for doctor's appointments
            columns = ('Patient Name', 'Appointment Date and Time', 'Status')
            tree = ttk.Treeview(self.patientrequest_frame, columns=columns, show='headings')

            # Define column headings
            for col in columns:
                tree.heading(col, text=col)

            # Insert appointment data into Treeview
            for app_id, app_info in appointments_ref.get().items():
                if app_info.get('doctor_name') == doctor_name:
                    tree.insert('', 'end', values=(
                        app_info.get('username', ''),
                        f"{app_info.get('appointment_date', '')} {app_info.get('appointment_time', '')}",
                        app_info.get('status', '')
                    ))

            tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)



class DoctorListPage(tk.Frame):
    def __init__(self, parent, logo_path, admin_id):
        super().__init__(parent)
        self.parent = parent
        self.logo_path = logo_path
        self.admin_id = admin_id
        self.specialties = [
            "All", "Cardiology", "Dermatology", "Endocrinology", "Gastroenterology", 
            "Neurology", "Oncology", "Pediatrics", "Psychiatry", "Radiology", "Urology"
        ]
        self.create_widgets()
        self.clinic = db.reference('clinicAdmins/' + admin_id).get()
        self.load_doctors()
        self.doctors = db.reference('doctors').get()

    def fetch_specialties(self):
        ref = db.reference('specialties')
        return ref.get() or []

    def create_widgets(self):
        self.parent.title("Admin Page")

        # Logo setup
        logo_image = tk.PhotoImage(file=self.logo_path)
        logo_image = logo_image.subsample(2, 2)
        header_frame = tk.Frame(self.parent, bg='#f7f7eb')
        header_frame.pack(fill=tk.X)
        logo_label = tk.Label(header_frame, image=logo_image, bg='#f7f7eb')
        logo_label.image = logo_image
        logo_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Styling setup
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=10, background='White')
        style.map('TButton',
                  foreground=[('active', 'white')],
                  background=[('active', '#5cb85c')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        style.configure('unactive.TButton', background='#9AB892')
        style.map('unactive.TButton',
                  foreground=[('active', 'white')],
                  background=[('active', '#82a383')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        # Navigation buttons
        def open_doctor_list():
            for widget in self.parent.winfo_children():
                widget.destroy()
            DoctorListPage(self.parent, self.logo_path, self.admin_id)

        def open_patient_request():
            for widget in self.parent.winfo_children():
                widget.destroy()
            PatientRequest(self.parent, self.logo_path, self.admin_id)

        def start_login():
            self.parent.destroy()
            subprocess.Popen(["python", os.path.join(dir, 'Login.py')])

        btn_logout = ttk.Button(header_frame, text="Logout", style='TButton', command=start_login)
        btn_logout.pack(side=tk.RIGHT, padx=10, pady=10)
        btn_doctor_list = ttk.Button(header_frame, text="Doctor List", style='unactive.TButton', command=open_doctor_list)
        btn_doctor_list.pack(side=tk.RIGHT, padx=10, pady=10)
        btn_patient_request = ttk.Button(header_frame, text="Patient Request", style='TButton', command=open_patient_request)
        btn_patient_request.pack(side=tk.RIGHT, padx=10, pady=10)

        # Main frame setup
        self.main_frame = tk.Frame(self.parent, bg='#f7f7eb')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.columns_frame = tk.Frame(self.main_frame, bg='#f7f7eb')
        self.columns_frame.pack(fill=tk.BOTH, expand=True)
        self.pending_frame = tk.Frame(self.columns_frame, bg='#B2E7B1')
        self.pending_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.existing_frame = tk.Frame(self.columns_frame, bg='#E9B6A6')
        self.existing_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        pending_label = tk.Label(self.pending_frame, text="Add to Current Doctor List", font=("Arial", 16, "bold"), bg='#B2E7B1')
        pending_label.pack(pady=10)
        existing_label = tk.Label(self.existing_frame, text="Remove from Current Doctor List", font=("Arial", 16, "bold"), bg='#E9B6A6')
        existing_label.pack(pady=10)

        # Scrollbars setup
        pending_scrollbar = ttk.Scrollbar(self.pending_frame, orient=tk.VERTICAL)
        pending_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        existing_scrollbar = ttk.Scrollbar(self.existing_frame, orient=tk.VERTICAL)
        existing_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.pending_canvas = tk.Canvas(self.pending_frame, yscrollcommand=pending_scrollbar.set, bg='#B2E7B1')
        self.pending_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.existing_canvas = tk.Canvas(self.existing_frame, yscrollcommand=existing_scrollbar.set, bg='#E9B6A6')
        self.existing_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        pending_scrollbar.config(command=self.pending_canvas.yview)
        existing_scrollbar.config(command=self.existing_canvas.yview)

        self.pending_content = tk.Frame(self.pending_canvas, bg='#B2E7B1')
        self.existing_content = tk.Frame(self.existing_canvas, bg='#E9B6A6')
        self.pending_canvas.create_window((0, 0), window=self.pending_content, anchor=tk.NW)
        self.existing_canvas.create_window((0, 0), window=self.existing_content, anchor=tk.NW)

        self.pending_content.bind("<Configure>", lambda e: self.pending_canvas.configure(scrollregion=self.pending_canvas.bbox("all")))
        self.existing_content.bind("<Configure>", lambda e: self.existing_canvas.configure(scrollregion=self.existing_canvas.bbox("all")))

        # Filter by specialist setup
        filter_label = ttk.Label(header_frame, text="Filter by Specialist", font=("Arial", 12), background="#f7f7eb")
        filter_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.specialty_var = tk.StringVar()
        self.specialty_combobox = ttk.Combobox(header_frame, textvariable=self.specialty_var, values=self.specialties)
        self.specialty_combobox.pack(side=tk.RIGHT, padx=10, pady=10)
        self.specialty_combobox.bind("<<ComboboxSelected>>", self.filter_doctors)

    def load_doctors(self):
        self.clear_content()
        ref = db.reference('doctors')
        doctors = ref.get()

        for doctor_id, doc_info in doctors.items():
            if doc_info.get('clinic_name') == self.clinic['clinic_name'] and doc_info.get('clinic_state') == self.clinic['clinic_state']:
                self.add_doctor_box(doctor_id, doc_info)

    def clear_content(self):
        for widget in self.pending_content.winfo_children():
            widget.destroy()
        for widget in self.existing_content.winfo_children():
            widget.destroy()

    def add_doctor_box(self, doctor_id, doc_info):
        frame = ttk.Frame(self.pending_content if doc_info.get('status') == 'Pending' else self.existing_content,
                          padding="10", style="Card.TFrame")
        frame.pack(fill="x", pady=5, padx=10)

        brief_label_text = (
            f"Doctor Name: {doc_info.get('username')}\n"
            f"Specialist: {doc_info.get('specialist')}\n"
        )

        brief_label = ttk.Label(frame, text=brief_label_text, style="Card.TLabel",
                                justify="left", padding=(50, 5))
        brief_label.pack(fill="both")

        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(pady=5)

        view_button = ttk.Button(buttons_frame, text="View", command=lambda: self.view_details(doctor_id), width=5)
        view_button.pack(side=tk.LEFT, padx=5)

        if doc_info.get('status') == 'Pending':
            accept_button = ttk.Button(buttons_frame, text="Approve", command=lambda: self.accept_request(doctor_id))
            accept_button.pack(side=tk.LEFT, padx=5)

            reject_button = ttk.Button(buttons_frame, text="Reject", command=lambda: self.reject_request(doctor_id))
            reject_button.pack(side=tk.LEFT, padx=5)
        else:
            remove_button = ttk.Button(buttons_frame, text="Remove", command=lambda: self.remove_doctor(doctor_id))
            remove_button.pack(side=tk.LEFT, padx=5)

    def view_details(self, doctor_id):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        doctor_data = db.reference('doctors/' + doctor_id).get()

        back_image = tk.PhotoImage(file=backIconImage)
        back_image = back_image.subsample(20, 20)
        back_button = tk.Button(self.main_frame, image=back_image, command=self.reinitialize_page, bg='#f7f7eb', bd=0)
        back_button.image = back_image
        back_button.pack(side=tk.TOP, anchor='ne', pady=10, padx=10)

        DoctorDetail_label = ttk.Label(self.main_frame, text="Doctor Detail: ", font=("Arial", 14), background="#f7f7eb")
        DoctorDetail_label.pack(pady=10, anchor="w")

        name_label = ttk.Label(self.main_frame, text=f"Doctor Name: {doctor_data.get('username')}", font=("Arial", 12), background="#f7f7eb")
        name_label.pack(pady=10, anchor="w")

        specialty_label = ttk.Label(self.main_frame, text=f"Specialty: {doctor_data.get('specialist')}", font=("Arial", 12), background="#f7f7eb")
        specialty_label.pack(pady=10, anchor="w")

        ContactDetail_label = ttk.Label(self.main_frame, text="Contact Detail: ", font=("Arial", 14), background="#f7f7eb")
        ContactDetail_label.pack(pady=10, anchor="w")

        email_label = ttk.Label(self.main_frame, text=f"Email Address: {doctor_data.get('email')}", font=("Arial", 12), background="#f7f7eb")
        email_label.pack(pady=10, anchor="w")

        phone_label = ttk.Label(self.main_frame, text=f"Phone Number: {doctor_data.get('phone')}", font=("Arial", 12), background="#f7f7eb")
        phone_label.pack(pady=10, anchor="w")

        # Create Treeview for doctor's appointments
        columns = ('Patient Name', 'Appointment Date and Time', 'Status')
        tree = ttk.Treeview(self.main_frame, columns=columns, show='headings')

        # Define column headings
        for col in columns:
            tree.heading(col, text=col)

        # Fetch and insert appointment data into Treeview
        appointments_ref = db.reference('appointment')
        for app_id, app_info in appointments_ref.get().items():
            if app_info.get('doctor_name') == doctor_data.get('username'):
                tree.insert('', 'end', values=(
                    app_info.get('username', ''),
                    f"{app_info.get('appointment_date', '')} {app_info.get('appointment_time', '')}",
                    app_info.get('status', '')
                ))

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)


    def reinitialize_page(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        DoctorListPage(self.parent, self.logo_path, self.admin_id)

    def accept_request(self, doctor_id):
        ref = db.reference(f'doctors/{doctor_id}')
        ref.update({'status': 'Existing'})
        self.load_doctors()

    def reject_request(self, doctor_id):
        ref = db.reference(f'doctors/{doctor_id}')
        ref.delete()
        self.load_doctors()

    def remove_doctor(self, doctor_id):
        ref = db.reference(f'doctors/{doctor_id}')
        ref.update({'status': 'Pending'})
        self.load_doctors()

    def filter_doctors(self, event):
        selected_specialty = self.specialty_var.get()
        ref = db.reference('doctors')
        doctors = ref.get()

        self.clear_content()

        for doctor_id, doc_info in doctors.items():
            if doc_info.get('clinic_name') == self.clinic['clinic_name'] and doc_info.get('clinic_state') == self.clinic['clinic_state']:
                if selected_specialty == "All" or doc_info.get('specialist') == selected_specialty:
                    self.add_doctor_box(doctor_id, doc_info)


if __name__ == "__main__":
    root = tk.Tk()
    logo_path = logoImageFile
    admin_id = sys.argv[1]
    DoctorListPage(root, logo_path, admin_id)
    root.mainloop()
