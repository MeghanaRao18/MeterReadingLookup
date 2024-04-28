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

              
Input: Management command takes in file paths seperated by comma as command line argument
example : "python3 manage.py parse_file /Users/raofamily/myproject/MeterReadingLookup/MeterReadingLookup/files/D0010_Sample1.txt,
            /Users/raofamily/myproject/MeterReadingLookup/MeterReadingLookup/files/D0010_Sample2.txt"

Assumptions: 
  - Data flow files are available locally and placed in ../myproject/MeterReadingLookup/MeterReadingLookup/files/  folder.
  - 2 sample files are created and placed in above path to test the application and parser code.
  - The file is assumed to have the main MPAN_core fields and only relevant data fields are extracted.
  - It is assumed that every MPAN_core field will have one serial_number associated. However Reading Registers can be multiple.
  - Only admin ( username: admin, password: meghanarao) is authenticated and allowed to login and upload, view or search for meter reading data as of now.

App templates:
  - home/main page: Option to login
  - Login Page : To enter user name and password
  - Post Successful login : Home page with logout, View Files and Upload Files options
  - : Page to list all the uploaded or cmd line passed and stored files.
                 From here each file content can be viewed and searched or all the files data can be viewed and searched
    - Upload File : Browse the file from local path and upload to the application to be parsed
    - 

    

Enhancements
    - Adding  mmultiple user registration authentication capabilities
    - Adding nested database schema and parsing of the nested data from file with error handling for missing levels from flow file as per the specification
    - Using Django rest framework to serialize the large data




              



    
