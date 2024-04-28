Projet name : MeterReadingLookUp
Description : Hosts the application to  view all the available/ uploaded electricity consumption data flow files
              The application also supports searching of data based on MPAN or serial number of the electric meter
Application Name : Lookup

Input: Management command takes in file paths seperated by comma as command line argument
example : "python3 manage.py parse_file /Users/raofamily/myproject/MeterReadingLookup/MeterReadingLookup/files/D0010_Sample1.txt,
            /Users/raofamily/myproject/MeterReadingLookup/MeterReadingLookup/files/D0010_Sample2.txt"

Assumptions: 
  - Data flow files are available locally and placed in ../myproject/MeterReadingLookup/MeterReadingLookup/files/  folder.
  - 2 sample files are created and placed in above path to test the application and parser code.
  - The file is assumed to have the main MPAN_core fields and only relevant data fields are extracted.
  - Only admin ( username: admin, password: meghanarao) is authenticated and allowed to login and upload, view or search for meter reading data as of now.

Enhancements
    - Adding  mmultiple user registration authentication capabilities
    - Adding nested database schema and parsing of the nested data from file with error handling for missing levels from flow file as per the specification
    - Using Django rest framework to serialize the large data


    
