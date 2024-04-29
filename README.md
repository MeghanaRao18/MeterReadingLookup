Author : Meghana Rao
Email: mvmeghana@gmail.com

Projet name : MeterReadingLookUp
Description : 
•	Hosts the application to view all the available/ uploaded electricity consumption data flow files.
•	The application also supports searching for data based on MPAN or serial number of the electric meter.

Application Name : Lookup

•	This Application takes the file through the management command as command-line argument 
                             or
•	Once the user is logged in, the file can be uploaded through the web under the "Upload File" Option.


Prerequisited and installers
Virtual Env : OE_env - created the virtual environment inside project
              Python 3.12.3
              Django version 5.0.4
              database: PostgreSQL 16
              database name : mydatabase
              asgiref==3.8.1
              Django==5.0.4
              djangorestframework==3.15.1
              psycopg2-binary==2.9.9
              sqlparse==0.5.0



Assumptions: 
  
  1.	Data flow files are available locally and placed in ../myproject/MeterReadingLookup/MeterReadingLookup/files/  folder.
  2.	2 sample files are created and placed in above path to test the application and parser code.
  3.	The file is assumed to always have the main MPAN_core fields, and only relevant data fields ( not all fields) are extracted.
  4.	It is assumed that every MPAN_core field will have one serial_number associated. However Reading Registers can be multiple.
  5.	As of now, only the admin ( username: admin, password: meghanarao) is authenticated and allowed to log in and upload, view, or search for meter reading data.
  6.	Test cases are developed based on the above assumptions. 

App templates:

  - home/main page: Option to login
  - Login Page : To enter user name and password
  - Post Successful login : Home page with logout, View Files and Upload Files options
  - FlowFile_list   : Page to list all the uploaded or cmd line passed and stored files.
                 From here each file content can be viewed and searched or all the files data can be viewed and searched
  - FlowFile_Details:  Template to display all the contents of single or multiple files in a tabular form. This includes even Search Operation
  - Upload File : Browse the file from local path and upload to the application to be parsed and stored into Database
  - Upload status: Displays the status of the upload operation

Instruction To Setup

    1.  Transfer the Tarball to the Deployment Server
    2.	Extract the Tarball to any location: tar -xzvf MeghanaRao_project.tar.gz
    3.	Navigate to the extracted project directory and activate the virtual environment:
             source /path/to/your/venv/bin/activate/OE_env   
    4.  Install Dependencies: pip  install -r requirements.txt
    5.	Set Up the Database:
        - The database used for this project is PostgreSQL and the dump of the same is present in the project folder .. /MeterReadingLookup/dump_file.sql
        - If PostgreSQL is installed, create a new database using the below command
 		      createdb -U postgres your_database_name  
        -	Use the psql command-line tool.Replace your_database_name with the name database used in the project <mydatabase> and dump_file.sql with the <dump_file.sql> of the shared              database dump:
          psql -U postgres -d your_database_name -f dump_file.sql
        - Update Django Settings: Update your Django project's settings (settings.py) to point to the newly created PostgreSQL database.
    6.  Run DB Migration
          python manage.py migrate

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
       
      All the test case classes are defined in lookup/tests.py
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
1.	Adding multiple user registration authentication capabilities.
2.	Adding nested database schema and parsing of the nested data from a file with error handling for missing levels from the flow file as per the specification.
3.	Using Django rest framework to serialise the large data files.
4.	Model to have all the fields ( as per D0010 specification), parsing all of them from file to store into the database with thorough testing. Currently, only a few fields are handled and Stored.
5.	Elaborated test cases to validate  all the CRUD operations on all the fields of the database  
6.	A better and more scalable Database can be used to handle large, unstructured data files – for example MongoDB



    




              



    
