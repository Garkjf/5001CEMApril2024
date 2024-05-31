import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from firebase_admin import credentials, initialize_app ,db
import os
import subprocess
from SharePath import start_registration, start_patient, start_doctor, start_admin

# Create relative file paths
dir = os.path.dirname(__file__)

serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')   # Change the path to your own serviceAccountKey.json
logoImageFile = os.path.join(dir, '../Images/CallADoctor-logo.png')  # Change the path to your own logo image

# Initialize Firebase
cred = credentials.Certificate(serviceAccountKeyFile)
initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})

def start_registration():
    subprocess.call(["python", os.path.join(dir, 'Registration.py')])    

def start_patient():
    subprocess.call(["python", os.path.join(dir, 'PatientPage.py')])

def start_doctor():
    subprocess.call(["python", os.path.join(dir, 'DoctorPage.py')])

def start_admin():
    subprocess.call(["python", os.path.join(dir, 'ClinicAdministatorPage.py')])

class LoginPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#9AB892")

        # Header
        self.label = tk.Label(self, text="Login Portal", bg="#9AB892", font=("Arial", 24))
        self.label.grid(row=0, column=0, columnspan=7, pady=20, sticky="n") 

        # Left side
        self.label = tk.Label(self, text="Select Your Role\nWelcome to use our Call A Doctor Application.", bg="#9AB892")
        self.label.grid(row=1, column=0, padx=20, sticky="w")
        # Register label
        self.label = tk.Label(self, text="New Here? ", bg="#9AB892")
        self.label.grid(row=2, column=0, padx=20, pady=10, sticky="w") 
        # Register button
        self.register_button = tk.Button(self, text="Register Now!", command=self.register)
        self.register_button.grid(row=3, column=0, padx=100, pady=10, sticky="w") 
        # Logo
        self.logo = tk.PhotoImage(file=logoImageFile)
        self.logo = self.logo.subsample(2)  # Adjust the size of the logo image
        self.logo_label = tk.Label(self, image=self.logo)
        self.logo_label.grid(row=4, column=0, rowspan=11 ,padx=20 , sticky="w")

        # Left side End

        # Right Side
        # Role selection
        self.role_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Role", bg="#9AB892")
        self.label.grid(row=1, column=4, padx=20, sticky="w") 
        role_options = ["Choose Role", "Patient", "Doctor", "Clinic Admin"]
        self.role_dropdown = ttk.Combobox(self, textvariable=self.role_var, values=role_options, state="readonly")
        self.role_dropdown.current(0)  # Set the default value to "Choose Role"
        self.role_dropdown.grid(row=2, column=4, padx=20, pady=10, sticky="w") 
        self.role_dropdown.bind("<<ComboboxSelected>>", self.check_role_selection)        

        # Get a reference to the clinics node in the database
        clinics_ref = db.reference('clinicAdmins')

        # Retrieve the clinic data
        clinics = clinics_ref.get()
        # Clinic selection
        clinic_options = ["Choose Clinic"]
        clinic_names = set()
        
        for clinic_id, clinic_data in clinics.items():
            clinic_name = clinic_data.get('clinic_name')
            if clinic_name not in clinic_names:
                clinic_options.append(clinic_name)
                clinic_names.add(clinic_name)

        self.clinic_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Clinic", bg="#9AB892")
        self.label.grid(row=3, column=4, padx=20, sticky="w")
        self.clinic_dropdown = ttk.Combobox(self, textvariable=self.clinic_var, values=clinic_options, state="readonly")
        self.clinic_dropdown.current(0)  # Set the default value to "Choose Clinic"
        self.clinic_dropdown.grid(row=4, column=4, padx=20, pady=10, sticky="w")
        self.clinic_dropdown.bind("<<ComboboxSelected>>", self.check_clinic_selection)

        # Clinic state Selection
        self.clinic_state_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Clinic State", bg="#9AB892")
        self.label.grid(row=5, column=4, padx=20, sticky="w")  # Changed column to 1
        clinic_state_options = ["Choose Clinic State", "Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", "Pahang", "Perak", "Perlis", "Pulau Pinang", "Sabah", "Sarawak", "Selangor", "Terengganu", "Kuala Lumpur", "Labuan", "Putrajaya"]
        self.clinic_state_dropdown = ttk.Combobox(self, textvariable=self.clinic_state_var, values=clinic_state_options, state="readonly")
        self.clinic_state_dropdown.current(0)  # Set the default value to "Choose Clinic State"
        self.clinic_state_dropdown.grid(row=6, column=4, padx=20, pady=10, sticky="w") 
        self.clinic_state_dropdown.bind("<<ComboboxSelected>>", self.check_clinic_state_selection)

        # Username 
        self.label = tk.Label(self, text="IC / Passport ID", bg="#9AB892")
        self.label.grid(row=7, column=4, padx=20, sticky="w")  
        self.ic_passport_id_entry = tk.Entry(self)
        self.ic_passport_id_entry.grid(row=8, column=4, padx=20, pady=10, sticky="w")  

        # Password
        self.label = tk.Label(self, text="Password", bg="#9AB892")
        self.label.grid(row=9, column=4, padx=20, sticky="w")  
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=10, column=4, padx=20, pady=10, sticky="w") 

        # Submit button
        self.submit_button = tk.Button(self, text="Submit", bg="#0275DD", fg="#ffffff", command=self.submit)
        self.submit_button.grid(row=11, column=4, padx=20, pady=10, sticky="w") 
        # Right Side End

    def check_role_selection(self, event):
        selected_role = self.role_var.get()
        if selected_role == "Choose Role":
            messagebox.showerror("Error", "Please select a role")
        if selected_role in ["Doctor", "Clinic Admin"]:
            self.clinic_dropdown.config(state='readonly')
            self.clinic_state_dropdown.config(state='readonly')
        else:
            self.clinic_dropdown.config(state='disabled') 
            self.clinic_dropdown.current(0)
            self.clinic_state_dropdown.config(state='disabled')  
            self.clinic_state_dropdown.current(0)

    def check_clinic_selection(self, event):
        selected_clinic = self.clinic_var.get()
        if selected_clinic == "Choose Clinic":
            messagebox.showerror("Error", "Please select a clinic")

    def check_clinic_state_selection(self, event):
        selected_clinic_state = self.clinic_state_var.get()
        if selected_clinic_state == "Choose Clinic State":
            messagebox.showerror("Error", "Please select a clinic state")    

    def submit(self):
        ic_passport_id = self.ic_passport_id_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()
        clinic = self.clinic_var.get()
        clinic_state = self.clinic_state_var.get()

        if ic_passport_id == "":
            messagebox.showerror("Error", "IC / Passport ID is required")
            return

        if role == "Choose Role":
            messagebox.showerror("Error", "Role is required")
            return
        
        if password == "":  
            messagebox.showerror("Error", "Password is required")
            return
        
        try:
            # Retrieve user data from Firebase
            ref = db.reference(role.lower() + 's')
            user_data = ref.get()

            # Check if the entered username exists and the password matches
            for key, value in user_data.items():
                if role == "Patient":
                    if value['ic_passport_id'] == ic_passport_id and value['password'] == password:
                        messagebox.showinfo("Success", "Login Successful")
                        return self.patientScreen()

                elif role == "Doctor":
                    if value['ic_passport_id'] == ic_passport_id and value['password'] == password and clinic == value['clinic_name'] and clinic_state == value['clinic_state']:
                        messagebox.showinfo("Success", "Login Successful")
                        return self.doctorScreen()
                    
                elif role == "Clinic Admin":
                    if value['ic_passport_id'] == ic_passport_id and value['password'] == password and clinic == value['clinic_name'] and clinic_state == value['clinic_state']:
                        messagebox.showinfo("Success", "Login Successful")
                        return self.clinicAdminScreen()
                else:
                    raise Exception("Invalid role")
               
            # username doesn't exist or the password doesn't match
            raise Exception("Invalid username or password")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        start_registration()

    def patientScreen(self):
        start_patient()   

    def doctorScreen(self):
        start_doctor()
    
    def adminScreen(self):
        start_admin()

# Main Execution
if __name__ == "__main__":
    root = tk.Tk()  # Create a new Tk root window
    root.title("Call a Doctor")  # Set the title of the window
    root.geometry("750x550")
    app = LoginPage(root)  # Pass the root window to your LoginPage class
    app.pack(fill="both", expand=True)  # Make the LoginPage fill the entire window
    root.mainloop()  # Start the Tkinter event loop