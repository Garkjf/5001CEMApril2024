import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials,initialize_app, db
import os
import subprocess
import re
from SharePath import start_login

# Create relative file paths
dir = os.path.dirname(__file__)

serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')   # Change the path to your own serviceAccountKey.json
logoImageFile = os.path.join(dir, '../Images/CallADoctor-logo.png')  # Change the path to your own logo image

# Initialize Firebase
cred = credentials.Certificate(serviceAccountKeyFile)
initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})

def start_login():
    subprocess.call(["python", os.path.join(dir, 'login.py')])

class RegistrationPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#9AB892")

        # Header
        self.label = tk.Label(self, text="Registration Portal", bg="#9AB892", font=("Arial", 24))
        self.label.grid(row=0, column=0, columnspan=7, pady=20, sticky="n") 

        # Left side
        self.label = tk.Label(self, text="Select Your Role\nWelcome to use our Call A Doctor Application.", bg="#9AB892")
        self.label.grid(row=1, column=0, padx=20, sticky="w")
        # login label
        self.label = tk.Label(self, text="Already Have an Account? ", bg="#9AB892")
        self.label.grid(row=2, column=0, padx=20, pady=10, sticky="w") 
        # login button
        self.login_button = tk.Button(self, text="Login Now!", command=self.login)
        self.login_button.grid(row=3, column=0, padx=100, sticky="w") 
        # Logo
        self.logo = tk.PhotoImage(file=logoImageFile)
        self.logo = self.logo.subsample(2)
        self.logo_label = tk.Label(self, image=self.logo)
        self.logo_label.grid(row=5, column=0, rowspan=11 ,padx=20 , sticky="w")
        # Left side End

        # Right Side
        # Role selection
        self.role_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Role", bg="#9AB892")
        self.label.grid(row=1, column=1, padx=20, sticky="w") 
        role_options = ["Choose Role", "Patient", "Doctor", "Clinic Admin"]
        self.role_dropdown = ttk.Combobox(self, textvariable=self.role_var, values=role_options, state="readonly")
        self.role_dropdown.current(0)  # Set the default value to "Choose Role"
        self.role_dropdown.grid(row=2, column=1, padx=20, pady=10, sticky="w") 
        self.role_dropdown.bind("<<ComboboxSelected>>", self.check_role_selection)

        # Get a reference to the clinics node in the database
        clinics_ref = db.reference('clinicAdmins')

        # Retrieve the clinic data
        clinics = clinics_ref.get()
        # Clinic selection
        clinic_options = ["Choose Clinic"]
        clinic_names = set()

        # Clinic State Selection
        clinic_state_options = [
            "Choose Clinic State",
            "Johor",
            "Kedah",
            "Kelantan",
            "Kuala Lumpur",
            "Melaka",
            "Negeri Sembilan",
            "Pahang",
            "Perak",
            "Perlis",
            "Penang",
            "Sabah",
            "Sarawak",
            "Selangor",
            "Terengganu",
        ]
            
        for clinic_id, clinic_data in clinics.items():
            clinic_name = clinic_data.get('clinic_name')
            if clinic_name not in clinic_names:
                clinic_options.append(clinic_name)
                clinic_names.add(clinic_name)
            
                
        self.clinic_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Clinic", bg="#9AB892")
        self.label.grid(row=3, column=1, padx=20, sticky="w")
        self.clinic_dropdown = ttk.Combobox(self, textvariable=self.clinic_var, values=clinic_options, state="readonly")
        self.clinic_dropdown.current(0)  # Set the default value to "Choose Clinic"
        self.clinic_dropdown.grid(row=4, column=1, padx=20, pady=10, sticky="w")
        self.clinic_dropdown.bind("<<ComboboxSelected>>", self.check_clinic_selection)

        # Clinic state Selection
        self.clinic_state_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Clinic State", bg="#9AB892")
        self.label.grid(row=5, column=1, padx=20, sticky="w")  # Changed column to 0
        self.clinic_state_dropdown = ttk.Combobox(self, textvariable=self.clinic_state_var, values=clinic_state_options, state="readonly")
        self.clinic_state_dropdown.current(0)  # Set the default value to "Choose Clinic State"
        self.clinic_state_dropdown.grid(row=6, column=1, padx=20, pady=10, sticky="w") 
        self.clinic_state_dropdown.bind("<<ComboboxSelected>>", self.check_clinic_state_selection)

        # Doctor Specialist Selection
        self.specialist_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Specialist", bg="#9AB892")
        self.label.grid(row=7, column=1, padx=20, sticky="w")  # Changed column to 0
        specialist_options = ["Choose Specialist", "Cardiology", "Dermatology", "Endocrinology", "Gastroenterology", "Neurology", "Oncology", "Pediatrics", "Psychiatry", "Radiology", "Urology"]
        self.specialist_dropdown = ttk.Combobox(self, textvariable=self.specialist_var, values=specialist_options, state="readonly")
        self.specialist_dropdown.current(0)  # Set the default value to "Choose Specialist"
        self.specialist_dropdown.grid(row=8, column=1, padx=20, pady=10, sticky="w") 
        self.specialist_dropdown.bind("<<ComboboxSelected>>", self.check_specialist_selection)

        # Radio buttons for IC and Passport selection
        self.id_type_var = tk.StringVar()
        self.label = tk.Label(self, text="ID Type", bg="#9AB892")
        self.label.grid(row=9, column=1, padx=20, sticky="w")
        self.ic_radio = tk.Radiobutton(self, text="IC", variable=self.id_type_var, value="IC")
        self.ic_radio.grid(row=10, column=1, padx=20, pady=5, sticky="w")
        self.passport_radio = tk.Radiobutton(self, text="Passport", variable=self.id_type_var, value="Passport")
        self.passport_radio.grid(row=11, column=1, padx=20, pady=5, sticky="w")
        
        # IC / Passport ID
        self.label = tk.Label(self, text="IC / Passport ID", bg="#9AB892")
        self.label.grid(row=12, column=1, padx=20, sticky="w")
        self.ic_passport_id_entry = tk.Entry(self)
        self.ic_passport_id_entry.grid(row=13, column=1, padx=20, pady=10, sticky="w")
        
        # Select IC by default
        self.ic_radio.select()

        #  Clinic name entry
        self.label = tk.Label(self, text="Enter Clinic Name", bg="#9AB892")
        self.label.grid(row=1, column=2, padx=20, sticky="w") 
        self.clinic_name_entry = tk.Entry(self)
        self.clinic_name_entry.grid(row=2, column=2, padx=20, pady=10, sticky="w")
        self.clinic_name_entry.config(state="disabled")  # Disable the entry by default

        # Username 
        self.label = tk.Label(self, text="Username", bg="#9AB892")
        self.label.grid(row=3, column=2, padx=20, sticky="w")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=4, column=2, padx=20, pady=10, sticky="w")
        
        #  Email
        self.label = tk.Label(self, text="Email", bg="#9AB892")
        self.label.grid(row=5, column=2, padx=20, sticky="w") 
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=6, column=2, padx=20, pady=10, sticky="w") 
       
       #  Phone number
        self.label = tk.Label(self, text="Phone Number", bg="#9AB892")
        self.label.grid(row=7, column=2, padx=20, sticky="w") 
        self.phone_no_entry = tk.Entry(self)
        self.phone_no_entry.grid(row=8, column=2, padx=20, pady=10, sticky="w") 

        # Password
        self.label = tk.Label(self, text="Password", bg="#9AB892")
        self.label.grid(row=9, column=2, padx=20, sticky="w") 
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=10, column=2, padx=20, pady=10, sticky="w") 

        # confirm password
        self.label = tk.Label(self, text="Confirm Password", bg="#9AB892")
        self.label.grid(row=11, column=2, padx=20, sticky="w")
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.grid(row=12, column=2, padx=20, pady=10, sticky="w") 

        # Submit button
        self.submit_button = tk.Button(self, text="Submit", bg="#0275DD", fg="#ffffff", command=self.submit)
        self.submit_button.grid(row=14, column=2, padx=20, pady=10, sticky="w") 
        # Right Side End

    def check_role_selection(self, event):
        selected_role = self.role_var.get()
        if selected_role == "Choose Role" or selected_role == "":
            messagebox.showerror("Error", "Please select a role")
        if selected_role in ["Doctor", "Clinic Admin"]:
            self.clinic_state_dropdown.config(state='readonly')
            
            if selected_role == "Doctor":
                self.clinic_dropdown.config(state='readonly')
                self.specialist_dropdown.config(state='readonly')
                self.clinic_name_entry.config(state="disabled")
                self.clinic_name_entry.delete(0, tk.END)

            if selected_role == "Clinic Admin":
                self.clinic_dropdown.config(state='disabled') 
                self.clinic_dropdown.current(0)
                self.specialist_dropdown.config(state='disabled')
                self.specialist_dropdown.current(0)
                self.clinic_name_entry.config(state="normal")

        else:
            self.clinic_dropdown.config(state='disabled') 
            self.clinic_dropdown.current(0)
            self.clinic_state_dropdown.config(state='disabled')  
            self.clinic_state_dropdown.current(0)
            self.specialist_dropdown.config(state='disabled')
            self.specialist_dropdown.current(0)
            self.clinic_name_entry.config(state="disabled")
            self.clinic_name_entry.delete(0, tk.END)

    def check_clinic_selection(self, event):
        selected_clinic = self.clinic_var.get()
        if selected_clinic == "Choose Clinic":
            messagebox.showerror("Error", "Please select a clinic")

    def check_clinic_state_selection(self, event):
        selected_clinic_state = self.clinic_state_var.get()
        if selected_clinic_state == "Choose Clinic State":
            messagebox.showerror("Error", "Please select a clinic state")    

    def check_specialist_selection(self, event):
        selected_specialist = self.specialist_var.get()
        if selected_specialist == "Choose Specialist":
            messagebox.showerror("Error", "Please select a specialist")        

    def validate_ic(self, value):
        ic_regex = r'^\d{6}-\d{2}-\d{4}$'
        if re.match(ic_regex, value):
            return True
        else: 
            messagebox.showerror("Error", "IC ID must follow the Malaysia IC format (YYMMDD-PB-####)")
            return False

    def validate_passport(self, value):
        if len(value) >= 8 and len(value) <= 9:
            return True
        else:
            messagebox.showerror("Error", "Passport ID must be 8-9 characters")
        return  

    def validate_email(self, email):
        
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.fullmatch(email_regex, email):
            return True
        else:
            messagebox.showerror("Error", "Invalid email format")
            return False
        
    def validate_phone(self, phone):

        phone_number_regex = r'^01\d-\d{7,8}$'
        if re.fullmatch(phone_number_regex, phone):
            return True
        else:
            messagebox.showerror("Error", "PHone Number is not in Correct Format! \n Should use Malaysia Phone Number Format (01X-XXXXXXX)")
            return False

    def submit(self):
        role = self.role_var.get()
        clinic = self.clinic_var.get()
        clinic_state = self.clinic_state_var.get()
        ic_passport_id = self.ic_passport_id_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        phone = self.phone_no_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        specialist = self.specialist_var.get()
        clinic_info = {}

        # Capitalize the first letter of each word in the username
        username = username.title()

        if not self.validate_email(email):
            return
        
        if not self.validate_ic(ic_passport_id) and self.id_type_var.get() == "IC":
            return
        
        if not self.validate_passport(ic_passport_id) and self.id_type_var.get() == "Passport":
            return

        clinics_ref = db.reference('clinicAdmins')
        clinics = clinics_ref.get()

        for clinic_id, clinic_data in clinics.items():
            clinic_name = clinic_data.get('clinic_name')
            clinic_state_db = clinic_data.get('clinic_state')

            clinic_info[clinic_name] = clinic_state_db
                    
        if role == "Doctor":
            if clinic_info.get(clinic) != clinic_state:
                messagebox.showerror("Error", "Clinic not found")
                return

        if role == "Choose Role":
            messagebox.showerror("Error", "Role is required")
            return
        
        if clinic == "Choose Clinic" and role == "Doctor":
            messagebox.showerror("Error", "Select a Clinic is required")
            return
        
        if clinic_state == "Choose Clinic State" and role == "Doctor":
            messagebox.showerror("Error", "Select the Clinic State is required")
            return
        
        if ic_passport_id == "":
            messagebox.showerror("Error", "IC/Passport ID is required")
            return
        
        if username == "":
            messagebox.showerror("Error", "Username is required")
            return
        
        if email == "":
            messagebox.showerror("Error", "Email is required")
            return
        
        if phone == "":
            messagebox.showerror("Error", "Phone Number is required")
            return

        if password == "":  
            messagebox.showerror("Error", "Password is required")
            return
        
        if confirm_password == "":
            messagebox.showerror("Error", "Confirm Password is required")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if role == "Doctor" and specialist == "Choose Specialist":
            messagebox.showerror("Error", "Specialist is required")
            return

        try:
            # Check if IC/Passport ID already exists
            ref = db.reference(role.lower() + 's')
            if ref.child(ic_passport_id).get() is not None:
                messagebox.showerror("Error", "IC/Passport ID already exists")
                return
            
            if role == 'Patient':
                self.save_patient(role, ic_passport_id, username, email, phone, password)
                messagebox.showinfo("Success", "Patient registration successful")
            elif role == 'Doctor':
                self.save_doctor(role, clinic, clinic_state, ic_passport_id, username, email, phone, password, specialist)
                messagebox.showinfo("Success", "Your Doctor registration information is sending for approval")
            elif role == 'Clinic Admin':
                self.save_clinic_admin(role, clinic, clinic_state, ic_passport_id, username, email, phone, password)
                messagebox.showinfo("Success", "Your Clinic Admin registration information is sending for approval")
            else:
                messagebox.showerror("Error", "Invalid role selected")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", e)

    def save_patient(self, role, ic_passport_id, username, email, phone, password):
        ref = db.reference('patients')
        ref.child(ic_passport_id).set({
            'role': role,
            'ic_passport_id': ic_passport_id,
            'username': username,
            'email': email,
            'phone': phone,
            'password': password
        })

    def save_clinic_admin(self, role, clinic_name, clinic_state, ic_passport_id, username, email, phone, password):
        if clinic_name == "" or clinic_name == "Choose Clinic":
            clinic_name = self.clinic_name_entry.get()
            # Capitalize the first letter of each word in the username
            clinic_name = clinic_name.title()
        ref = db.reference('clinicAdmins')
        ref.child(ic_passport_id).set({
            'role': role,
            'clinic_name': clinic_name,
            'clinic_state': clinic_state,
            'ic_passport_id': ic_passport_id,
            'username': username,
            'email': email,
            'phone': phone,
            'password': password
        })

    def save_doctor(self, role, clinic_name, clinic_state, ic_passport_id, username, email, phone, password, specialist):
        if clinic_name == "":
            clinic_name = self.clinic_name_entry.get()

        ref = db.reference('doctors')
        ref.child(ic_passport_id).set({
            'role': role,
            'clinic_name': clinic_name,
            'clinic_state': clinic_state,
            'ic_passport_id': ic_passport_id,
            'username': username,
            'email': email,
            'phone': phone,
            'password': password,
            'specialist': specialist
        })        
    
    def login(self):
        start_login()

# Main Execution
if __name__ == "__main__":
    root = tk.Tk()  # Create a new Tk root window
    root.title("Call a Doctor")  # Set the title of the window
    root.geometry("750x750")
    app = RegistrationPage(root)  # Pass the root window to your LoginPage class
    app.pack(fill="both", expand=True)  # Make the LoginPage fill the entire window
    root.mainloop()  # Start the Tkinter event loop