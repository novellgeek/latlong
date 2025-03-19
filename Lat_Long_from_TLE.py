# Requires
# pip install numpy
# pip install pymap3d
# pip install astropy
# pip install sgp4


from sgp4.api import Satrec, jday
from datetime import datetime, timezone
import numpy as np
import pymap3d as pm
from astropy.time import Time
from astropy.coordinates import EarthLocation, TEME, ITRS
from astropy import units as u
import csv

def read_tle_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        tle_data = [line.strip() for line in lines if line.strip()]
    return tle_data

# Function to compute satellite lat/lon/alt
def get_satellite_lat_lon_alt(line1, line2):
    satellite = Satrec.twoline2rv(line1, line2)

    # Get current UTC time
    current_time = datetime.now(timezone.utc)

    # Convert current time to Julian Date
    jd, fr = jday(current_time.year, current_time.month, current_time.day,
                  current_time.hour, current_time.minute, current_time.second)

    # Propagate the satellite's position
    error, r, v = satellite.sgp4(jd, fr)
    if error != 0:
        raise ValueError(f"SGP4 propagation error: {error}")

    # Extract ECI coordinates (in kilometers)
    x, y, z = r  # TEME (True Equator, Mean Equinox) frame

    # Convert TEME to ECEF using Astropy
    teme_coords = TEME(x=x * u.km, y=y * u.km, z=z * u.km,
                        representation_type="cartesian",
                        obstime=Time(jd + fr, format='jd', scale='utc'))

    ecef_coords = teme_coords.transform_to(ITRS(obstime=teme_coords.obstime))

    # Extract ECEF coordinates in meters
    xecef, yecef, zecef = ecef_coords.x.to(u.m).value, ecef_coords.y.to(u.m).value, ecef_coords.z.to(u.m).value

    # Convert from ECEF to geodetic latitude, longitude, and altitude
    lat, lon, alt = pm.ecef2geodetic(xecef, yecef, zecef)

    # Normalize longitude to be within 0° to 360° (East-positive)
    lon = lon % 360

    return lat, lon, alt

def main():
    file_path = "C:/Users/HP/Desktop/Python Scripts/spacetrack_TLE.txt"  # Update this path to your TLE file
    tle_data = read_tle_from_file(file_path)
    
    csv_file = "satellite_positions.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Satellite Name", "Latitude", "Longitude", "Altitude (meters)"])
        
        if len(tle_data) < 2:
            raise ValueError("Insufficient TLE data in the file")
        
        for i in range(0, len(tle_data), 3):
            if i + 2 < len(tle_data):
                sat_name = tle_data[i]
                line1 = tle_data[i + 1]
                line2 = tle_data[i + 2]
                lat, lon, alt = get_satellite_lat_lon_alt(line1, line2)
                lat_str = f"{abs(lat):.6f} {'N' if lat >= 0 else 'S'}"
                lon_str = f"{abs(lon):.6f} {'E' if lon >= 0 else 'W'}"
                writer.writerow([sat_name, lat_str, lon_str, f"{alt:.2f}"])

if __name__ == "__main__":
    main()