import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font, BOLD
import os
import sys

# Ensure the service account key file is in the correct directory
dir = os.path.dirname(__file__)
serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')

# Import the PatientPage class
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Model.PatientPage import PatientPage

class TestSearchClinic(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.patient_id = 123
        self.patient_page = PatientPage(self.root, self.patient_id)

    def tearDown(self):
        self.root.destroy()

    @patch('Model.PatientPage.db.reference')
    @patch.object(PatientPage, 'clearClinicInfo')
    @patch.object(PatientPage, 'clearFilters')
    @patch.object(PatientPage, 'displayClinicInfo')
    def test_search_clinic(self, mock_displayClinicInfo, mock_clearFilters, mock_clearClinicInfo, mock_db_reference):
        # Mocking the database reference
        mock_clinic_ref = MagicMock()
        mock_db_reference.return_value = mock_clinic_ref

        # Mock clinic data
        mock_clinic_data = {
            'clinic1': {'clinic_name': 'Sunway Clinic', 'clinic_state': 'Johor', 'status': 'Approved'},
            'clinic2': {'clinic_name': 'Clinic Theesan', 'clinic_state': 'Penang', 'status': 'Approved'},
            'clinic3': {'clinic_name': 'Bagan Specialist', 'clinic_state': 'Kuala Lumpur', 'status': 'Pending'},
            'clinic4': {'clinic_name': 'Bagan Ajam', 'clinic_state': 'Kedah', 'status': 'Approved'}
        }
        mock_clinic_ref.get.return_value = mock_clinic_data

        # Call the method
        self.patient_page.searchClinic()

        # Verify method calls
        mock_clearClinicInfo.assert_called_once()
        mock_clearFilters.assert_called_once()
        mock_displayClinicInfo.assert_called_once()

        # Verify that the comboboxes have the correct values
        expected_clinic_names = ['All Clinic', 'Sunway Clinic', 'Clinic Theesan', 'Bagan Specialist', 'Bagan Ajam']
        expected_clinic_states = ['All State', 'Johor', 'Penang', 'Kuala Lumpur', 'Kedah']

        self.assertEqual(list(self.patient_page.clinic_dropdown['values']), expected_clinic_names)
        self.assertEqual(list(self.patient_page.clinic_state_dropdown['values']), expected_clinic_states)

        # Verify default selections
        self.assertEqual(self.patient_page.clinic_state_var.get(), 'All State')
        self.assertEqual(self.patient_page.clinic_var.get(), 'All Clinic')

if __name__ == '__main__':
    unittest.main()