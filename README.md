Projet name : MeterReadingLookUp
Description : Hosts the application to  view all the available/ uploaded electricity consumption data flow files
              The application also supports searching of data based on MPAN or serial number of the electric meter

      
Application Name : Lookup

This Application takes the file through mamagement command as command line argument 
                             or
The File can be uploaded through web under "Upload File" Option once the user is logged in.


Prerequisited and installers
Virtual Env : OE_env - created the virtual environment inside project
              Python 3.12.3
              Django version 5.0.4
              database: PostgreSQL
              database name : mydatabase
              asgiref==3.8.1
              Django==5.0.4
              djangorestframework==3.15.1
              psycopg2-binary==2.9.9
              sqlparse==0.5.0



Assumptions: 
  
  - Data flow files are available locally and placed in ../myproject/MeterReadingLookup/MeterReadingLookup/files/  folder.
  - 2 sample files are created and placed in above path to test the application and parser code.
  - The file is assumed to always have the main MPAN_core fields and only relevant data fields are extracted ( not all fields).
  - It is assumed that every MPAN_core field will have one serial_number associated. However Reading Registers can be multiple.
  - Only admin ( username: admin, password: meghanarao) is authenticated and allowed to login and upload, view or search for meter reading data as of now.
  - Test cases are developed based on the above assumptions. 

App templates
  - home/main page: Option to login
  - Login Page : To enter user name and password
  - Post Successful login : Home page with logout, View Files and Upload Files options
  - FlowFile_list   : Page to list all the uploaded or cmd line passed and stored files.
                 From here each file content can be viewed and searched or all the files data can be viewed and searched
  - FlowFile_Details:  Template to display all the contents of single or multiple files in a tabular form. This includes even Search Operation
  - Upload File : Browse the file from local path and upload to the application to be parsed and stored into Database
  - Upload status: Displays the status of the upload operation
    
To Run the App:
    App name : lookup
    Step 1:  To pass the file as command line to management command and store in database. This framework can take single or multiple files to be parsed.
            python manage.py parse_file <file1, file2, file3 >
            Example :   python3 manage.py parse_file ../myproject/MeterReadingLookup/MeterReadingLookup/files/D0010_Sample1.txt, 
                     ../myproject/MeterReadingLookup/MeterReadingLookup/files/D0010_Sample2.txt
            NOTE: parse_file.py is located at MeterReadingLookup/lookup/management/commands/
    Step 2 : Once the data is stored in database. Start the application server
             python3 manage.py runserver

    Step 3 : Open the server at  http://127.0.0.1:8000/
             To access Admin page, goto  http://127.0.0.1:8000/admin
             Admin username : admin
             Admin password : meghanarao

    Step 4 : at  http://127.0.0.1:8000/  login with the above admin credentials and access the view file and click of each file and view the contents

    Step 5 : To upload a file , goto Upload file tab and browse to any txt file locally. On successful upload, the filename gets listed under <View Files>

 To Run the test cases:
   -  All the test case classes are defined in lookup/tests.py
   The test case Classes are as follows:
   1. FileParsingTestCase
   2. UploadFileTestCase
   3. DisplayFilesTestCase
   4. SearchOperationTestCase

   To Run the above classes together use the below cmd:
     -  python3 manage.py test lookup

   To Run tests in individual classes use the below cmd:
     - python3 manage.py test lookup.tests.<ClassName>


Enhancements
    - Adding mmultiple user registration authentication capabilities.
    - Adding nested database schema and parsing of the nested data from file with error handling for missing levels from flow file as per the specification
    - Using Django rest framework to serialize the large data files.
    - Model to have all the fields ( as per D0010 specification), parsing all of them from file to store into database with thorough testing. Currently only few fields are handled and 
      stored
    - Elaborated test cases to validate  all the CRUD operations on all the fields of the database  
    - Better and more scalable Database can be used to handle large, unstructured data files - example MongoDB
    




              



    
