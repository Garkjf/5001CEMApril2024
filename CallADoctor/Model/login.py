import tkinter as tk
from tkinter import messagebox

# Main Application Window
class CallADoctorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Call a Doctor")
        self.geometry("600x400")

        self.frames = {}

        # Initialize different frames (screens) in the same window
        for F in (StartPage, PatientFrame, ClinicAdminFrame, DoctorFrame, SystemAdminFrame):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Display the start page initially
        self.show_frame(StartPage)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

# Start Page Frame
class StartPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Welcome to Call a Doctor!").pack(pady=20)

        tk.Button(self, text="Patient", command=lambda: parent.show_frame(PatientFrame)).pack(pady=10)
        tk.Button(self, text="Clinic Admin", command=lambda: parent.show_frame(ClinicAdminFrame)).pack(pady=10)
        tk.Button(self, text="Doctor", command=lambda: parent.show_frame(DoctorFrame)).pack(pady=10)
        tk.Button(self, text="System Admin", command=lambda: parent.show_frame(SystemAdminFrame)).pack(pady=10)

# Patient Frame
class PatientFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Button(self, text="<-", command=lambda: parent.show_frame(StartPage)).pack(pady=10)
        tk.Label(self, text="Patient Features").pack(pady=10)

        tk.Button(self, text="View Clinics", command=self.view_clinics).pack(pady=10)
        tk.Button(self, text="Send Request", command=self.send_request).pack(pady=10)

    def view_clinics(self):
        messagebox.showinfo("Clinics", "Display clinics")

    def send_request(self):
        messagebox.showinfo("Request", "Send request")

# Clinic Admin Frame
class ClinicAdminFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Button(self, text="<-", command=lambda: parent.show_frame(StartPage)).pack(pady=10)
        tk.Label(self, text="Clinic Admin Features").pack(pady=10)

        tk.Button(self, text="Add Doctor", command=self.add_doctor).pack(pady=10)
        tk.Button(self, text="Manage Requests", command=self.manage_requests).pack(pady=10)

    def add_doctor(self):
        messagebox.showinfo("Doctor", "Add new doctor")

    def manage_requests(self):
        messagebox.showinfo("Requests", "Manage requests")

# Doctor Frame
class DoctorFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Button(self, text="<-", command=lambda: parent.show_frame(StartPage)).pack(pady=10)
        tk.Label(self, text="Doctor Features").pack(pady=10)

        tk.Button(self, text="View Requests", command=self.view_requests).pack(pady=10)
        tk.Button(self, text="Generate Prescription", command=self.generate_prescription).pack(pady=10)

    def view_requests(self):
        messagebox.showinfo("Requests", "View assigned requests")

    def generate_prescription(self):
        messagebox.showinfo("Prescription", "Generate prescription")

# System Admin Frame
class SystemAdminFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Button(self, text="<-", command=lambda: parent.show_frame(StartPage)).pack(pady=10)
        tk.Label(self, text="System Admin Features").pack(pady=10)

        tk.Button(self, text="Approve Clinics", command=self.approve_clinics).pack(pady=10)
        tk.Button(self, text="View System Activity", command=self.view_system_activity).pack(pady=10)

    def approve_clinics(self):
        messagebox.showinfo("Clinics", "Approve clinics")

    def view_system_activity(self):
        messagebox.showinfo("System Activity", "View system activity")

# Main Execution
if __name__ == "__main__":
    app = CallADoctorApp()
    app.mainloop()