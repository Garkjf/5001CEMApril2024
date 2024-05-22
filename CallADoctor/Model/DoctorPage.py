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
        self.logo_label = tk.Label(self, image=self.logo, bg="#F6F6E9")
        self.logo_label.grid(row=0, column=0, rowspan=2, sticky="w")

        self.bold14 = Font(self.master, size=14, weight=BOLD) 
        self.label = tk.Label(self, text="Search For Patient", bg="#F6F6E9", font=self.bold14)
        self.label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

        self.patient_name_entry = tk.Entry(self)
        self.patient_name_entry.grid(row=3, column=0, columnspan=30, padx=20, pady=(10, 0), sticky="w")

        self.submit_button = tk.Button(self, text="Search", bg="#0275DD", fg="#ffffff")
        self.submit_button.grid(row=3, column=1, pady=(10, 0), sticky="w")

        # Create a frame with a white background to display patient details
        self.patient_frame = tk.Frame(self, bg='white', width=400, height=100)
        self.patient_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        # Ensure the patient_frame expands correctly
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

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
