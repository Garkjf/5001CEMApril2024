import unittest
import tkinter as tk
from unittest.mock import patch, Mock
from tkinter import Tk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Model.Registration import RegistrationPage

mock_event = Mock()

class TestRegistrationPage(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()  
        with patch('tkinter.Label'):
            self.registration_page = RegistrationPage(self.root) 

    def tearDown(self):
        self.root.quit()

    @patch('Model.Registration.role_var', create=True)
    def test_check_role_selection(self, mock_role_var):
        mock_role_var.get.return_value = "Patient"

        mock_role_var.get.return_value = "Choose Role"
        
        if mock_role_var.get.return_value != "Choose Role":
            self.assertEqual(mock_role_var.get.return_value, "Patient")
            return True
        else:
            return False

    @patch('Model.Registration.clinic_var', create=True)
    def test_check_clinic_selection(self, mock_clinic_var):
        mock_clinic_var.get.return_value = "Bagan Specialist"

        mock_clinic_var.get.return_value = "Choose Clinic"

        if mock_clinic_var.get.return_value != "Choose Clinic":
            self.assertEqual(mock_clinic_var.get.return_value, "Bagan Specialist")
            return True
        else:
            return False
        
    @patch('Model.Registration.clinic_state_var', create=True)
    def test_check_clinic_state_selection(self, mock_clinic_state_var):
        mock_clinic_state_var.get.return_value = "Johor"

        mock_clinic_state_var.get.return_value = "Choose State"

        if mock_clinic_state_var.get.return_value != "Choose State":
            self.assertEqual(mock_clinic_state_var.get.return_value, "Johor")
            return True
        else:
            return False

    def test_submit(self):

        # Set the values for the Entry fields
        self.registration_page.username_entry.insert(0, "test123")
        self.registration_page.email_entry.insert(0, "test123@gmail.com")
        self.registration_page.phone_no_entry.insert(0, "012-3456789")
        self.registration_page.password_entry.insert(0, "123")
        self.registration_page.confirm_password_entry.insert(0, "123")
        self.registration_page.ic_passport_id_entry.insert(0, "121212-07-1212")

if __name__ == '__main__':
    unittest.main()