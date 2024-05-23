import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import BOLD, Font
from PIL import Image, ImageTk
import os

dir = os.path.dirname(__file__)

class DoctorPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F6F6E9")

        # Header
        self.logo = Image.open(os.path.join(dir, '../Images/CallADoctor-logo.png'))
        self.logo = ImageTk.PhotoImage(self.logo.resize((130, 130)))
        logo_label = tk.Label(self, image=self.logo, bg="#F6F6E9")
        logo_label.grid(row=0, column=0, rowspan=2, sticky="w")

        bold14 = Font(self.master, size=14, weight=BOLD) 
        label = tk.Label(self, text="Search For Patient", bg="#F6F6E9", font=bold14)
        label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

        patient_name_entry = tk.Entry(self)
        patient_name_entry.grid(row=3, column=0, columnspan=30, padx=20, pady=(10, 0), sticky="w")

        submit_button = tk.Button(self, text="Search", bg="#0275DD", fg="#ffffff")
        submit_button.grid(row=3, column=1, pady=(10, 0), sticky="w")

        patients = [
            {"name": "Stephen Lee", "email": "stephen@gmail.com", "phoneNum": "00123542122"}, 
            {"name": "Aaron Lee", "email": "aaron@gmail.com", "phoneNum": "221543542"},
        ]
        self.listPatients(patients)

        # Ensure the patient_frame expands correctly
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

    def listPatients(self, patients):
         for row, patient in enumerate(patients, 4):
            # Create a frame with a white background to display patient details
            patient_frame = tk.Frame(self, bg='white', width=400, height=30)
            patient_frame.grid(row=row, column=0, padx=20, pady=20, sticky="n")
            self.grid_rowconfigure(row, weight=1)

            name_label = tk.Label(patient_frame, text=f"Patient Name: {patient['name']}", bg="white")
            name_label.grid(row=0, column=0, padx=20, sticky="w")

            view_button = tk.Button(patient_frame, text="View", bg="#0275DD", fg="#ffffff")
            view_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

            email_label = tk.Label(patient_frame, text=f"Email: {patient['email']}", bg="white")
            email_label.grid(row=1, column=0, padx=20, sticky="w")

            phone_num_label = tk.Label(patient_frame, text=f"Phone Number: {patient['phoneNum']}", 
                                       bg="white")
            phone_num_label.grid(row=2, column=0, padx=20, sticky="w")

    # def search_patient(self):
    #     # Function to handle the search functionality
    #     patient_name = self.patient_name_entry.get()
    #     messagebox.showinfo("Search", f"Searching for patient: {patient_name}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Call a Doctor - Doctor Page")
    root.geometry("750x550")
    app = DoctorPage(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
