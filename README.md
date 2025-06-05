# SurveyAccuracyChecker
The program will do the necessary calculations for the user given the collected surveying data either by csv or manual input in order to confirm whether the closed traverse surveying data collected is within allowable accuracy standards or not and will then define the order of accuracy and display for the user. 
The inputs of this program are: reference azimuth (decimal degrees), interior angles(decimal degrees), interior angles(decimal degrees), 
backsight(meters), foresight(meters) and the known number of stations. The program calculates azimuths, average horizontal distance for lines, 
perimeter, latitudes, departures, error of misclosure, and the order of accuracy for the survey. 
- The user has the option to input data manually or uploading a csv file
- Outputs of the program are displayed on screen in a tabular format. The user also has the option to have the program map the surveyed location/data
  using latitude and longitude information. 

## Requirements

This program requires the following modules:
- math
- arcpy
- csv

## How to use the program

formatting csv data for survey 

If the user chooses 'A' for manual entries, the inputs are as follows:
- number of stations: interger data type
- reference azimuth: float data type
- interior angle: float data type
- backsight and foresights: float data type
- coordinate points (optional if the user would like the program to map the location): latitude/longitude are to be float data types, and not 
  entered as a string.

NOTE: the inputs listed above cannot be equal to zero, negative or be entered as a string. The interior angles also cannot exceed 360 degrees. 

If the user chooses 'B' for uploading a file, the csv file needs to be formatted as stated below:
- The first row is for the headers only and must be in the following sequence: station, inter angle, backsight, foresight. The first row will 
  skipped and not be executed within the program so do not include any test values within the first row. 
- Ensure that the data entries in the csv file are in order, starting from station one and only contain number values, no strings. 

## How to run the program

The user must choose between choices 'A' for manual input or 'B' for uploading a file, 

If the choice is 'A' follow below:

1. Enter the number of stations observed in the surveyed traverse
2. The reference azimuth must be entered in decimal degrees
3. Depending on the number of stations that were observed, it determine how many times the user must enter interior angles, backsight and foresight
4. After all appropriate values are entered, the user will be prompted with the option to have the surveyed located to be mapped using arcpy

IF the choice is 'B' follow below:

1. Enter the number of stations ovserved in the surveyed traverse
2. Enter the reference azimuth in decimal degrees
3. The user must then enter the name of the CSV file they are uploading

NOTE: for both maunal and uploaded entry options, if the user has chosen to have the surveyed data mapped, they will need to provide the path
to a .csv or .txt document that contains both latitudes and longitude values for their traverse. The format of this document will have headers in
row one, and these will be skipped when the program executes so ensure to not include data values in these. The uploaded document must have the 
values for longitude in the first column and values for latitude in the second column
- In the program, it will prompt the user to enter both the .csv file along with the workspace. Both of these files MUST be entered as the full file path where they are stored. 
- The .csv file must be stored in the folder where the geodatabase is located.
