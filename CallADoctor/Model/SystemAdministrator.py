import tkinter as tk
from tkinter import messagebox

class SystemAdministrator:
    def __init__(self):
        self.systemAdmin_id = None
        self.name = None
        self.email = None
        self.phone_number = None
        self.requests = [] 

    def approveClinic(self,clinic ):
        clinic['status'] = 'Approved'
        messagebox.showinfo("Success", f"Clinic {clinic['name']} approved successfully!")
        self.updateRequestList()

    def rejectClinic(self,clinic ):
        clinic['status'] = 'Rejected'
        messagebox.showinfo("Success", f"Clinic {clinic['name']} rejected.")
        self.updateRequestList()

    def manageClinics(self, ):
         self.window = tk.Tk()
         self.window.title("Manage Clinic Requests")
         self.window.geometry("800x500")

         search_frame = tk.Frame(self.window)
         search_frame.pack(fill="x", padx=20, pady=10)

         tk.Label(search_frame, text="Search by Name:").pack(side="left", padx=5)
         self.search_name_entry = tk.Entry(search_frame)
         self.search_name_entry.pack(side="left", padx=5)

         tk.Label(search_frame, text="Search by State:").pack(side="left", padx=5)
         self.search_state_var = tk.StringVar()
         self.search_state_var.set("All")
         self.states = ["All", "Johor", "Kedah", "Kelantan", "Malacca", "Negeri Sembilan", "Pahang", "Penang", "Perak", "Perlis", "Sabah", "Sarawak", "Selangor", "Terengganu", "Kuala Lumpur", "Labuan", "Putrajaya"]
         self.search_state_menu = tk.OptionMenu(search_frame, self.search_state_var, *self.states)
         self.search_state_menu.pack(side="left", padx=5)

         tk.Button(search_frame, text="Search", command=self.updateRequestList).pack(side="left", padx=5)

         self.request_list_frame = tk.Frame(self.window)
         self.request_list_frame.pack(fill="both", expand=True, padx=20, pady=20)

         self.updateRequestList()

         self.window.mainloop()


    def updateRequestList(self):
        for widget in self.request_list_frame.winfo_children():
            widget.destroy()

        for clinic in self.requests:
            if clinic['status'] == 'Pending':
                frame = tk.Frame(self.request_list_frame, bd=2, relief="groove")
                frame.pack(fill="x", padx=5, pady=5)

                tk.Label(frame, text=f"Clinic Name: {clinic['name']}").pack(side="left", padx=5)
                tk.Button(frame, text="Approve", command=lambda c=clinic: self.approveClinic(c)).pack(side="right", padx=5)
                tk.Button(frame, text="Reject", command=lambda c=clinic: self.rejectClinic(c)).pack(side="right", padx=5)

