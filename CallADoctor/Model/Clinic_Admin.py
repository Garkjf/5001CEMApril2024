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
        self.create_ui(parent, logo_path, admin_id)

    def fetch_appointments(self, clinic_name, clinic_state):
        # Fetch appointments from Firebase database
        ref = db.reference('appointment')
        appointments = ref.get()

        filtered_appointments = {}

        for appt_id, appt_info in appointments.items():
            appt_clinic_name = appt_info.get('clinic_name')
            appt_clinic_state = appt_info.get('clinic_state')
            appt_status = appt_info.get('status')

            if appt_clinic_name == clinic_name and appt_clinic_state == clinic_state and appt_status == 'Pending':
                # Filter out appointments that are already Accepted or Rejected
                filtered_appointments[appt_id] = appt_info

        return filtered_appointments

    def update_appointment_status(self, appt_id, status):
        # Update the appointment status in Firebase database
        ref = db.reference(f'appointment/{appt_id}')
        ref.update({'status': status})
        messagebox.showinfo("Info", f"Appointment {status} successfully!")
        
        # Refresh UI after updating status
        self.refresh_ui()

    def open_doctor_schedule(self, doctor_id):
        # Replace this with your logic to open the doctor's schedule
        print(f"Viewing schedule for doctor with ID: {doctor_id}")

    def create_ui(self, root, logo_path, admin_id):
        # Set the window title
        root.title("Admin Page")

        # Load the logo image
        logo_image = tk.PhotoImage(file=logo_path)
        logo_image = logo_image.subsample(2, 2)  # Resize if needed

        # Create a frame for the header
        header_frame = tk.Frame(root, bg='#f7f7eb')
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

        # Create a specific style for the "Patient Request" button
        style.configure('unactive.TButton', background='#9AB892')
        style.map('unactive.TButton',
                  foreground=[('active', 'white')],
                  background=[('active', '#82a383')],  # Slightly darker green for active state
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        # Open the doctor_list.py script using subprocess
        def open_doctor_list():
            for widget in root.winfo_children():
                widget.destroy()
            DoctorListPage(root, logo_path, admin_id)

        def open_patient_request():
            for widget in root.winfo_children():
                widget.destroy()
            PatientRequest(root, logo_path, admin_id)

        def start_login():
            self.parent.destroy()
            subprocess.Popen(["python", os.path.join(dir, 'Login.py')])

        # Add buttons to the header with switched positions
        btn_logout = ttk.Button(header_frame, text="Logout", style='unactive.TButton', command=start_login)
        btn_logout.pack(side=tk.RIGHT, padx=10, pady=10)
        btn_doctor_list = ttk.Button(header_frame, text="Doctor List", style='TButton', command=open_doctor_list)
        btn_doctor_list.pack(side=tk.RIGHT, padx=10, pady=10)
        btn_patient_request = ttk.Button(header_frame, text="Patient Request", style='unactive.TButton', command=open_patient_request)
        btn_patient_request.pack(side=tk.RIGHT, padx=10, pady=10)

        # Create a frame for the main content
        content_frame = tk.Frame(root, bg='#f7f7eb')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas to hold the appointment details with scrollbar attached
        canvas = tk.Canvas(content_frame, bg='#f7f7eb', yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure the scrollbar to work with the canvas
        scrollbar.config(command=canvas.yview)

        # Frame inside the canvas to contain the appointment details
        appointments_frame = tk.Frame(canvas, bg='#f7f7eb')
        appointments_frame.pack(fill=tk.BOTH, expand=True)

        # Attach the frame to the canvas
        canvas.create_window((0, 0), window=appointments_frame, anchor=tk.NW)

        clinic_ref = db.reference('clinicAdmins/' + admin_id)
        clinic_name = clinic_ref.get()['clinic_name']
        clinic_state = clinic_ref.get()['clinic_state']

        # Fetch appointments from Firebase
        appointments = self.fetch_appointments(clinic_name, clinic_state)
        # Add the title label to the content frame
        title_label = tk.Label(appointments_frame, text=f"{clinic_name} {clinic_state} Patient’s Request",
                               font=("Arial", 18, "bold"), bg='#f7f7eb')
        title_label.pack(padx=20, pady=20, anchor=tk.W)

        if appointments:
            # Display appointment details
            for appt_id, appt in appointments.items():
                frame = ttk.Frame(appointments_frame, padding="10", style="Card.TFrame")
                frame.pack(fill="x", pady=5, padx=10)

                doctor_ref = db.reference('doctors')
                doctor_data = doctor_ref.get()

                doctor_name = doctor_data.get('name')
                if doctor_name == appt.get('doctor_name'):
                    doctor_id = doctor_data[appt.get('doctor_id')]
                    admin_id = doctor_id

                brief_label_text = (
                    f"Requested at: {appt.get('created_at')}\n"
                    f"\n"
                    f"Clinic Name: {appt.get('clinic_name')}\n"
                    f"Doctor Name: {appt.get('doctor_name')}\n"
                    f"Appointment Date and Time: {appt.get('appointment_date')} - {appt.get('appointment_time')}"
                )
                brief_label = ttk.Label(frame, text=brief_label_text, style="Card.TLabel",
                                        justify="left", padding=(50, 5))
                brief_label.pack(fill="both")

                buttons_frame = ttk.Frame(frame)
                buttons_frame.pack(pady=5)

                view_button = ttk.Button(buttons_frame, text="View", command=lambda a=appt: self.view_appointment_details(root, a, logo_path, appt_id, admin_id), width=5)
                view_button.pack(side=tk.LEFT, padx=5)

                accept_button = ttk.Button(buttons_frame, text="Approve", command=lambda appt_id=appt_id: self.update_appointment_status(appt_id, "Accepted"))
                accept_button.pack(side=tk.LEFT, padx=5)

                reject_button = ttk.Button(buttons_frame, text="Reject", command=lambda appt_id=appt_id: self.update_appointment_status(appt_id, "Rejected"))
                reject_button.pack(side=tk.LEFT, padx=5)

        # Update the canvas scroll region when widgets are added
        appointments_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def refresh_ui(self):
        # Clear current UI and recreate with updated data
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.create_ui(self.parent, self.logo_path, self.admin_id)        

    def view_appointment_details(self, root, appt, logo_path, appt_id, admin_id):
        # Clear the current content
        for widget in root.winfo_children():
            widget.destroy()

        # Create a frame for the detailed view
        detail_frame = tk.Frame(root, bg='#f7f7eb')
        detail_frame.pack(fill=tk.BOTH, expand=True)

        # Ensure the header buttons and logo remain visible
        header_frame = tk.Frame(detail_frame, bg='#f7f7eb')
        header_frame.pack(fill=tk.X)

        # Load the logo image
        logo_image = tk.PhotoImage(file=logo_path)
        logo_image = logo_image.subsample(2, 2)  # Resize if needed

        # Add the logo to the header
        logo_label = tk.Label(header_frame, image=logo_image, bg='#f7f7eb')
        logo_label.image = logo_image  # Keep a reference to avoid garbage collection
        logo_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Open the doctor_list.py script using subprocess
        def open_doctor_list():
            for widget in root.winfo_children():
                widget.destroy()
            DoctorListPage(root, logo_path, admin_id)

        def open_patient_request():
            for widget in root.winfo_children():
                widget.destroy()
            PatientRequest(root, logo_path, admin_id)

        def start_login():
            self.parent.destroy()
            subprocess.Popen(["python", os.path.join(dir, 'Login.py')])

        # Add buttons to the header with switched positions
        btn_logout = ttk.Button(header_frame, text="Logout", style='unactive.TButton', command=start_login)
        btn_logout.pack(side=tk.RIGHT, padx=10, pady=10)
        btn_doctor_list = ttk.Button(header_frame, text="Doctor List", style='TButton', command=open_doctor_list)
        btn_doctor_list.pack(side=tk.RIGHT, padx=10, pady=10)
        btn_patient_request = ttk.Button(header_frame, text="Patient Request", style='unactive.TButton', command=open_patient_request)
        btn_patient_request.pack(side=tk.RIGHT, padx=10, pady=10)

        # Detailed appointment information
        info1 = (
            f"Requested at: {appt.get('created_at')}\n"
            f"Patient Name: {appt.get('patient_name')}\n"
            f"Patient Contact: {appt.get('patient_contact')}\n"
            f"Patient Email: {appt.get('patient_email')}\n"
            f"Description: {appt.get('description')}"
        )
        info_label1 = tk.Label(detail_frame, text=info1, anchor="w", justify=tk.LEFT, bg="white", width=132, height=5,
                               font=("Arial", 11))  # Adjust font size here
        info_label1.pack(anchor="w", padx=20, pady=(10, 5))

        info2 = (
            f"Appointment Detail:\n"
            f"Clinic Name: {appt.get('clinic_name')}\n"
            f"Doctor Name: {appt.get('doctor_name')}\n"
            f"Specialty: {appt.get('specialty')}\n"
            f"Date: {appt.get('appointment_date')}\n"
            f"Time: {appt.get('appointment_time')}\n"
            f"Status: {appt.get('status')}\n"
        )
        info_label2 = tk.Label(detail_frame, text=info2, anchor="w", justify=tk.LEFT, bg="white", width=132, height=8,
                               font=("Arial", 11))  # Adjust font size here
        info_label2.pack(anchor="w", padx=20, pady=(10, 5))

        # Add "View Doctor Schedule" button to view the doctor's schedule
        def view_doctor_schedule():
            # Replace with logic to fetch doctor ID and open schedule
            doctor_id = appt.get('doctor_id')  # Assuming doctor_id is stored in appointment data
            self.open_doctor_schedule(doctor_id)

        view_schedule_button = ttk.Button(detail_frame, text="View Doctor Schedule", command=view_doctor_schedule)
        view_schedule_button.pack(anchor="center", pady=20)

        # Add Accept and Reject buttons to the detailed view
        buttons_frame = ttk.Frame(detail_frame)
        buttons_frame.pack(pady=20)

        accept_button = ttk.Button(buttons_frame, text="Approve", command=lambda: self.update_appointment_status(appt_id, "Accepted"))
        accept_button.pack(side=tk.LEFT, padx=10)

        reject_button = ttk.Button(buttons_frame, text="Reject", command=lambda: self.update_appointment_status(appt_id, "Rejected"))
        reject_button.pack(side=tk.LEFT, padx=10)

        # Create a back button with an image
        backIconImage = os.path.join(dir, 'C:/Users/mwk02/OneDrive/Desktop/5001CEMApril2024-main/CallADoctor/Images/back-icon.png')  # Path to back icon image
        back_image = tk.PhotoImage(file=backIconImage)
        back_image = back_image.subsample(20, 20)  # Resize the image as needed

        back_button = tk.Button(header_frame, image=back_image, command=self.refresh_ui, bg='#f7f7eb', bd=0)
        back_button.image = back_image  # Keep a reference to avoid garbage collection
        back_button.pack(side=tk.TOP, anchor='ne', pady=10, padx=10)

        # Configure grid weights to ensure proper resizing
        detail_frame.grid_columnconfigure(0, weight=1)
        detail_frame.grid_rowconfigure(1, weight=1)


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
        self.load_doctors()

    def fetch_specialties(self):
        # Fetch specialties from the Firebase database
        ref = db.reference('specialties')
        return ref.get() or []

    def create_widgets(self):
        self.parent.title("Admin Page")

        # Load the logo image
        logo_image = tk.PhotoImage(file=self.logo_path)
        logo_image = logo_image.subsample(2, 2)

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

        btn_logout = ttk.Button(header_frame, text="Logout", style='unactive.TButton', command=start_login)
        btn_logout.pack(side=tk.RIGHT, padx=10, pady=10)
        btn_doctor_list = ttk.Button(header_frame, text="Doctor List", style='TButton', command=open_doctor_list)
        btn_doctor_list.pack(side=tk.RIGHT, padx=10, pady=10)
        btn_patient_request = ttk.Button(header_frame, text="Patient Request", style='unactive.TButton', command=open_patient_request)
        btn_patient_request.pack(side=tk.RIGHT, padx=10, pady=10)

        # Create a frame for the main content
        self.main_frame = tk.Frame(self.parent, bg='#f7f7eb')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create a frame for the columns
        self.columns_frame = tk.Frame(self.main_frame, bg='#f7f7eb')
        self.columns_frame.pack(fill=tk.BOTH, expand=True)

        # Create frames for Pending and Existing doctors
        self.pending_frame = tk.Frame(self.columns_frame, bg='#B2E7B1')
        self.pending_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.existing_frame = tk.Frame(self.columns_frame, bg='#E9B6A6')
        self.existing_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add labels to the frames
        pending_label = tk.Label(self.pending_frame, text="Add to Current Doctor List", font=("Arial", 16, "bold"), bg='#B2E7B1')
        pending_label.pack(pady=10)

        existing_label = tk.Label(self.existing_frame, text="Remove from Current Doctor List", font=("Arial", 16, "bold"), bg='#E9B6A6')
        existing_label.pack(pady=10)

        # Add scrollbars to each frame
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

        # Create a combobox for filtering by specialty
        self.specialty_var = tk.StringVar()
        self.specialty_combobox = ttk.Combobox(header_frame, textvariable=self.specialty_var, values=self.specialties)
        self.specialty_combobox.pack(side=tk.RIGHT, padx=10, pady=10)
        self.specialty_combobox.bind("<<ComboboxSelected>>", self.filter_doctors)

    def load_doctors(self):
        self.clear_content()
        ref = db.reference('doctors')
        doctors = ref.get()

        for doctor_id, doc_info in doctors.items():
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
            accept_button = ttk.Button(buttons_frame, text="Approved", command=lambda: self.accept_request(doctor_id))
            accept_button.pack(side=tk.LEFT, padx=5)

            reject_button = ttk.Button(buttons_frame, text="Reject", command=lambda: self.reject_request(doctor_id))
            reject_button.pack(side=tk.LEFT, padx=5)
        else:
            remove_button = ttk.Button(buttons_frame, text="Remove", command=lambda: self.remove_doctor(doctor_id))
            remove_button.pack(side=tk.LEFT, padx=5)

    def view_details(self, doctor_id):
        # Clear the main frame content
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ref = db.reference(f'doctors/{doctor_id}')
        doc_info = ref.get()

        # Create a back button with an image
        back_image = tk.PhotoImage(file=backIconImage)
        back_image = back_image.subsample(20, 20)  # Resize the image as needed
        back_button = tk.Button(self.main_frame, image=back_image, command=self.reinitialize_page, bg='#f7f7eb', bd=0)
        back_button.image = back_image  # Keep a reference to avoid garbage collection
        back_button.pack(side=tk.TOP, anchor='ne', pady=10, padx=10)

        # Display doctor details in the main frame
        DoctorDetail_label = ttk.Label(self.main_frame, text=f"Doctor Detail: ", font=("Arial", 14), background="#f7f7eb")
        DoctorDetail_label.pack(pady=10, anchor="w")

        name_label = ttk.Label(self.main_frame, text=f"Doctor Name: {doc_info.get('username')}", font=("Arial", 12), background="#f7f7eb")
        name_label.pack(pady=10, anchor="w")

        specialty_label = ttk.Label(self.main_frame, text=f"Speciality: {doc_info.get('specialist')}", font=("Arial", 12), background="#f7f7eb")
        specialty_label.pack(pady=10, anchor="w")

        ContactDetail_label = ttk.Label(self.main_frame, text=f"Contact Detail: ", font=("Arial", 14), background="#f7f7eb")
        ContactDetail_label.pack(pady=10, anchor="w")

        email_label = ttk.Label(self.main_frame, text=f"Email Address: {doc_info.get('email')}", font=("Arial", 12), background="#f7f7eb")
        email_label.pack(pady=10, anchor="w")

        # Assuming 'phone' is a field in your database for each doctor
        phone_label = ttk.Label(self.main_frame, text=f"Phone Number: {doc_info.get('phone')}", font=("Arial", 12), background="#f7f7eb")
        phone_label.pack(pady=10, anchor="w")

        if doc_info.get('status') == 'Pending':
            # Create a frame for the accept and reject buttons with a background color
            buttons_frame = ttk.Frame(self.main_frame, style='Background.TFrame')  # Use a custom style
            buttons_frame.pack(pady=10)

            # Define a custom style for the frame's background color (optional)
            style = ttk.Style()
            style.configure('Background.TFrame', background="#f7f7eb")  # Set desired background color

            accept_button = ttk.Button(buttons_frame, text="Approved    ", command=lambda: self.accept_request(doctor_id))
            accept_button.pack(side=tk.LEFT, padx=5)

            reject_button = ttk.Button(buttons_frame, text="Reject", command=lambda: self.reject_request(doctor_id))
            reject_button.pack(side=tk.LEFT, padx=5)


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
            if selected_specialty == "All" or doc_info.get('specialist') == selected_specialty:
                self.add_doctor_box(doctor_id, doc_info)

if __name__ == "__main__":
    root = tk.Tk()
    logo_path = logoImageFile
    admin_id = sys.argv[1]
    DoctorListPage(root, logo_path, admin_id)
    root.mainloop()
