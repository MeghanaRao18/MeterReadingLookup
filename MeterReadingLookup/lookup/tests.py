from django.test import TestCase, Client
from django.urls import reverse
from .models import ParsedData,RegisterReadings
from lookup.management.commands import parse_file
import sys
from datetime import datetime
class FileParsingTestCase(TestCase):
    """
    Test cases to validate upload file and parsing through command line.
    """
    def test_cmdline_fileparsing(self):

        # Create a test file
        test_file = open('test_file.txt', 'w')
        test_file.close()

        # passing empty file, Test should fail as the file doesn't meet the D0010 spec
        try:
            parse_file.Command().handle(file_path='test_file.txt')
            self.assertTrue(False)
        except ValueError:
              print(" #### Test passed ####")

        # passing no file, Test should Fail as file does not exist to parse
        try:
            parse_file.Command().handle(file_path='')
            self.assertTrue(False)
        except FileNotFoundError:
            print(" #### Test passed ####")

        # passing non standard D0010 file content format
        test_file = open('test_file.txt', 'w')
        test_file.write('Hello World')
        test_file.close()
        try:
            parse_file.Command().handle(file_path='test_file.txt')
            self.assertTrue(False) 
        except ValueError:
            print(" #### Test passed ####")

class UploadFileTestCase(TestCase):
    """
    Test cases to validate upload file through web page functionality
    """

    def test_upload_file(self):
        # Create a test file with random file content
        test_file = open('test_file.txt', 'w')
        test_file.write('Hello World')
        test_file.close()
        test_file = open('test_file.txt', 'r')


        # Simulate file upload
        client = Client()
        response = client.post(reverse('upload_file'), {'file': test_file})

        # Check if file  upload fails due to invalid format
        self.assertEqual(response.status_code, 200)
        self.assertFalse(RegisterReadings.objects.filter(mpan__file_name='test_file.txt').exists())
        print(" #### Test passed ####")

        test_file.close()

         # Create a test file with valid D0010 file content
        test_file = open('test_file.txt', 'w')
        test_file.write('026|1200023305967|V|')
        test_file.close()
        test_file = open('test_file.txt', 'r')


        # Simulate file upload
        client = Client()
        response = client.post(reverse('upload_file'), {'file': test_file})

        # Check if file  upload is successful
        self.assertEqual(response.status_code, 200)
        self.assertTrue(RegisterReadings.objects.filter(mpan__file_name='test_file.txt').exists())
        test_file.close()
        print(" #### Test passed ####")

        # create a file such that  invalid Model fields enters the database

        test_file = open('test_file.txt', 'w')

        # file with  invalid  reading Type field with more than max  character size
        test_file.write('026|1200023305967|V|\n028|S85D24767|CAS|')
        test_file.close()
        test_file = open('test_file.txt', 'r')


        # Simulate file upload
        client = Client()
        response = client.post(reverse('upload_file'), {'file': test_file})

        # Check if file  upload is unsuccessful
        self.assertEqual(response.status_code, 200)
        try:
            RegisterReadings.objects.filter(mpan__file_name='test_file.txt')
            self.assertTrue(False)
        except Exception:
            sys.stdout.write(" Test passed")

        test_file.close()

