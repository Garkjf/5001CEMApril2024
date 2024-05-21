import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, auth
import os
import subprocess
from SharePath import start_login

# Create relative file paths
dir = os.path.dirname(__file__)

# os.path.join(dir, '../Images/CallADoctor-logo.png')

serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')   # Change the path to your own serviceAccountKey.json
logoImageFile = os.path.join(dir, '../Images/CallADoctor-logo.png')  # Change the path to your own logo image

# Initialize Firebase
cred = credentials.Certificate(serviceAccountKeyFile)
firebase = firebase_admin.initialize_app(cred)

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
        self.logo_label.grid(row=4, column=0, rowspan=11 ,padx=20 , sticky="w")

        # Left side End

        # Right Side
        # Role selection
        self.role_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Role", bg="#9AB892")
        self.label.grid(row=1, column=2, padx=20, sticky="w") 
        role_options = ["Choose Role", "Patient", "Doctor", "Clinic Admin"]
        self.role_dropdown = ttk.Combobox(self, textvariable=self.role_var, values=role_options, state="readonly")
        self.role_dropdown.current(0)  # Set the default value to "Choose Role"
        self.role_dropdown.grid(row=2, column=2, padx=20, pady=10, sticky="w") 
        self.role_dropdown.bind("<<ComboboxSelected>>", self.check_role_selection)

        # Clinic selection
        self.clinic_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Clinic", bg="#9AB892")
        self.label.grid(row=3, column=2, padx=20, sticky="w") 
        clinic_options = ["Choose Clinic", "Bagan Ajam", "Bagan Specialist", "Sunway Hospital"]
        self.clinic_dropdown = ttk.Combobox(self, textvariable=self.clinic_var, values=clinic_options, state="readonly")
        self.clinic_dropdown.current(0)  # Set the default value to "Choose Clinic"
        self.clinic_dropdown.grid(row=4, column=2, padx=20, pady=10, sticky="w")  
        self.clinic_dropdown.bind("<<ComboboxSelected>>", self.check_clinic_selection)

        # Clinic state Selection
        self.clinic_state_var = tk.StringVar()
        self.label = tk.Label(self, text="Select Clinic State", bg="#9AB892")
        self.label.grid(row=5, column=2, padx=20, sticky="w")  # Changed column to 1
        clinic_state_options = ["Choose Clinic State", "Penang", "Kuala Lumpur", "Johor"]
        self.clinic_state_dropdown = ttk.Combobox(self, textvariable=self.clinic_state_var, values=clinic_state_options, state="readonly")
        self.clinic_state_dropdown.current(0)  # Set the default value to "Choose Clinic State"
        self.clinic_state_dropdown.grid(row=6, column=2, padx=20, pady=10, sticky="w") 
        self.clinic_state_dropdown.bind("<<ComboboxSelected>>", self.check_clinic_state_selection)

        # Username 
        self.label = tk.Label(self, text="Username", bg="#9AB892")
        self.label.grid(row=1, column=3, padx=20, sticky="w")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=2, column=3, padx=20, pady=10, sticky="w")
        
        #  Email
        self.label = tk.Label(self, text="Email", bg="#9AB892")
        self.label.grid(row=3, column=3, padx=20, sticky="w") 
        self.emai_entry = tk.Entry(self)
        self.emai_entry.grid(row=4, column=3, padx=20, pady=10, sticky="w") 

        # Password
        self.label = tk.Label(self, text="Password", bg="#9AB892")
        self.label.grid(row=5, column=3, padx=20, sticky="w") 
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=6, column=3, padx=20, pady=10, sticky="w") 

        # confirm password
        self.label = tk.Label(self, text="Confirm Password", bg="#9AB892")
        self.label.grid(row=7, column=3, padx=20, sticky="w")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=8, column=3, padx=20, pady=10, sticky="w") 

        # Submit button
        self.submit_button = tk.Button(self, text="Submit", bg="#0275DD", fg="#ffffff", command=self.submit)
        self.submit_button.grid(row=10, column=3, padx=20, pady=10, sticky="w") 
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
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()
        clinic = self.clinic_var.get()
        click_state = self.clinic_state_var.get()

        try:
            user = auth.sign_in_with_email_and_password(username, password, role, clinic, click_state)
            # You can add code here to handle role, clinic, and click state
        except:
            messagebox.showerror("Error", "Invalid username or password")

    def login(self):
        start_login()

# Main Execution
if __name__ == "__main__":
    root = tk.Tk()  # Create a new Tk root window
    root.title("Call a Doctor")  # Set the title of the window
    root.geometry("750x550")
    app = RegistrationPage(root)  # Pass the root window to your LoginPage class
    app.pack(fill="both", expand=True)  # Make the LoginPage fill the entire window
    root.mainloop()  # Start the Tkinter event loop