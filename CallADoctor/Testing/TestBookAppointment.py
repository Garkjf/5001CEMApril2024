import unittest
import tkinter as tk
from unittest.mock import patch, Mock, MagicMock
from unittest import mock
from tkinter import Tk
from tkinter import ttk
import sys
import os
from datetime import datetime, timedelta
from firebase_admin import get_app, credentials, initialize_app
from firebase_helper import serviceAccountKeyFile
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Model.PatientPage import PatientPage

#  Assuming the service account key file is in the correct directory
dir = os.path.dirname(__file__)
serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')

class TestBookAppointment(unittest.TestCase):
    def setUp(self):
        try:
            # Attempt to get the Firebase app instance
            self.app = get_app()
        except ValueError:
            # Initialize Firebase if it's not already initialized
            cred = credentials.Certificate(serviceAccountKeyFile)
            self.app = initialize_app(cred, {'databaseURL': 'https://calladoctor-5001-default-rtdb.asia-southeast1.firebasedatabase.app/'})
        
        self.patient_id = 123  # Replace with actual patient ID
        self.root = tk.Tk()  # Example tkinder

        # Initialize your PatientPage instance with required arguments
        self.patient_page = PatientPage(self.root, self.patient_id)

    def tearDown(self):
        self.root.destroy()  # Destroy the Tkinter root window after each test

    @patch('Model.PatientPage.PatientPage.role_var', create=True)
    def test_check_role_selection(self, mock_role_var):
        mock_role_var.get.return_value = "Patient"
        self.assertEqual(mock_role_var.get.return_value, "Patient")

        mock_role_var.get.return_value = "Choose Role"
        self.assertNotEqual(mock_role_var.get.return_value, "Patient")

    @patch('Model.PatientPage.PatientPage.clinic_var', create=True)
    def test_check_clinic_selection(self, mock_clinic_var):
        mock_clinic_var.get.return_value = "Bagan Specialist"
        self.assertEqual(mock_clinic_var.get.return_value, "Bagan Specialist")

        mock_clinic_var.get.return_value = "Choose Clinic"
        self.assertNotEqual(mock_clinic_var.get.return_value, "Bagan Specialist")

    @patch('Model.PatientPage.PatientPage.clinic_state_var', create=True)
    def test_check_clinic_state_selection(self, mock_clinic_state_var):
        mock_clinic_state_var.get.return_value = "Johor"
        self.assertEqual(mock_clinic_state_var.get.return_value, "Johor")

        mock_clinic_state_var.get.return_value = "Choose State"
        self.assertNotEqual(mock_clinic_state_var.get.return_value, "Johor")

    @patch('Model.PatientPage.PatientPage.ic_passport_id_entry', create=True)
    @patch('Model.PatientPage.PatientPage.password_entry', create=True)
    @patch('Model.PatientPage.PatientPage.role_var', create=True)
    @patch('Model.PatientPage.PatientPage.clinic_var', create=True)
    @patch('Model.PatientPage.PatientPage.clinic_state_var', create=True)
    def test_submit(self, mock_ic_passport_id_entry, mock_password_entry, mock_role_var, mock_clinic_var, mock_clinic_state_var):
        mock_ic_passport_id_entry.get.return_value = "121212-07-1212"
        mock_password_entry.get.return_value = "123"
        mock_role_var.get.return_value = "Patient"
        mock_clinic_var.get.return_value = "Bagan Specialist"
        mock_clinic_state_var.get.return_value = "Johor"
        self.assertEqual(mock_ic_passport_id_entry.get.return_value, "121212-07-1212")
        self.assertEqual(mock_password_entry.get.return_value, "123")
        self.assertEqual(mock_role_var.get.return_value, "Patient")
        self.assertEqual(mock_clinic_var.get.return_value, "Bagan Specialist")
        self.assertEqual(mock_clinic_state_var.get.return_value, "Johor")

    @patch('Model.PatientPage.PatientPage.clearClinicInfo', create=True)
    @patch('Model.PatientPage.PatientPage.clearFilters', create=True)
    @patch('Model.PatientPage.PatientPage.check_clinic_selection', create=True)
    @patch('Model.PatientPage.PatientPage.check_clinic_state_selection', create=True)
    @patch('Model.PatientPage.PatientPage.check_doctor_specialty_selection', create=True)
    @patch('Model.PatientPage.PatientPage.check_doctor_name_selection', create=True)
    @patch('Model.PatientPage.PatientPage.check_date_selection', create=True)
    @patch('Model.PatientPage.PatientPage.check_time_selection', create=True)
    def test_make_appointment(self, mock_clear_clinic_info, mock_clear_filters, 
                              mock_check_clinic_selection, mock_check_clinic_state_selection, 
                              mock_check_doctor_specialty_selection, mock_check_doctor_name_selection,
                              mock_check_date_selection, mock_check_time_selection):
        with patch('Model.PatientPage.db.reference') as mock_db_ref:
            mock_db_ref.return_value.get.return_value = {
                'username': 'test123',
                'email': 'test123@gmail.com',
                'phone': '1234567890'
            }
            mock_db_ref.return_value.child.return_value.get.return_value = {
                'clinic_name': 'Bagan Specialist',
                'clinic_state': 'Johor',
                'username': 'Lisa',
                'specialist': 'Cardiologist',
                'status': 'Approved'
            }

            self.patient_page.makeAppointment('Bagan Specialist', 'Johor', 'Lisa', 'Cardiologist')
           
            self.assertEqual(self.patient_page.clinic_var.get(), 'Bagan Specialist')
            self.assertEqual(self.patient_page.clinic_state_var.get(), 'Johor')

if __name__ == '__main__':
    unittest.main()