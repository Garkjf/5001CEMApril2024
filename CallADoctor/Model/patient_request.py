import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials, initialize_app, db
import os
import subprocess

# Set up paths
dir = os.path.dirname(__file__)
serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')

# Initialize Firebase
cred = credentials.Certificate(serviceAccountKeyFile)
initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})

def fetch_appointments():
    # Fetch appointments from Firebase database
    ref = db.reference('appointment')
    appointments = ref.get()
    
    # Filter out appointments that are already Accepted or Rejected
    filtered_appointments = {key: value for key, value in appointments.items() if value.get('status') not in ['Accepted', 'Rejected']}
    
    return filtered_appointments

def update_appointment_status(appt_id, status):
    # Update the appointment status in Firebase database
    ref = db.reference(f'appointment/{appt_id}')
    ref.update({'status': status})
    messagebox.showinfo("Info", f"Appointment {status} successfully!")
    
    # Refresh UI after updating status
    refresh_ui()

def open_doctor_schedule(doctor_id):
    # Replace this with your logic to open the doctor's schedule
    print(f"Viewing schedule for doctor with ID: {doctor_id}")

def create_ui(root, logo_path):
    # Set the window title
    root.title("Admin Page")

    # Load the logo image
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((100, 60))  # Resize if needed
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Create a frame for the header
    header_frame = tk.Frame(root, bg='#f7f7eb')
    header_frame.pack(fill=tk.X)

    # Add the logo to the header
    logo_label = tk.Label(header_frame, image=logo_photo, bg='#f7f7eb')
    logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
    logo_label.pack(side=tk.LEFT, padx=10, pady=10)

    # Create a style for the buttons
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), padding=10, background='White')
    style.map('TButton',
              foreground=[('active', 'white')],
              background=[('active', '#5cb85c')],
              relief=[('pressed', 'sunken'), ('!pressed', 'raised')])   

    # Create a specific style for the "Patient Request" button
    style.configure('PatientRequest.TButton', background='#9AB892')
    style.map('PatientRequest.TButton',
              foreground=[('active', 'white')],
              background=[('active', '#82a383')],  # Slightly darker green for active state
              relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

    # Open the doctor_list.py script using subprocess
    def open_doctor_list():
        subprocess.Popen(['python', 'C:/Users/mwk02/OneDrive/Desktop/5001CEMApril2024-main/CallADoctor/Model/doctor_list.py'])

    def open_patient_request():
        subprocess.Popen(['python', 'C:/Users/mwk02/OneDrive/Desktop/5001CEMApril2024-main/CallADoctor/Model/patient_request.py'])

    # Add buttons to the header with switched positions
    btn_doctor_list = ttk.Button(header_frame, text="Doctor List", style='TButton', command=open_doctor_list)
    btn_doctor_list.pack(side=tk.RIGHT, padx=10, pady=10)
    btn_patient_request = ttk.Button(header_frame, text="Patient Request", style='PatientRequest.TButton', command=open_patient_request)
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

    # Add the title label to the content frame
    title_label = tk.Label(appointments_frame, text="Pantai Hospital Penang Patient’s Request",
                           font=("Arial", 18, "bold"), bg='#f7f7eb')
    title_label.pack(padx=20, pady=20, anchor=tk.W)

    # Fetch appointments from Firebase
    appointments = fetch_appointments()

    if appointments:
        # Display appointment details
        for appt_id, appt in appointments.items():
            frame = ttk.Frame(appointments_frame, padding="10", style="Card.TFrame")
            frame.pack(fill="x", pady=5, padx=10)

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

            view_button = ttk.Button(buttons_frame, text="View", command=lambda a=appt: view_appointment_details(root, a, logo_path, appt_id))
            view_button.pack(side=tk.LEFT, padx=5)

            accept_button = ttk.Button(buttons_frame, text="Approve", command=lambda appt_id=appt_id: update_appointment_status(appt_id, "Accepted"))
            accept_button.pack(side=tk.LEFT, padx=5)

            reject_button = ttk.Button(buttons_frame, text="Reject", command=lambda appt_id=appt_id: update_appointment_status(appt_id, "Rejected"))
            reject_button.pack(side=tk.LEFT, padx=5)

    # Update the canvas scroll region when widgets are added
    appointments_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def view_appointment_details(root, appt, logo_path, appt_id):
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
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((100, 60))  # Resize if needed
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Add the logo to the header
    logo_label = tk.Label(header_frame, image=logo_photo, bg='#f7f7eb')
    logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
    logo_label.pack(side=tk.LEFT, padx=10, pady=10)

    # Add Back button to the top right corner of header
    back_button_image = Image.open("C:/Users/mwk02/OneDrive/Desktop/5001CEMApril2024-main/CallADoctor/Images/back-icon.png")  # Replace with your image file path
    back_button_image = back_button_image.resize((30, 15))  # Resize the image as needed
    back_photo = ImageTk.PhotoImage(back_button_image)

    def back_to_main_ui():
        detail_frame.destroy()
        create_ui(root, logo_path)

    back_button = tk.Button(header_frame, image=back_photo, command=back_to_main_ui, bd=0)
    back_button.image = back_photo
    back_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Add title for appointment information
    title_label = tk.Label(detail_frame, text="Appointment Details", font=("Arial", 20), bg='#f7f7eb')
    title_label.pack(anchor="n", pady=10)

    # Display "Appointment Detail" section
    info1 = (
        f"Patient Information:\n"
        f"Patient Name: {appt.get('username')}\n"
        f"Email: {appt.get('email')}\n"
        f"Phone: {appt.get('phone')}"
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
        open_doctor_schedule(doctor_id)

    view_schedule_button = ttk.Button(detail_frame, text="View Doctor Schedule", command=view_doctor_schedule)
    view_schedule_button.pack(anchor="e", pady=20)

    # Add Accept and Reject buttons to the detailed view
    buttons_frame = ttk.Frame(detail_frame)
    buttons_frame.pack(pady=20)

    accept_button = ttk.Button(buttons_frame, text="Approve", command=lambda: update_appointment_status(appt_id, "Accepted"))
    accept_button.pack(side=tk.LEFT, padx=10, anchor="nw")

    reject_button = ttk.Button(buttons_frame, text="Reject", command=lambda: update_appointment_status(appt_id, "Rejected"))
    reject_button.pack(side=tk.LEFT, padx=10, anchor="nw")

    # Configure grid weights to ensure proper resizing
    detail_frame.grid_columnconfigure(0, weight=1)
    detail_frame.grid_rowconfigure(1, weight=1)

def refresh_ui():
    # Clear current UI and recreate with updated data
    for widget in root.winfo_children():
        widget.destroy()
    create_ui(root, logo_path)

if __name__ == "__main__":
    root = tk.Tk()
    logo_path = "C:/Users/mwk02/OneDrive/Desktop/5001CEMApril2024-main/CallADoctor/Images/CallADoctor-logo-small.png"
    # Set the same geometry as the login page
    root.geometry("750x600")
    create_ui(root, logo_path)

    root.mainloop()

