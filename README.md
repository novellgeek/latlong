This repositoru contains a number of Python Scripts for Downloading TLE files and converting results to LAT Long
All TLEs are downloaded from SpaceTrack.org which requires a user account
There are two conversions to lat long one has the TLE embeded and not very useful but was great for debugging 
The other file calls the TLE files from txt file which contains the TLE data 
The download TLE file only downloads data as defined in a CSV file , whichmakes thisngs very quick


The Lat_Long_from_TLE.py file is a Python script that calculates the latitude, longitude, and altitude of satellites using their Two-Line Element (TLE) data. Here is a summary of its functionality:

Dependencies: The script requires the following Python packages: numpy, pymap3d, astropy, and sgp4.
Function Definitions:
read_tle_from_file(file_path): Reads TLE data from a specified file.
get_satellite_lat_lon_alt(line1, line2): Computes the satellite's latitude, longitude, and altitude based on TLE lines.
Main Function:
Reads TLE data from a specified file.
Computes the satellite's position using the get_satellite_lat_lon_alt function.
Writes the satellite's name and computed positions to a CSV file.
The script reads TLE data from a file, calculates the satellite's current position, and saves the results in a CSV file.
