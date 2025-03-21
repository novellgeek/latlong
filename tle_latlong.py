from sgp4.api import Satrec, jday
from datetime import datetime, timezone
import numpy as np
import pymap3d as pm
from astropy.time import Time
from astropy.coordinates import EarthLocation, TEME, ITRS
from astropy import units as u

# Define the TLE for TJS-10
tle_name = "TJS-10"
tle_line1 = "1 58204U 23169A   25073.71113927  .00000000  00000-0  00000+0 0  9997"
tle_line2 = "2 58204   1.3555  86.0418 0003920 202.7140 313.1699  1.00269225  5067"

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

# Compute satellite position
lat, lon, alt = get_satellite_lat_lon_alt(tle_line1, tle_line2)

# Format output
lat_str = f"{abs(lat):.6f}° {'N' if lat >= 0 else 'S'}"
lon_str = f"{abs(lon):.6f}° {'E' if lon >= 0 else 'W'}"

# Print results
print(f"Satellite: {tle_name}")
print(f"Latitude: {lat_str}")
print(f"Longitude: {lon_str}")
print(f"Altitude: {alt:.2f} meters")

