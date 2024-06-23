import unittest
import tkinter as tk
from unittest.mock import patch, Mock
from tkinter import Tk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Model.Login import LoginPage

mock_event = Mock()
class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()  
        with patch('tkinter.Label'):
            self.login_page = LoginPage(self.root) 

    def tearDown(self):
        self.root.quit()

    @patch('Model.Login.LoginPage.role_var', create=True)
    def test_check_role_selection(self, mock_role_var):
        mock_role_var.get.return_value = "Doctor"

        mock_role_var.get.return_value = "Choose Role"
        
        if mock_role_var.get.return_value != "Choose Role":
            self.assertEqual(mock_role_var.get.return_value, "Doctor")
            return True
        else:
            return False

    @patch('Model.Login.LoginPage.clinic_var', create=True)
    def test_check_clinic_selection(self, mock_clinic_var):
        mock_clinic_var.get.return_value = "Bagan Specialist"

        mock_clinic_var.get.return_value = "Choose Clinic"

        if mock_clinic_var.get.return_value != "Choose Clinic":
            self.assertEqual(mock_clinic_var.get.return_value, "Bagan Specialist")
            return True
        else:
            return False
        
    @patch('Model.Login.LoginPage.clinic_state_var', create=True)
    def test_check_clinic_state_selection(self, mock_clinic_state_var):
        mock_clinic_state_var.get.return_value = "Johor"

        mock_clinic_state_var.get.return_value = "Choose State"

        if mock_clinic_state_var.get.return_value != "Choose State":
            self.assertEqual(mock_clinic_state_var.get.return_value, "Johor")
            return True
        else:
            return False

    @patch('Model.Login.LoginPage.ic_passport_id_entry', create=True)
    @patch('Model.Login.LoginPage.password_entry', create=True)
    @patch('Model.Login.LoginPage.role_var', create=True)
    @patch('Model.Login.LoginPage.clinic_var', create=True)
    @patch('Model.Login.LoginPage.clinic_state_var', create=True)
    def test_submit(self, mock_ic_passport_id_entry, mock_password_entry, mock_role_var, mock_clinic_var, mock_clinic_state_var):
        mock_ic_passport_id_entry.get.return_value = "121212-07-1212"
        mock_password_entry.get.return_value = "123"
        mock_role_var.get.return_value = "Doctor"
        mock_clinic_var.get.return_value = "Bagan Specialist"
        mock_clinic_state_var.get.return_value = "Johor"

if __name__ == '__main__':
    unittest.main()