class DisplayFilesTestCase(TestCase):

    """
    Test cases to validate display of all uploaded files/parsed file
    """
    def test_display_filelist(self):

        sys.stdout.write("Running the test to validate the display of all the files available\n")

        # Create a test file
        mpan_obj = ParsedData.objects.create(file_name='test_file.txt', MPAN_Core='12345')
        RegisterReadings.objects.create(meter_id="",
                                        reading_date_time=datetime.strptime("11111111111111",'%Y%m%d%H%M%S'),
                                        register_reading=0.0, reading_method="", reading_flag="",
                                        reading_reason_code="",
                                        reading_status="", site_visit_check_code="", mpan=mpan_obj)

        files = RegisterReadings.objects.values_list('mpan__file_name', flat=True).distinct()

        # Simulate request to view file
        client = Client()
        response = client.post(reverse('flowfile_list'), {'file': files})

        # Check if file names are  displayed correctly
        self.assertEqual(response.status_code, 200)
        self.assertIn('test_file', response.content.decode())
        sys.stdout.write(" Test passed\n")


    def test_display_fileContent(self):
        """
        Test cases to validate display the contents of the selected file
        """

        sys.stdout.write('Running the test to validate the display of all the file contents\n')

        # Create 2 sample test files
        mpan_obj = ParsedData.objects.create(file_name='test_file_1.txt', MPAN_Core='12345')
        RegisterReadings.objects.create(meter_id="",
                                        reading_date_time=datetime.now(),
                                        register_reading=1.0, reading_method="V", reading_flag="T",
                                        reading_reason_code="Z",
                                        reading_status="T", site_visit_check_code="", mpan=mpan_obj)

        mpan_obj = ParsedData.objects.create(file_name='test_file_2.txt', MPAN_Core='989898')
        RegisterReadings.objects.create(meter_id="",
                                        reading_date_time=datetime.now(),
                                        register_reading=2.0, reading_method="C", reading_flag="T",
                                        reading_reason_code="Z",
                                        reading_status="F", site_visit_check_code="", mpan=mpan_obj)

        file_readings = RegisterReadings.objects.filter(mpan__file_name='test_file_1.txt')
        client = Client()
        # Simulate the request to view contents of  file 1

        response = client.post(reverse('flowfile_detail', kwargs={'file_name': 'test_file_1.txt'}),
                               {'file': file_readings})

        # Check if file names are listed  correctly

        self.assertEqual(response.status_code, 200)
        self.assertIn('test_file_1.txt', response.content.decode())
        self.assertIn('12345', response.content.decode())

        sys.stdout.write(" File 1 Contents Displayed and Verified. Test Passed\n")

        file_readings = RegisterReadings.objects.filter(mpan__file_name='test_file_2.txt')
        client = Client()
        # Simulate the request to view contents of  file 1

        response = client.post(reverse('flowfile_detail', kwargs={'file_name': 'test_file_2.txt'}),
                               {'file': file_readings})

        # Check if file names are listed  correctly

        self.assertEqual(response.status_code, 200)
        self.assertIn('test_file_2.txt', response.content.decode())
        self.assertIn('989898', response.content.decode())

        sys.stdout.write(" File 2 Contents Displayed and Verified. Test Passed\n")
        sys.stdout.write(" Test passed\n")

class SearchOperationTestCase(TestCase):

    """
    Class containing tests to validate search operation
    """

    def setUp(self):

        # create 2 sample file entries into database
        mpan_obj = ParsedData.objects.create(file_name='test_file_1.txt', MPAN_Core='12345',serial_number='F123FA')
        RegisterReadings.objects.create(meter_id="",
                                        reading_date_time=datetime.now(),
                                        register_reading=2.0, reading_method="V", reading_flag="T",
                                        reading_reason_code="Z",
                                        reading_status="F", site_visit_check_code="", mpan=mpan_obj)

        self.test_file_1 = RegisterReadings.objects.filter(mpan__file_name='test_file_1.txt')
        mpan_obj = ParsedData.objects.create(file_name='test_file_2.txt', MPAN_Core='989898',serial_number='100ABC')
        RegisterReadings.objects.create(meter_id="",
                                        reading_date_time=datetime.now(),
                                        register_reading=2.0, reading_method="C", reading_flag="F",
                                        reading_reason_code="Z",
                                        reading_status="F", site_visit_check_code="", mpan=mpan_obj)
        self.test_file_2 = RegisterReadings.objects.filter(mpan__file_name='test_file_2.txt')


    def test_search_withMPAN(self):

        sys.stdout.write('Running the test to validate the search using MPAN \n')
        client = Client()
        response = client.post(reverse('flowfile_detail', kwargs={'file_name': 'test_file_1.txt'}),
                               {'file': self.test_file_1})
        self.assertEqual(response.status_code, 200)
        self.assertIn('test_file_1.txt', response.content.decode())
        self.assertNotIn('test_file_2.txt', response.content.decode())
        sys.stdout.write(" Test passed\n")

    def test_search_withSerialNo(self):
        sys.stdout.write('Running the test to validate the search using serial No \n')

        client = Client()
        response = client.post(reverse('flowfile_detail', kwargs={'file_name': 'test_file_2.txt'}),
                               {'file': self.test_file_2})

        self.assertEqual(response.status_code, 200)
        self.assertIn('100ABC', response.content.decode())
        self.assertNotIn('F123FA', response.content.decode())
        sys.stdout.write(" Test passed\n")