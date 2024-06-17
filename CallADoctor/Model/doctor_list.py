import tkinter as tk
from tkinter import ttk, messagebox
import os
import firebase_admin
from firebase_admin import credentials, initialize_app, db
import subprocess
import sys

# Set up paths
dir = os.path.dirname(__file__)
serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')
logoImageFile = os.path.join(dir, '../Images/CallADoctor-logo.png')  # Change the path to your own logo image
backIconImage = os.path.join(dir, '../Images/back-icon.png') # Change the path to your own logo image

# Initialize Firebase
cred = credentials.Certificate(serviceAccountKeyFile)
initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})

class DoctorListPage(tk.Frame):
    def __init__(self, parent, logo_path, admin_id):
        super().__init__(parent, bg="#9AB892")
        self.admin_id = admin_id
        self.parent = parent
        self.logo_path = logo_path

        self.doctors = db.reference('doctors').get()
        self.clinic = db.reference('clinicAdmins/' + admin_id).get()
        clinic_name = self.clinic.get("clinic_name")
        clinic_state = self.clinic.get("state")
        specialties = []

        for doctor_id, doctor_data in self.doctors.items():
            if doctor_data.get("clinic_name") == clinic_name and doctor_data.get("state") == clinic_state:
                specialties.extend([doctor_data.get("specialist")])

        self.specialties = ["All"] + specialties
        self.selected_specialty = tk.StringVar(value="All")
        self.create_widgets()
        self.load_doctors()

    def create_widgets(self):
        # Create a frame for the header
        header_frame = tk.Frame(self.parent, bg='#f7f7eb')
        header_frame.pack(fill=tk.X)

        # Load the logo image
        logo_image = tk.PhotoImage(file=self.logo_path)
        logo_image = logo_image.subsample(2,2)  # Resize if needed

        # Add the logo to the header
        logo_label = tk.Label(header_frame, image=logo_image, bg='#f7f7eb')
        logo_label.image = logo_image  # Keep a reference to avoid garbage collection
        logo_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Add buttons to the header
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=10, background='#9AB892')
        style.map('TButton',
              foreground=[('active', 'white')],
              background=[('active', '#5cb85c')],
              relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        
        style.configure('PatientRequest.TButton', background='White')
        style.map('PatientRequest.TButton',
                foreground=[('active', 'white')],
                background=[('active', 'white')],  # Slightly darker green for active state
                relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
       
        # Open the doctor_list.py script using subprocess
        def open_doctor_list(admin_id):
            subprocess.Popen(['python', os.path.join(dir, 'doctor_list.py')] + [admin_id])

        def open_patient_request(admin_id):
            subprocess.Popen(['python', os.path.join(dir, 'patient_request.py')] + [admin_id])

        def start_login():
            subprocess.Popen(["python", os.path.join(dir, 'Login.py')])

        # Add buttons to the header with switched positions
        btn_logout = ttk.Button(header_frame, text="Logout", style='unactive.TButton', command=start_login)
        btn_logout.pack(side=tk.RIGHT, padx=10, pady=10)
        btn_doctor_list = ttk.Button(header_frame, text="Doctor List", style='TButton', command=lambda: open_doctor_list(self.admin_id))
        btn_doctor_list.pack(side=tk.RIGHT, padx=10, pady=10)
        btn_patient_request = ttk.Button(header_frame, text="Patient Request", style='TButton', command=lambda :open_patient_request(self.admin_id))
        btn_patient_request.pack(side=tk.RIGHT, padx=10, pady=10)

        # Create a frame for the main content
        self.content_frame = tk.Frame(self.parent, bg='#f7f7eb')
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Add the filter label and combobox to the content frame
        filter_frame = tk.Frame(self.content_frame, bg='#f7f7eb')
        filter_frame.pack(pady=10)
        filter_label = tk.Label(filter_frame, text="Filter by Specialist:", font=("Arial", 12), bg='#f7f7eb')
        filter_label.pack(side=tk.LEFT, padx=10)
        filter_combobox = ttk.Combobox(filter_frame, textvariable=self.selected_specialty, values=self.specialties, state='readonly')
        filter_combobox.pack(side=tk.LEFT)
        filter_combobox.bind("<<ComboboxSelected>>", self.apply_filter)

        # Scrollable frame for Pending Requests
        self.pending_frame = tk.Frame(self.content_frame, bg="#9AB892")
        self.pending_frame.pack(side="left", fill="both", expand=True, padx=10, pady=(10, 0))

        self.pending_canvas = tk.Canvas(self.pending_frame, bg="#9AB892")
        self.pending_scrollbar = ttk.Scrollbar(self.pending_frame, orient="vertical", command=self.pending_canvas.yview)
        self.pending_scrollable_frame = tk.Frame(self.pending_canvas, bg="#9AB892")

        self.pending_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.pending_canvas.configure(
                scrollregion=self.pending_canvas.bbox("all")
            )
        )

        self.pending_canvas.create_window((0, 0), window=self.pending_scrollable_frame, anchor="nw")
        self.pending_canvas.configure(yscrollcommand=self.pending_scrollbar.set)

        self.pending_canvas.pack(side="left", fill="both", expand=True)
        self.pending_scrollbar.pack(side="right", fill="y")

        self.pending_tree_label = tk.Label(self.pending_scrollable_frame, text="Pending Requests               ", font=("Arial", 16), bg="#9AB892")
        self.pending_tree_label.pack(pady=(10, 0))

        # Scrollable frame for Existing Doctors
        self.existing_frame = tk.Frame(self.content_frame, bg="#D69E8C")
        self.existing_frame.pack(side="left", fill="both", expand=True, padx=10, pady=(10, 0))

        self.existing_canvas = tk.Canvas(self.existing_frame, bg="#D69E8C")
        self.existing_scrollbar = ttk.Scrollbar(self.existing_frame, orient="vertical", command=self.existing_canvas.yview)
        self.existing_scrollable_frame = tk.Frame(self.existing_canvas, bg="#D69E8C")

        self.existing_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.existing_canvas.configure(
                scrollregion=self.existing_canvas.bbox("all")
            )
        )

        self.existing_canvas.create_window((0, 0), window=self.existing_scrollable_frame, anchor="nw")
        self.existing_canvas.configure(yscrollcommand=self.existing_scrollbar.set)

        self.existing_canvas.pack(side="left", fill="both", expand=True)
        self.existing_scrollbar.pack(side="right", fill="y")

        # Add the labels above the existing doctors list
        self.add_to_current_label = tk.Label(self.existing_scrollable_frame, text="Remove from Current Doctor List", font=("Arial", 16), bg="#D69E8C")
        self.add_to_current_label.pack(pady=(10, 0))

        self.existing_tree_label = tk.Label()
        self.existing_tree_label.pack(pady=(10, 0))

        # Configure grid weights to ensure proper resizing
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def load_doctors(self):
        # Clear current data but keep the labels
        for widget in self.pending_scrollable_frame.winfo_children():
            if widget not in [self.pending_tree_label]:
                widget.destroy()
        for widget in self.existing_scrollable_frame.winfo_children():
            if widget not in [self.add_to_current_label, self.existing_tree_label]:
                widget.destroy()
        
        # Fetch doctor data from Firebase
        self.doctors = db.reference('doctors').get()
        self.clinic = db.reference('clinicAdmins/' + admin_id).get()
        clinic_name = self.clinic.get("clinic_name")
        clinic_state = self.clinic.get("state")

        for doctor_id, doctor_data in self.doctors.items():
            if doctor_data.get("clinic_name") == clinic_name and doctor_data.get("state") == clinic_state:
                self.add_doctor_box(doctor_id, doctor_data)

    def add_doctor_box(self, doctor_id, doctor_data):
        # Filter based on the selected specialty
        if self.selected_specialty.get() != "All" and doctor_data.get("specialist") != self.selected_specialty.get():
            return

        # Determine the frame (pending or existing) to place the doctor box
        parent_frame = self.pending_scrollable_frame if doctor_data.get("status") == "Pending" else self.existing_scrollable_frame
        
        doctor_box = tk.Frame(parent_frame, bd=1, relief=tk.SOLID, padx=10, pady=10, bg="white")
        doctor_box.pack(fill=tk.X, pady=5)

        info = (
            f"Doctor Name: {doctor_data.get('username')}\n"
            f"Specialist: {doctor_data.get('specialist')}"
        )
        tk.Label(doctor_box, text=info, justify=tk.LEFT, bg="white").pack(anchor="w")

        # Add View button for both pending and existing doctors
        view_button = tk.Button(doctor_box, text="View", command=lambda id=doctor_id: self.view_details(id))
        view_button.pack(side=tk.RIGHT, padx=10)

        # Add Add button for pending doctors only
        if doctor_data.get("status") == "Pending":
            add_button = tk.Button(doctor_box, text="Add", command=lambda id=doctor_id: self.accept_request(id))
            add_button.pack(side=tk.RIGHT, padx=10)

        # Add Remove button for existing doctors only
        if doctor_data.get("status") == "Approved":
            remove_button = tk.Button(doctor_box, text="Remove", command=lambda id=doctor_id: self.remove_doctor(id))
            remove_button.pack(side=tk.RIGHT, padx=10)

    def view_details(self, doctor_id):
        doctor_data = db.reference('doctors/'+ doctor_id).get()

        self.clear_content()

        # Create a frame for the detailed view
        detail_frame = tk.Frame(self.parent, bg='#f7f7eb')
        detail_frame.pack(fill=tk.BOTH, expand=True)

        # Ensure the header buttons and logo remain visible
        header_frame = tk.Frame(detail_frame, bg='#f7f7eb')
        header_frame.pack(fill=tk.X)

        # Load the logo image (assuming self.logo_path is already defined)
        logo_image = tk.PhotoImage(self.logo_path)
        logo_image = logo_image.subsample(20, 20)  # Resize if needed

        # Add the logo to the header
        logo_label = tk.Label(header_frame, image=logo_image, bg='#f7f7eb')
        logo_label.image = logo_image  # Keep a reference to avoid garbage collection
        logo_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Add buttons to the header
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=10, background='#9AB892')
        style.map('TButton',
                foreground=[('active', 'white')],
                background=[('active', '#5cb85c')],
                relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        style.configure('unactive.TButton', background='#9AB892')
        style.map('unactive.TButton',
                foreground=[('active', 'white')],
                background=[('active', '#82a383')],  # Slightly darker green for active state
                relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        btn_logout = ttk.Button(header_frame, text="Logout", style='unactive.TButton')
        btn_logout.pack(side=tk.RIGHT, padx=10, pady=10)

        btn_doctor_list = ttk.Button(header_frame, text="Doctor List", style='TButton')
        btn_doctor_list.pack(side=tk.RIGHT, padx=10, pady=10)

        btn_patient_request = ttk.Button(header_frame, text="Patient Request", style='unactive.TButton')
        btn_patient_request.pack(side=tk.RIGHT, padx=10, pady=10)

        # Add Back button to the top right corner of header
        back_button_image = tk.PhotoImage(file= backIconImage)  # Replace with your image file path
        back_button_image = back_button_image.subsample(20,20)  # Resize the image as needed

        back_button = tk.Button(header_frame, image=back_button_image, command=self.back_to_list, bd=0)
        back_button.image = back_button_image
        back_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Create a scrollable frame for detailed content
        content_frame = tk.Frame(detail_frame, bg='#f7f7eb')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(content_frame, bg='#f7f7eb')
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f7f7eb')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add title for doctor information
        title_label = tk.Label(scrollable_frame, text="Doctor Details", font=("Arial", 15), bg='#f7f7eb')
        title_label.pack(anchor="n", pady=10)

        # Display "Doctor Detail" section
        info1 = (
            f"Doctor Detail:\n"
            f"Doctor Name: {doctor_data.get('username')}\n"
            f"Specialist: {doctor_data.get('specialist')}\n"
        )
        info_label1 = tk.Label(scrollable_frame, text=info1, anchor="w", justify=tk.LEFT, bg="white", width=132, height=5,
                            font=("Arial", 11))  # Adjust font size here
        info_label1.pack(anchor="w", padx=20, pady=(10, 5))

        # Display "Contact Detail" section
        info2 = (
            f"Contact Detail:\n"
            f"Email: {doctor_data.get('email')}\n"
            f"Phone: {doctor_data.get('phone')}\n"
        )
        info_label2 = tk.Label(scrollable_frame, text=info2, anchor="w", justify=tk.LEFT, bg="white", width=132, height=5,
                            font=("Arial", 11))  # Adjust font size here
        info_label2.pack(anchor="w", padx=20, pady=(0, 10))

        # Fetch appointment data based on doctor's username
        appointments_ref = db.reference('appointment').order_by_child('username').get()

        # Display fetched appointment information
        if appointments_ref:
            title_label = tk.Label(scrollable_frame, text="Appointment Schedule", font=("Arial", 16), bg='#f7f7eb')
            title_label.pack(anchor="n", pady=10)

            for appointment_id, appointment_data in appointments_ref.items():
                appointment_info = (
                    f"Appointment ID: {appointment_id}\n"
                    f"Patient Name: {appointment_data.get('username')}\n"
                    f"Date: {appointment_data.get('appointment_date')}\n"
                    f"Time: {appointment_data.get('appointment_time')}\n"
                    f"Status: {appointment_data.get('status')}\n"
                )
                appointment_label = tk.Label(scrollable_frame, text=appointment_info, anchor="w", justify=tk.LEFT, bg="white", width=132, height=6,
                                            font=("Arial", 11))  # Adjust font size here
                appointment_label.pack(anchor="w", padx=20, pady=(0, 5))

        # Add Remove button for existing doctors
        if doctor_data.get("status") == "Approved":
            remove_button = tk.Button(scrollable_frame, text="Remove", command=lambda id=doctor_id: self.remove_doctor(id))
            remove_button.pack(side=tk.TOP, padx=10, pady=10)

        # Configure grid weights to ensure proper resizing
        detail_frame.grid_columnconfigure(0, weight=1)
        detail_frame.grid_rowconfigure(1, weight=1)

       
    def reject_request(self, doctor_id):
        db.reference('doctors').child(doctor_id).update({"status": "Rejected"})
        messagebox.showinfo("Info", "Doctor request rejected.")
        self.back_to_list()

    def clear_content(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def back_to_list(self):
        self.clear_content()
        self.create_widgets()
        self.load_doctors()

    def accept_request(self, doctor_id):
        db.reference('doctors').child(doctor_id).update({"status": "Approved"})
        messagebox.showinfo("Info", "Doctor request approved.")
        self.back_to_list()

    def remove_doctor(self, doctor_id):
        db.reference('doctors').child(doctor_id).delete()
        messagebox.showinfo("Info", "Doctor removed.")
        self.back_to_list()

    def apply_filter(self, event):
        self.load_doctors()

if __name__ == "__main__":
    admin_id = sys.argv[1]

    root = tk.Tk()
    root.title("Admin Page")
    root.geometry("990x550")
    logo_path = logoImageFile
    
    # Create the DoctorListPage instance
    DoctorListPage(root, logo_path, admin_id)
    
    root.mainloop()
    