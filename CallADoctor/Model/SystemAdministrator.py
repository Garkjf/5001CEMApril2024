import tkinter as tk
from tkinter import messagebox
import sys
import os
from firebase_admin import credentials, initialize_app ,db

dir = os.path.dirname(__file__)

serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')   # Change the path to your own serviceAccountKey.json
logoImageFile = os.path.join(dir, '../Images/CallADoctor-logo-small.png')  # Change the path to your own logo image
backIconImage = os.path.join(dir, '../Images/back-icon.png') # Change the path to your own logo image

class SystemAdministrator:
    def __init__(self, root):
        self.systemAdmin_id = None
        self.name = None
        self.email = None
        self.phone_number = None
        self.requests = {}
        # self.system_admin = system_admin

        self.window = root
        self.manageClinics()
        
        

    def approveClinic(self, clinic):
        clinic['status'] = 'Approved'
        messagebox.showinfo("Success", f"Clinic {clinic['clinic_name']} approved successfully!")
        self.updateRequestList()

    def rejectClinic(self, clinic):
        clinic['status'] = 'Rejected'
        messagebox.showinfo("Success", f"Clinic {clinic['clinic_name']} rejected.")
        self.updateRequestList()

    def manageClinics(self):
        cred = credentials.Certificate(serviceAccountKeyFile)
        initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})
        # get clinic information
        clinics_ref = db.reference('clinicAdmins')

        clinics = clinics_ref.get()
        self.requests = clinics

        clinic_state_options = ["All"]
        clinic_states = set()
    
        for status, clinic_data in clinics.items():
            clinic_state = clinic_data.get('clinic_state')
            if clinic_state not in clinic_states:
                clinic_state_options.append(clinic_state)
                clinic_states.add(clinic_state)

        search_frame = tk.Frame(self.window)
        search_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(search_frame, text="Search by Name:").pack(side="left", padx=5)
        self.search_name_entry = tk.Entry(search_frame)
        self.search_name_entry.pack(side="left", padx=5)

        tk.Label(search_frame, text="Search by State:").pack(side="left", padx=5)
        self.search_state_var = tk.StringVar()
        self.search_state_var.set("Choose State Clinics")
        self.search_state_menu = tk.OptionMenu(search_frame, self.search_state_var, *clinic_state_options)
        self.search_state_menu.pack(side="left", padx=5)

        tk.Button(search_frame, text="Search", command=self.updateRequestList).pack(side="left", padx=5)

        self.request_list_frame = tk.Frame(self.window)
        self.request_list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.updateRequestList()

    def updateRequestList(self):
        for widget in self.request_list_frame.winfo_children():
            widget.destroy()

        for clinic in self.requests.values():
            if clinic.get('status') == 'Pending':
                frame = tk.Frame(self.request_list_frame, bd=2, relief="groove")
                frame.pack(fill="x", padx=5, pady=5)

                tk.Label(frame, text=f"Clinic Name: {clinic['clinic_name']}").grid(row=0, column=0, padx=5, pady=5, sticky="w")
                tk.Label(frame, text=f"Clinic State: {clinic['clinic_state']}").grid(row=1, column=0, padx=5, pady=5, sticky="w")
                tk.Label(frame, text=f"Admin Name: {clinic['username']}").grid(row=2, column=0, padx=5, pady=5, sticky="w")
                tk.Label(frame, text=f"Email: {clinic['email']}").grid(row=3, column=0, padx=5, pady=5, sticky="w")
                tk.Button(frame, text="Approve", command=lambda c=clinic: self.approveClinic(c), fg="white", bg="blue").grid(row=2, column=3, padx=5, pady=5, sticky="e")
                tk.Button(frame, text="Reject", command=lambda c=clinic: self.rejectClinic(c), fg="white", bg="red").grid(row=3, column=3, padx=5, pady=5, sticky="e")



if __name__ == "__main__":
    system_admin = sys.argv[1] 

    root = tk.Tk()  # Create a new Tk root window
    root.title("Call a Doctor - System Administrator")  # Set the title of the window
    root.geometry("1200x600")
    root.configure(background='#f6f6e9')

    # Load the logo image
    logo = tk.PhotoImage(file=logoImageFile)
    logo = logo.subsample(4, 4)

    # get logo image size
    logo_width = logo.width()
    logo_height = logo.height()

    # navigation bar
    nav_bar = tk.Frame(root, background='#f6f6e9', height=logo_height, width=logo_width)
    nav_bar.pack(side="top", fill="x", padx=250, pady=10)
    
    # Create a main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)

    # Create a canvas inside the main frame
    my_canvas = tk.Canvas(main_frame, bg="#f6f6e9")
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # Add a vertical scrollbar to the canvas
    my_scrollbar_vertical = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas
    my_canvas.configure(yscrollcommand=my_scrollbar_vertical.set)

    # Create another frame inside the canvas
    second_frame = tk.Frame(my_canvas, bg="#f6f6e9", width=1200)

    # Add that new frame to a window in the canvas
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    # Update the scrollregion of the canvas to include the entire second_frame
    second_frame.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    # display image
    logo_label = tk.Label(nav_bar, image=logo)
    logo_label.pack(side="left", fill="x")   
 
    # Body
    app = SystemAdministrator(second_frame)  # Pass the second_frame window to your SystemAdministrator class

   

    # Add more buttons here as needed

    root.mainloop()
