import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from datetime import datetime
import pytz
import os
import sys

# Ensure the service account key file is in the correct directory
dir = os.path.dirname(__file__)
serviceAccountKeyFile = os.path.join(dir, '../calladoctor-serviceAccountKey.json')

# Import the DoctorPage class
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Model.DoctorPage import DoctorPage

class TestDoctorCreateNewPrescription(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.patient_id = 222
        self.doctor_id = 111

        # Mock patients and doctors data
        self.mock_patients = {
            self.patient_id: {'username': 'Test123', 'email': 'Test123@gmail.com', 'phone': '012-3456789'}
        }
        self.mock_doctors = {
            str(self.doctor_id): {'username': 'Lisa', 'clinic_name': 'Bagan Specialist', 'phone': '011-0236542', 'specialist': 'Cardiology'}
        }

        # Patch the database reference to return the mock data
        patcher = patch('Model.DoctorPage.db.reference')
        self.addCleanup(patcher.stop)
        self.mock_db_reference = patcher.start()

        # Mock the return values for the database references
        self.mock_patients_ref = MagicMock()
        self.mock_doctors_ref = MagicMock()
        self.mock_prescriptions_ref = MagicMock()
        self.mock_db_reference.side_effect = lambda ref: {
            'patients': self.mock_patients_ref,
            'doctors': self.mock_doctors_ref,
            'prescriptions': self.mock_prescriptions_ref,
        }[ref]

        self.mock_patients_ref.get.return_value = self.mock_patients
        self.mock_doctors_ref.get.return_value = self.mock_doctors
        self.mock_prescriptions_ref.get.return_value = {}

        # Patch the getDefaultPatients method to return mock patients data
        patcher_get_default_patients = patch.object(DoctorPage, 'getDefaultPatients', return_value=self.mock_patients)
        self.addCleanup(patcher_get_default_patients.stop)
        patcher_get_default_patients.start()

        # Initialize the DoctorPage after setting up the mock database references
        self.doctor_page = DoctorPage(self.root, self.doctor_id)

    def tearDown(self):
        self.root.destroy()

    @patch('tkinter.messagebox.showinfo')
    @patch('Model.DoctorPage.datetime')
    def test_add_prescription(self, mock_datetime, mock_showinfo):
        # Mock current datetime
        mock_now = datetime(2024, 6, 23, 10, 0, 0, tzinfo=pytz.timezone('Asia/Kuala_Lumpur'))
        mock_datetime.now.return_value = mock_now

        # Call showAddPrescriptionPage to set up the entries
        self.doctor_page.showAddPrescriptionPage(self.patient_id)

        # Set values in the form
        self.doctor_page.symptoms_entry.insert(0, 'Cough and fever')  
        self.doctor_page.diagnosis_entry.insert(0, 'Flu')             
        self.doctor_page.treatment_entry.insert(0, 'Rest and hydration') 
        self.doctor_page.remark_entry.insert('1.0', 'Monitor temperature daily.') 

        # Call addPrescription method
        self.doctor_page.addPrescription(self.patient_id)

        # Verify that the prescription data is pushed to the database
        expected_prescription = {
            "diagnosis": 'Flu',
            "treatment": 'Rest and hydration',
            "remark": 'Monitor temperature daily.',
            "symptoms": 'Cough and fever',
            "patientID": self.patient_id,
            "doctorID": self.doctor_id,
            "created_at": mock_now.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.mock_prescriptions_ref.push.assert_called_once_with(expected_prescription)

        # Verify that the success message box is shown
        mock_showinfo.assert_called_once_with("Success", "Created new prescription!")

if __name__ == '__main__':
    unittest.main()
