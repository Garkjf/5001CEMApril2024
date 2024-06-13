import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials,initialize_app, db, get_app
import os
import subprocess
import re
import uuid

# Create relative file paths
dir = os.path.dirname(__file__)

serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')   # Change the path to your own serviceAccountKey.json
logoImageFile = os.path.join(dir, '../Images/CallADoctor-logo.png')  # Change the path to your own logo image

# Initialize Firebase
cred = credentials.Certificate(serviceAccountKeyFile)
try:
    get_app()
except ValueError as e:
    initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})

def start_login():
    subprocess.call(["python", os.path.join(dir, 'Login.py')])

class RegistrationPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#9AB892")

        # Header
        self.label = tk.Label(self, text="Patient Registration Portal", bg="#9AB892", font=("Arial", 24))
        self.label.grid(row=0, column=0, columnspan=7, pady=20, sticky="n") 

        # Left side
        self.label = tk.Label(self, text="Welcome to use our Call A Doctor Application.", bg="#9AB892")
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
        # start column 1
        # Username 
        self.label = tk.Label(self, text="Username", bg="#9AB892")
        self.label.grid(row=2, column=1, padx=20, sticky="w")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        
        #  Email
        self.label = tk.Label(self, text="Email", bg="#9AB892")
        self.label.grid(row=4, column=1, padx=20, sticky="w") 
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=5, column=1, padx=20, pady=10, sticky="w") 
       
       #  Phone number
        self.label = tk.Label(self, text="Phone Number", bg="#9AB892")
        self.label.grid(row=6, column=1, padx=20, sticky="w") 
        self.phone_no_entry = tk.Entry(self)
        self.phone_no_entry.grid(row=7, column=1, padx=20, pady=10, sticky="w") 

        # Password
        self.label = tk.Label(self, text="Password", bg="#9AB892")
        self.label.grid(row=8, column=1, padx=20, sticky="w") 
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=9, column=1, padx=20, pady=10, sticky="w") 

        # confirm password
        self.label = tk.Label(self, text="Confirm Password", bg="#9AB892")
        self.label.grid(row=10, column=1, padx=20, sticky="w")
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.grid(row=11, column=1, padx=20, pady=10, sticky="w") 
        # end column 1

        # start cloumn 2
        # Radio buttons for IC and Passport selection
        self.id_type_var = tk.StringVar()
        self.label = tk.Label(self, text="ID Type", bg="#9AB892")
        self.label.grid(row=2, column=2, padx=20, sticky="w")
        self.ic_radio = tk.Radiobutton(self, text="IC", variable=self.id_type_var, value="IC")
        self.ic_radio.grid(row=3, column=2, padx=20, pady=5, sticky="w")
        self.passport_radio = tk.Radiobutton(self, text="Passport", variable=self.id_type_var, value="Passport")
        self.passport_radio.grid(row=4, column=2, padx=20, pady=5, sticky="w")
        
        # IC / Passport ID
        self.label = tk.Label(self, text="IC / Passport ID", bg="#9AB892")
        self.label.grid(row=5, column=2, padx=20, sticky="w")
        self.ic_passport_id_entry = tk.Entry(self)
        self.ic_passport_id_entry.grid(row=6, column=2, padx=20, pady=10, sticky="w")
        
        # Select IC by default
        self.ic_radio.select()

        # Submit button
        self.submit_button = tk.Button(self, text="Submit", bg="#0275DD", fg="#ffffff", command=self.submit)
        self.submit_button.grid(row=12, column=2, padx=30, pady=10, sticky="w") 
        # end column 2
        # Right Side End


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
        role = 'Patient'
        ic_passport_id = self.ic_passport_id_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        phone = self.phone_no_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        patient_id = str(uuid.uuid4())
        # Capitalize the first letter of each word in the username
        username = username.title()

        if not self.validate_email(email):
            return
        
        if not self.validate_phone(phone):
            return
        
        if self.id_type_var.get() == "IC":
             if not self.validate_ic(ic_passport_id):
                return
        
        elif self.id_type_var.get() == "Passport":
            if not self.validate_passport(ic_passport_id):
                return
                    
        if role == "Choose Role":
            messagebox.showerror("Error", "Role is required")
            return

        if ic_passport_id == "":
            messagebox.showerror("Error", "IC/Passport ID is required")
            return
        
        if username == "":
            messagebox.showerror("Error", "Username is required")
            return
        
        elif not all(char.isalpha() or char.isspace() for char in username):
            messagebox.showerror("Error", "Username should only contain letters only!")
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

        try:
            # Check if IC/Passport ID already exists
            ref = db.reference(role.lower() + 's')
            if ref.child(ic_passport_id).get() is not None:
                messagebox.showerror("Error", "IC/Passport ID already exists")
                return
            
            if ref.child(phone).get() is not None:
                messagebox.showerror("Error", "Phone Number already exists")
                return 
            
            if role == 'Patient':
                self.save_patient(patient_id, role, ic_passport_id, username, email, phone, password)
                messagebox.showinfo("Success", "Patient registration successful")
                self.login()
            else:
                messagebox.showerror("Error", "Invalid role")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", e)

    def save_patient(self,patient_id, role, ic_passport_id, username, email, phone, password):
        ref = db.reference('patients')
        ref.child(ic_passport_id).set({
            'patientID': patient_id,
            'role': role,
            'ic_passport_id': ic_passport_id,
            'username': username,
            'email': email,
            'phone': phone,
            'password': password
        })  
    
    def login(self):
        # close the current window
        self.master.destroy()
        start_login()

# Main Execution
if __name__ == "__main__":
    root = tk.Tk()  # Create a new Tk root window
    root.title("Call a Doctor")  # Set the title of the window
    root.geometry("750x550")
    app = RegistrationPage(root)  # Pass the root window to your LoginPage class
    app.pack(fill="both", expand=True)  # Make the LoginPage fill the entire window
    root.mainloop()  # Start the Tkinter event loop
