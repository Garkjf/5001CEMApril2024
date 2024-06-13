import unittest
import tkinter as tk
from unittest.mock import patch, Mock
from tkinter import Tk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Model.Login import LoginPage
from Model.Registration import RegistrationPage

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
        mock_role_var.get.return_value = "Some Role"

        mock_role_var.get.return_value = "Choose Role"
        
        if mock_role_var.get.return_value != "Choose Role":
            self.assertEqual(mock_role_var.get.return_value, "Some Role")
            return True
        else:
            return False

    @patch('Model.Login.LoginPage.clinic_var', create=True)
    def test_check_clinic_selection(self, mock_clinic_var):
        mock_clinic_var.get.return_value = "Some Clinic"

        mock_clinic_var.get.return_value = "Choose Clinic"

        if mock_clinic_var.get.return_value != "Choose Clinic":
            self.assertEqual(mock_clinic_var.get.return_value, "Some Clinic")
            return True
        else:
            return False
        
    @patch('Model.Login.LoginPage.clinic_state_var', create=True)
    def test_check_clinic_state_selection(self, mock_clinic_state_var):
        mock_clinic_state_var.get.return_value = "Some State"

        mock_clinic_state_var.get.return_value = "Choose State"

        if mock_clinic_state_var.get.return_value != "Choose State":
            self.assertEqual(mock_clinic_state_var.get.return_value, "Some State")
            return True
        else:
            return False

    @patch('Model.Login.LoginPage.ic_passport_id_entry', create=True)
    @patch('Model.Login.LoginPage.password_entry', create=True)
    @patch('Model.Login.LoginPage.role_var', create=True)
    @patch('Model.Login.LoginPage.clinic_var', create=True)
    @patch('Model.Login.LoginPage.clinic_state_var', create=True)
    def test_submit(self, mock_ic_passport_id_entry, mock_password_entry, mock_role_var, mock_clinic_var, mock_clinic_state_var):
        mock_ic_passport_id_entry.get.return_value = "123456"
        mock_password_entry.get.return_value = "password"
        mock_role_var.get.return_value = "Doctor"
        mock_clinic_var.get.return_value = "Some Clinic"
        mock_clinic_state_var.get.return_value = "Some State"


class TestRegistrationPage(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()  
        with patch('tkinter.Label'):
            self.registration_page = RegistrationPage(self.root) 

    def tearDown(self):
        self.root.quit()

    @patch('Model.Registration.role_var', create=True)
    def test_check_role_selection(self, mock_role_var):
        mock_role_var.get.return_value = "Some Role"

        mock_role_var.get.return_value = "Choose Role"
        
        if mock_role_var.get.return_value != "Choose Role":
            self.assertEqual(mock_role_var.get.return_value, "Some Role")
            return True
        else:
            return False

    @patch('Model.Registration.clinic_var', create=True)
    def test_check_clinic_selection(self, mock_clinic_var):
        mock_clinic_var.get.return_value = "Some Clinic"

        mock_clinic_var.get.return_value = "Choose Clinic"

        if mock_clinic_var.get.return_value != "Choose Clinic":
            self.assertEqual(mock_clinic_var.get.return_value, "Some Clinic")
            return True
        else:
            return False
        
    @patch('Model.Registration.clinic_state_var', create=True)
    def test_check_clinic_state_selection(self, mock_clinic_state_var):
        mock_clinic_state_var.get.return_value = "Some State"

        mock_clinic_state_var.get.return_value = "Choose State"

        if mock_clinic_state_var.get.return_value != "Choose State":
            self.assertEqual(mock_clinic_state_var.get.return_value, "Some State")
            return True
        else:
            return False

    @patch('Model.Registration.validate_email')
    @patch('Model.Registration.validate_ic')
    @patch('Model.Registration.validate_passport')
    def test_submit(self, mock_validate_email, mock_validate_ic, mock_validate_passport):
        # Set the return values for the mocked methods
        mock_validate_email.return_value = True
        mock_validate_ic.return_value = True
        mock_validate_passport.return_value = True

        # Set the values for the Entry fields
        self.registration_page.username_entry.insert(0, "testuser")
        self.registration_page.email_entry.insert(0, "testuser@test.com")
        self.registration_page.phone_no_entry.insert(0, "012-3456789")
        self.registration_page.password_entry.insert(0, "password")
        self.registration_page.confirm_password_entry.insert(0, "password")
        self.registration_page.ic_passport_id_entry.insert(0, "1234567890")

        # Call the submit method
        # self.registration_page.submit()

        # Assert that the mocked methods were called
        mock_validate_email.assert_called_once_with("testuser@test.com")
        mock_validate_ic.assert_called_once_with("1234567890")
        mock_validate_passport.assert_called_once_with("1234567890")
    
if __name__ == '__main__':
    unittest.main()