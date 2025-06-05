# group2assignment3.py
# Created by: Ashley Allan, Jessica Murdoch, Khazana Ahmadli, Lorissa Lowy
# November 2022
# Calculates the order of accuracy for a horizontal traverse survey
# Uses a reference bearing (in DD), interior angles (in DD), backsight (m), foresight (m) and known number of stations
# Calculates bearings and average horizontal distances for lines, angle of misclosure for traverse, and order of accuracy for survey
# Inputs are uploaded in csv file format
# Outputs are displayed on screen

# import from library
import math, arcpy, csv
from os import path, access, R_OK


def CalculateAzimuths(ref_azimuth: float, interior_angles: list): #Lori Lowy
    """Function for calculating azimuths for each station based on input reference azimuth and interior angles. Returns float value azimuth"""
    azimuths = []                                                   # create empty list for azimuths
    for i in range(len(interior_angles)):
        if i == 0:                                                  # first azimuth entry is the reference azimuth
            azimuths.append(ref_azimuth)
        elif i == 1:                                                # second azimuth calculated from reference azimuth
            check_azimuth = ref_azimuth + interior_angles[i]
            if check_azimuth <= 180:
                check_azimuth += 180
            else:                          
                check_azimuth -= 180
            prev_azimuth = check_azimuth
            azimuths.append(check_azimuth)
        else:
            check_azimuth = prev_azimuth + interior_angles[i]       # next azimuth calculated using previous azimuth + interior angle
            if check_azimuth <= 180:
                check_azimuth += 180
            else:
                check_azimuth -= 180
            prev_azimuth = check_azimuth
            azimuths.append(check_azimuth)
    return azimuths


def CalculateHorizontalDistance(backsights: list, foresights: list): # Khazana Ahmadli
    """Function takes input backsight and foresight for a station and will calculate horizontal distance. Returns float value horizontal distance."""
    horizontal_dist = []                                            # create empty list for horizontal distances
    for i in range(len(backsights)):
        hd = (backsights[i] + foresights[i]) / 2
        horizontal_dist.append(hd)                                  #add horizontal distance to list
    return horizontal_dist


def CalculatePerimeter(horizontal_dist: list): #Lori Lowy
    """Function takes input list of horizontal distances for a survey and return the perimeter float value"""
    return sum(horizontal_dist)


def CalculateLatitude(horizontal_dist: list, azimuths: list): # Khazana Ahmadli
    """Function will take unput list of horizontal distance and list of azimuths and calculates and returns list of latitudes"""
    latitudes = []                                                  #create empty list for latitudes
    for i in range(len(horizontal_dist)):
        lat = horizontal_dist[i] * math.cos(math.radians(azimuths[i])) #Lori Lowy
        latitudes.append(lat)                                       #add latitudes to the list
    return latitudes


def CalculateDepartures(horizontal_dist: list, azimuths: list): # Khazana Ahmadli
    """Function will take input list horizontal distance and list azimuths and will calculate and return list of departures"""
    departures = []
    for i in range(len(horizontal_dist)):
        dep = horizontal_dist[i] * math.sin(math.radians(azimuths[i]))
        departures.append(dep)
    return departures


def CalculateSumofInteriorAngles(interior_angles: list): #Lori Lowy
    """Function for calculating the sum of interior angles. Take input list of interior angles and returns float value sum"""
    return sum(interior_angles)


def CalculateErrorofClosure(departures: list, latitudes: list): # Khazana Ahmadli
    """Function takes input departures list and latitudes list and returns the error of closure"""
    return math.sqrt(math.fsum(departures)**2 + math.fsum(latitudes)**2)


def CalculateAccuracy(error_closure: float, perimeter: float): #Lori Lowy
    """Function takes input error of closure and perimeter and returns the level of accuracy, where level 1
    is most accurate and level 3 is least accurate"""
    #First order: 1:25000 (most accurate)
    #Second order: 1:10000
    #Third order: 1:5000 (least accurate)
    #accuracy = (error_closure/error_closure) / (perimeter/error_closure) # 0.50001 = 1/50001
    perimeter_ratio = round(round((perimeter/error_closure),-1))    #rounds to the nearest 10th and gets rid of decimal places
    if len(str(perimeter_ratio)) < 4:                               #ensures value is in the 1000s
        perimeter_ratio = int(str(perimeter_ratio) + "0")           #adds an extra zero if value is in 100s
    accuracy_statement = ""
    if perimeter_ratio >= 25000:
        accuracy_statement = "First Order Accuracy"
    elif perimeter_ratio >= 10000:
        accuracy_statement = "Second Order Accuracy"
    elif perimeter_ratio >= 5000:
        accuracy_statement = "Third Order Accuracy"
    else:
        accuracy_statement = "Not in Order Accuracy"
    return accuracy_statement, f"1/{perimeter_ratio}"               # formats order of accuracy in fraction format


# Main function
def main():


    # Display program purpose                                                            #Ashley Allan (all choices options), Lori Lowy (if statements for inputs)
    print("Calculates the order of accuracy for a horizontal traverse survey")
    print("---------------------------------------------------------------------------------")
    print()

    ############### Begin input ################

    # Obtain data input method from user
    print("A. Manual Input")
    print("B. Upload File")
    choice = str(input("Data entry choice, A or B: "))
    
    # lists to hold user input
    input_interiorangle = []         			                    # create empty list for interior angles
    input_backsight = []                  	                        # create empty list for backsights
    input_foresight = []                                            # create empty list for foresights

    if choice.upper() == "A":                                                                                            
        print("You chose item A")
        
        # Obtain number of stations, reference bearing, interior angles, backsights, and foresights from the user manually
        try:                                                        # Error handler begin
            num_stations = int(input("Enter number of stations: "))
            if num_stations <= 0:                                   # if number of stations is invalid, ask for input again
                print("Number of stations must be greater than 0")
                num_stations = int(input("Enter number of stations: "))
            
            reference_azimuth= float(input("Enter reference azimuth in decimal degrees: "))
            if reference_azimuth <= 0:                              # if azimuth entry is invalid, ask for input again
                print("Reference azimuth must be greater than 0") 
                reference_azimuth = float(input("Enter reference azimuth in decimal degrees: "))

            for i in range(num_stations):
                print("Station ", i + 1)
                
                interior_angle = float(input("     Interior angle in decimal degrees:"))
                if interior_angle <= 0 or interior_angle > 360:     # if interior angle entry is invalid, ask for input again
                    print("Interior angle must be greater than 0 and less than 360") 
                    interior_angle = float(input("     Interior angle in decimal degrees:"))
                input_interiorangle.append(interior_angle)			# add interior angle to input_interiorangle list
                
                backsight = float(input("     Backsight in meters:"))
                if backsight <= 0:                                  # if backsight entry is invalid, ask for input again
                    print("Backsight must be greater than or equal to 0")
                    backsight = float(input("     Backsight in meters:"))
                input_backsight.append(backsight)		            # add backsight to input_backsight list
                
                foresight = float(input("     Foresight in meters:"))
                if foresight <= 0:                                  # if foresight entry is invalid, ask for input again
                    print("Foresight must be greater than or equal to 0")
                    foresight = float(input("     Foresight in meters:"))
                input_foresight.append(foresight) 		            # add foresight to input_foresight list
                print()
        
        except ValueError as msg:                                   # Error handler end
            print("Error:", msg)                                    # Print error as message
            print("Exiting program")                        
            exit()                                                  # Exit program


    # Obtain number of stations, reference bearing, interior angles, backsights, and foresights from the user csv file
    elif choice.upper() == "B":
        print("You chose item B")
                                                   # Error handler begin
        # Obtain number of stations, reference azimuth from the user
        num_stations = int(input("Enter number of stations: "))
        if num_stations <= 0:                                   # if number of stations is invalid, ask for input again
            print("Number of stations must be greater than 0")
            num_stations = int(input("Enter number of stations: "))
        
        reference_azimuth= float(input("Enter reference azimuth in decimal degrees: "))
        if reference_azimuth <= 0:                              # if azimuth entry is invalid, ask for input again
            print("Reference azimuth must be greater than 0") 
            reference_azimuth = float(input("Enter reference azimuth in decimal degrees: "))

        # Read csv
        try:
            fName = str(input("Please enter CSV file name: "))          # user input CSV file name
            if path.exists(fName) and path.isfile(fName) and access(fName, R_OK):   # if file exists and is readable, print message
                print("File exists and is readable")        
                f_open = open(fName)                        # open csv file
                data = csv.reader(f_open)                   # csv reader
                next(data)                                  # skip row of column titles
                data = list(data)                           # converts csv to list

                for row in data:
                    interior_angle = float(row[1])
                    input_interiorangle.append(interior_angle)      # add interior_angle to input_interiorangle list
                    backsight = float(row[2])
                    input_backsight.append(backsight)               # add backsight to input_backsight list
                    foresight = float(row[3])
                    input_foresight.append(foresight)               # add foresight to input_foresight list
                f_open.close()                                      # close csv file
                print("Read successful")
            else:                       # if file file is missing or is not readable, print message
                print("Either file is missing or is not readable")

        except IOError:                 # if IOError occurs, print messagee
            print("Can\'t find file or read")
            exit()                      # program terminates if no input is provided

    else:                               # if choice entered is invalid, print message
        print("Your choice is not in the options")
        exit()
            
        


    # Obtain input from user (Y/N) to have program display map of the survey location              # Khazana Ahmadli (all arcpy), Ashley (try except)
    try:                                                            # Error handler begin
        map_location = input("Would you like to map the survey location? (Y/N): ")
        if map_location.lower() == "y":
            try:                                                    # Error handler begin
                in_table = input("Enter .csv or .txt file path: ")
                if path.exists(in_table) and path.isfile(in_table) and access(in_table, R_OK):   
                    print("File exists and is readable")            # if file exists and is readable, print message
                    ws = input("Enter workspace location: ")
                    # start of arcpy
                    arcpy.env.workspace = ws
                    out_feature_class = "mapped_traverse"
                    x_coord = "X_Point"
                    y_coord = "Y_Point"
                    spatial_ref = arcpy.SpatialReference(4326)
                    # make xy event layer
                    arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coord, y_coord, "", spatial_ref)
                    print(arcpy.GetCount_management(out_feature_class))
                else:                                               # if file file is missing or is not readable, print message
                    print("Either file is missing or is not readable")
            except ValueError as msg:
                print("Error: ", msg)
        elif map_location.lower() == "n":
            print("You have chosen not to map the survey location")
        elif not map_location.lower() == "y" or not map_location.lower() == "n":
            print("Your choice is not in the options")              # if option is invalid, print message
            print("Unable to map the survey location")    
    except Exception as msg:                                        # Error handler end
        print("Error:", msg)                                        # Print error message


    ############### End of input, Start of calculations ################
                            
    #Begin Calculations                                                           # Jessica Murdoch (calculations)
    azimuths = CalculateAzimuths(reference_azimuth, input_interiorangle)
    horizontal_distance = CalculateHorizontalDistance(input_backsight, input_foresight)
    perimeter = CalculatePerimeter(horizontal_distance)
    latitudes = CalculateLatitude(horizontal_distance, azimuths)
    departures = CalculateDepartures(horizontal_distance, azimuths)
    sum_interior_angles = CalculateSumofInteriorAngles(input_interiorangle)
    error_closure = CalculateErrorofClosure(departures, latitudes)
    accuracy = CalculateAccuracy(error_closure, perimeter)
    
    ############## End of calculations, Start of output #################

    #Display results                                            #Lori Lowy (results)
    print()
    print("Perimeter:", perimeter)
    print("Interior Angles Sum:", sum_interior_angles)
    print("Error of closure:", error_closure)
    print("Accuracy: ", accuracy)
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    # Display column header line
    print("Station No.\t\t  Azimuths\t\t Horizontal Distance\tLatitudes\t\tDepartures") 
    # Display table

    for i in range(num_stations):
        print(str(i+1), "\t\t\t ", str(round(azimuths[i],6)), "\t\t", str(round(horizontal_distance[i],6)), "\t\t", str(round(latitudes[i],6)), "\t\t", str(round(departures[i],6)))

if __name__ == '__main__':                                          # end of main function
    main()


print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------")
print()

print()
print("Done")